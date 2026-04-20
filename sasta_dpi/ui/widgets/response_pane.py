from textual.app import ComposeResult
from textual.widgets import Static, DataTable

class ResponsePane(Static):
    def compose(self) -> ComposeResult:
        # We use DataTable for tracking responses
        table = DataTable(id="response-table")
        table.cursor_type = "row"
        table.zebra_stripes = True
        yield table

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Time", "Protocol", "Status", "Latency", "Summary")

    def add_response(self, time_str, proto, status, latency, summary):
        table = self.query_one(DataTable)
        table.add_row(time_str, proto, status, latency, summary)
        table.scroll_to_bottom()
