from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Vertical
from database.query import init_db
from table.Table import Table
from utils.clip import check_clipboard

class ClipStack(App):
    BINDINGS = [
        ("ctrl+c", "quit", "Quit the program"),
        ("ctrl+q", "quit", "Quit the program"),
        ("d", "toggle_dark", "Toggle dark mode")
    ]

    def action_quit(self) -> None:
        self.exit()

    def __init__(self):
        super().__init__()
        init_db()
        self.last_clipboard = ''

    def compose(self) -> ComposeResult:
        yield Header()
        self.table = Table()
        with Vertical():
            yield self.table
        yield Footer()

    async def on_mount(self) -> None:
        self.set_interval(1, self.poll_clipboard)

    def poll_clipboard(self) -> None:
        result = check_clipboard(self.last_clipboard)
        if result:
            self.last_clipboard = result
            self.table.add_clip(result)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    ClipStack().run()
