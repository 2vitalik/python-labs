from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from config import settings
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
    return await oauth.google.authorize_redirect(request, redirect_uri, hd=NURE_DOMAIN)


@router.get("/callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    info = token["userinfo"]
    if not info.get("email_verified"):
        return RedirectResponse("/?error=verify")
    if info.get("hd") != NURE_DOMAIN and info["email"] not in settings.admin_list:
        return RedirectResponse("/?error=domain")
    await upsert_user(info)
    request.session["email"] = info["email"]
    return RedirectResponse("/")


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


@router.get("/dev-login")
async def dev_login(request: Request):
    if settings.fake_user_email:
        await upsert_user({"email": settings.fake_user_email, "name": "Dev User"})
        request.session["email"] = settings.fake_user_email
    return RedirectResponse("/")


async def upsert_user(info: dict):
    email = info["email"]
    user = await User.find_one(User.email == email) or User(email=email)
    user.name = info.get("name", "")
    user.picture = info.get("picture", "")
    if email in settings.admin_list:
        user.status = Status.admin
    await user.save()
