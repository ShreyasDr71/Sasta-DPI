from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class PacketConfig:
    protocol: str = "tcp"
    target: str = ""
    port: int = 80
    options: Dict[str, any] = field(default_factory=dict)

@dataclass
class SessionStats:
    sent: int = 0
    received: int = 0
    errors: int = 0
    start_time: float = field(default_factory=time.time)
    
    @property
    def success_rate(self) -> float:
        if self.sent == 0: return 0.0
        return (self.received / self.sent) * 100
        
    @property
    def time_elapsed(self) -> float:
        return time.time() - self.start_time

class Session:
    def __init__(self, name: str):
        self.name = name
        self.config = PacketConfig()
        self.stats = SessionStats()
        self.history = []

class SessionManager:
    def __init__(self):
        self.sessions: List[Session] = []
        self.active_index: int = -1
        self._create_default_session()

    def _create_default_session(self):
        self.create_session("Session 1")

    def create_session(self, name: str) -> Session:
        session = Session(name)
        self.sessions.append(session)
        if self.active_index == -1:
            self.active_index = 0
        return session

    def get_active(self) -> Optional[Session]:
        if 0 <= self.active_index < len(self.sessions):
            return self.sessions[self.active_index]
        return None

    def switch_session(self, index: int) -> bool:
        if 0 <= index < len(self.sessions):
            self.active_index = index
            return True
        return False
