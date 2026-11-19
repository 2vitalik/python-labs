from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class LabShape(Document):
    """A lab's notebook (T354 §2): the templates cell by cell with the task each cell is, the tasks and the plots level 14 waits for,
    the templates to hand out. From disk by lab_io.py (labs_shape.py); a lab without one still takes files."""
    lab: Annotated[int, Indexed(unique=True)]
    cells: list[dict] = []  # the Jupyter template: {kind, sig, role, key, title, case, names, source}
    mcells: list[dict] = []  # the marimo one
    tasks: list[dict] = []  # {key, role, case, title, plot, names}
    plots: int = 0
    jupyter: bytes = b""
    marimo: str = ""
    live: bool = False  # the service cell reports check() to the site: the card gets a TOKEN
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "lab_shapes"

    def view(self) -> dict:
        """What the notebook readers take (labs_facts, labs_show)."""
        return {"cells": self.cells, "mcells": self.mcells, "tasks": self.tasks, "plots": self.plots}
