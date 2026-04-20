from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Header, Footer

from sasta_dpi.ui.widgets.config_pane import ConfigPane
from sasta_dpi.ui.widgets.response_pane import ResponsePane
from sasta_dpi.ui.widgets.capture_pane import CapturePane
from sasta_dpi.ui.widgets.stats_bar import StatsBar
from sasta_dpi.ui.widgets.command_input import CommandInput

class MainScreen(Screen):
    BINDINGS = [
        ("colon", "focus_command", "Command Mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield StatsBar(id="stats-bar")
        
        with Grid(id="main-grid"):
            yield ConfigPane(id="config-pane")
            with Vertical(id="right-col"):
                yield ResponsePane(id="response-pane")
                yield CapturePane(id="capture-pane")
                
        yield CommandInput(id="command-input")
        yield Footer()

    def action_focus_command(self) -> None:
        cmd_input = self.query_one(CommandInput)
        cmd_input.activate()
