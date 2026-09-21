from datetime import datetime, timezone
from urllib.parse import quote

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, BackgroundTasks, Request
from starlette.responses import RedirectResponse

from bot import alerts
from config import settings
from models.activity import Activity
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
async def login(request: Request, next: str = "/"):
    request.session["next"] = safe_path(next)  # SPA state doesn't survive the Google round-trip
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, hd=NURE_DOMAIN, prompt="select_account")


@router.get("/callback")
async def callback(request: Request, tasks: BackgroundTasks):
    next = request.session.pop("next", "/")
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:  # cancelled at Google or stale state: back to the form, not a 500
        return to_login("oauth", next)
    info = token["userinfo"]
    if not info.get("email_verified"):
        return to_login("verify", next)
    if info.get("hd") != NURE_DOMAIN and info["email"] not in settings.admin_list:
        return to_login("domain", next)
    await upsert_user(info, tasks)
    request.session["email"] = info["email"]
    return RedirectResponse(next)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


@router.get("/dev-login")
async def dev_login(request: Request, tasks: BackgroundTasks, next: str = "/"):
    if settings.fake_user_email:
        await upsert_user({"email": settings.fake_user_email, "name": "Dev User"}, tasks)
        request.session["email"] = settings.fake_user_email
    return RedirectResponse(safe_path(next))


def safe_path(path: str) -> str:
    """Same-site paths only, so `?next=` can't bounce users to a foreign host."""
    return path if path.startswith("/") and path[1:2] not in ("/", "\\") else "/"


def to_login(error: str, next: str) -> RedirectResponse:
    return RedirectResponse(f"/login?error={error}&next={quote(next)}")


async def upsert_user(info: dict, tasks: BackgroundTasks):
    email = info["email"]
    user = await User.find_one(User.email == email)
    is_new = user is None
    user = user or User(email=email)
    first = user.first_seen_at is None
    user.last_seen_at = datetime.now(timezone.utc)
    user.first_seen_at = user.first_seen_at or user.last_seen_at
    user.name = info.get("name", "")
    user.picture = info.get("picture", "")
    if not user.last_name and not user.first_name:  # prefill empty names from Google claims
        user.last_name = info.get("family_name", "")
        user.first_name = info.get("given_name", "")
    if email in settings.admin_list:
        user.status = Status.admin
    await user.save()
    await Activity(user=email, kind="login").insert()
    if is_new:
        await record_new(user, actor=email)
    if first:
        tasks.add_task(alerts.signed_in, user)
