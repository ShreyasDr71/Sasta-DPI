from textual.app import ComposeResult
from textual.widgets import Static, RichLog
from textual.containers import VerticalScroll

class CapturePane(Static):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            RichLog(id="capture-log", wrap=True, highlight=True)
        )

    def log_packet(self, data: str):
        log = self.query_one(RichLog)
        log.write(data)

    def clear(self):
        self.query_one(RichLog).clear()
