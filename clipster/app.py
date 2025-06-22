from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.screen import Screen


# Define screen
class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("📋 Welcome to Clipster!\n\nPress Q to quit.", id="welcome")


# Define app
class ClipsterApp(App):
    CSS_PATH = Path(__file__).parent.parent / "assets" / "styles.css"
    TITLE = "Clipster"
    SUB_TITLE = "Terminal Clipboard Manager"

    def on_mount(self) -> None:
        self.push_screen(HomeScreen())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
