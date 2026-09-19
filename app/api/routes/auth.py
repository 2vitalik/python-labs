from datetime import datetime, timezone

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, BackgroundTasks, Request
from starlette.responses import RedirectResponse

from bot import alerts
from config import settings
from models.history import record_new
from models.user import Status, User

NURE_DOMAIN = "nure.ua"

router = APIRouter(prefix="/api/auth")

oauth = OAuth()
oauth.register(
    "google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, hd=NURE_DOMAIN, prompt="select_account")


@router.get("/callback")
async def callback(request: Request, tasks: BackgroundTasks):
    token = await oauth.google.authorize_access_token(request)
    info = token["userinfo"]
    if not info.get("email_verified"):
        return RedirectResponse("/?error=verify")
    if info.get("hd") != NURE_DOMAIN and info["email"] not in settings.admin_list:
        return RedirectResponse("/?error=domain")
    await upsert_user(info, tasks)
    request.session["email"] = info["email"]
    return RedirectResponse("/")


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


@router.get("/dev-login")
async def dev_login(request: Request, tasks: BackgroundTasks):
    if settings.fake_user_email:
        await upsert_user({"email": settings.fake_user_email, "name": "Dev User"}, tasks)
        request.session["email"] = settings.fake_user_email
    return RedirectResponse("/")


async def upsert_user(info: dict, tasks: BackgroundTasks):
    email = info["email"]
    user = await User.find_one(User.email == email)
    is_new = user is None
    user = user or User(email=email)
    first = user.seen_at is None
    user.seen_at = datetime.now(timezone.utc)
    user.name = info.get("name", "")
    user.picture = info.get("picture", "")
    if not user.last_name and not user.first_name:  # prefill empty names from Google claims
        user.last_name = info.get("family_name", "")
        user.first_name = info.get("given_name", "")
    if email in settings.admin_list:
        user.status = Status.admin
    await user.save()
    if is_new:
        await record_new(user, actor=email)
    if first:
        tasks.add_task(alerts.signed_in, user)
