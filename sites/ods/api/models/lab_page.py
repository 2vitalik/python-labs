from typing import Annotated

from beanie import Document, Indexed


class LabPage(Document):
    """What stands where among the labs' pages: a lab's own page and its parts, the pages common to all labs.
    The texts are guide pages by the same slug; this list is the disk's and is rewritten by content_io.py."""
    slug: Annotated[str, Indexed(unique=True)]  # lab3 · lab3-guide · labs-grading
    kind: str  # lab · common
    lab: int | None = None
    part: str = ""  # the address word: /labs/3/<part>, /labs/about/<part>; "" — the lab's own page
    nav: str  # the short word of the link
    order: int = 0
    files: list[dict] = []  # what the page hands out: {name, title, url}

    class Settings:
        name = "lab_pages"
