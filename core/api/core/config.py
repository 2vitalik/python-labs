from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Read in the site's folder: `site.env` — what the site is, kept in git; `.env` — secrets and this machine's values."""
    site_name: str = "Labs"  # the API title, the bot's texts
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "labs"
    google_client_id: str = ""
    google_client_secret: str = ""
    session_secret: str
    admin_emails: str = ""
    fake_user_email: str = ""
    tg_bot_name: str = ""
    tg_bot_token: str = ""  # from BotFather; empty = bot refuses to start
    site_url: str = "http://127.0.0.1:5000"  # links in bot messages; Telegram won't link `localhost`
    guide_dir: str = "data/guide"  # the guide's seed and snapshot, *.md
    uploads_dir: str = ""  # files people upload; what they are and the default folder — the site's
    agent_tokens: str = ""  # `name:token,…` — AI agents that edit the site's texts (deps.editor_user); empty = no such way in

    model_config = {"env_file": ("site.env", ".env"), "extra": "ignore"}

    @property
    def admin_list(self) -> list[str]:
        return [e.strip() for e in self.admin_emails.split(",") if e.strip()]

    @property
    def agents(self) -> dict[str, str]:
        """token → the agent's email; an empty token opens nothing."""
        pairs = (p.strip().partition(":") for p in self.agent_tokens.split(","))
        return {token: f"{name}@agent" for name, _, token in pairs if name and token}


settings = Settings()
