from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "labs"
    google_client_id: str = ""
    google_client_secret: str = ""
    session_secret: str
    admin_emails: str = ""
    fake_user_email: str = ""

    model_config = {"env_file": ".env"}

    @property
    def admin_list(self) -> list[str]:
        return [e.strip() for e in self.admin_emails.split(",") if e.strip()]


settings = Settings()
