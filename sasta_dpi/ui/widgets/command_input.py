from textual.app import ComposeResult
from textual.widgets import Input
from textual import events

class CommandInput(Input):
    def on_mount(self) -> None:
        self.display = False # hidden by default

    def activate(self):
        self.display = True
        self.focus()
        self.value = ":"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.display = False
            self.value = ""
            self.app.set_focus(None)
