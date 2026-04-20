from textual.app import ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

class StatsBar(Static):
    sent = reactive(0)
    received = reactive(0)
    errors = reactive(0)

    def watch_sent(self, old_value: int, new_value: int) -> None:
        self.update_stats()

    def watch_received(self, old_value: int, new_value: int) -> None:
        self.update_stats()

    def watch_errors(self, old_value: int, new_value: int) -> None:
        self.update_stats()

    def update_stats(self):
        sr = 0.0
        if self.sent > 0:
             sr = (self.received / self.sent) * 100
             
        self.update(f"Sent: {self.sent}  |  Received: {self.received}  |  Errors: {self.errors}  |  Success Rate: {sr:.1f}%")

    def on_mount(self) -> None:
        self.update_stats()
