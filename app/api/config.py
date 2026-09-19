from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "python_labs"
    google_client_id: str = ""
    google_client_secret: str = ""
    session_secret: str
    admin_emails: str = ""
    fake_user_email: str = ""
    tg_bot_name: str = ""
    tg_bot_token: str = ""  # from BotFather; empty = bot refuses to start
    site_url: str = "http://127.0.0.1:5030"  # links in bot messages; Telegram won't link `localhost`
    uploads_dir: str = ""  # empty = app/api/uploads

    model_config = {"env_file": ".env"}

    @property
    def admin_list(self) -> list[str]:
        return [e.strip() for e in self.admin_emails.split(",") if e.strip()]


settings = Settings()
