from textual.widgets import DataTable
from database.query import get_all


class Table(DataTable):
    def __init__(self):
        super().__init__()
        self.add_columns("ID", "Content", "Pinned")
        for clip in get_all():
            self.add_row(str(clip.id), str(clip.clip), str(clip.pinned))

    def add_clip(self, content: str, pinned: bool = False) -> None:
        row_id = str(len(self.rows) + 1)
        self.add_row(row_id, content, str(pinned))