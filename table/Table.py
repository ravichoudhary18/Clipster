from textual.widgets import DataTable
from textual.events import Key
from database.query import get_all, create, update
import pyperclip


class Table(DataTable):
    def __init__(self):
        super().__init__()
        self.add_column("ID")
        self.add_column("Content", width=60)
        self.add_column("Pinned")
        self.add_column("Delete")

        self.load_rows()

    def load_rows(self):
        self.clear()
        for clip in get_all():
            pin_icon = "📌" if bool(clip.pinned) else "📍"
            delete_icon = "❌"
            self.add_row(str(clip.id), clip.clip, pin_icon, delete_icon)

    def add_clip(self, content: str, pinned: bool = False) -> None:
        create(content, pinned=pinned)
        self.load_rows()

    async def on_key(self, event: Key) -> None:
        if not self.cursor_coordinate:
            return

        row_index, _ = self.cursor_coordinate
        row_data = self.get_row_at(row_index)
        if not row_data or len(row_data) < 2:
            return

        clip_text = row_data[1]

        if event.key == "enter":
            pyperclip.copy(clip_text)
            self.app.notify(
                f"Copied: {clip_text[:30]}{'...' if len(clip_text) > 30 else ''}"
            )

        elif event.key == "p":
            # Toggle pin
            current_pin = row_data[2] == "📌"
            update(clip=clip_text, pinned=not current_pin)
            self.load_rows()

        elif event.key == "r":
            # Delete the clip
            from database.query import delete

            delete(clip_text)
            self.load_rows()
            self.app.notify("Deleted.")
