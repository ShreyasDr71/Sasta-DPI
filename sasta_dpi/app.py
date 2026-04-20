import asyncio
from textual.app import App, ComposeResult
from sasta_dpi.ui.screens.main_screen import MainScreen
from sasta_dpi.core.session import SessionManager

class SastaDPI(App):
    """A Textual app to manage network packet crafting and sending."""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("?", "toggle_help", "Help"),
        ("ctrl+n", "new_session", "New Session"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_manager = SessionManager()

    def on_mount(self) -> None:
        self.push_screen(MainScreen())

    def action_toggle_help(self) -> None:
        """Toggle the help text."""
        pass # To be implemented
        
    def action_new_session(self) -> None:
        pass # To be implemented
