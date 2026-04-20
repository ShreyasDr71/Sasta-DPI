from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Header, Footer

from sasta_dpi.ui.widgets.config_pane import ConfigPane
from sasta_dpi.ui.widgets.response_pane import ResponsePane
from sasta_dpi.ui.widgets.capture_pane import CapturePane
from sasta_dpi.ui.widgets.stats_bar import StatsBar
from sasta_dpi.ui.widgets.command_input import CommandInput
from sasta_dpi.core.session import PacketConfig
from sasta_dpi.protocols import get_engine

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

    async def on_input_submitted(self, event) -> None:
        if event.input.id == "command-input":
            cmd = event.value.strip()
            event.input.display = False
            event.input.value = ""
            self.app.set_focus(None)
            
            if cmd == ":send":
                await self.execute_send()
            elif cmd in (":q", ":quit"):
                self.app.exit()
                
    async def execute_send(self):
        config_pane = self.query_one(ConfigPane)
        protocol = config_pane.query_one("#protocol-select").value
        target = config_pane.query_one("#target-input").value
        port_val = config_pane.query_one("#port-input").value
        
        if not target:
            self.query_one(ResponsePane).add_response("-", "-", "Error", 0, "Target missing")
            return
            
        port = int(port_val) if port_val else 80
        
        config = PacketConfig(protocol=str(protocol), target=target, port=port)
        engine = get_engine(str(protocol))
        
        if not engine:
            self.query_one(ResponsePane).add_response("-", str(protocol), "Error", 0, "Engine not implemented")
            return
            
        import time
        t_str = time.strftime("%H:%M:%S")
        res = await engine.send(config)
        
        self.query_one(ResponsePane).add_response(t_str, protocol.upper(), res.status, f"{res.latency:.2f}ms", res.summary)
        
        cap_pane = self.query_one(CapturePane)
        cap_pane.clear()
        cap_pane.log_packet(str(res.raw_data))
        
        # update stats
        stats = self.query_one(StatsBar)
        stats.sent += 1
        if res.status != "Error":
             stats.received += 1
        else:
             stats.errors += 1

