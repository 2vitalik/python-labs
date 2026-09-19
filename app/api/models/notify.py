from typing import Annotated

from beanie import Document, Indexed


class Route(Document):
    """Where admin alerts of one kind go: a chat, or a forum topic inside it; bound with /here (T111)."""
    kind: Annotated[str, Indexed(unique=True)]
    chat_id: int
    thread_id: int | None = None
    title: str = ""  # "chat › topic", shown by /here status

    class Settings:
        name = "routes"
