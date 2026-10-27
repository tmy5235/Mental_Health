"""Explicit backend-only configuration; never include secrets in repr or health."""
import os
from dataclasses import dataclass, field
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


@dataclass(frozen=True)
class Settings:
    mode: str = "mock"
    api_key: str = field(default="", repr=False)
    model: str = ""
    demo_session: str = "part2-local"

    @property
    def configured(self):
        return self.mode == "mock" or (self.mode == "openai" and bool(self.api_key and self.model))


def load_settings(path=ENV_PATH):
    # Simple NAME=value format, optional matching quotes; no shell expansion.
    values = {}
    if path.is_file():
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key.strip()] = value
    def get(key, default=""):
        return os.environ.get(key, values.get(key, default)).strip()
    return Settings(get("PROVIDER_MODE", "mock"), get("OPENAI_API_KEY"),
                    get("OPENAI_MODEL"), get("DEMO_SESSION_ID", "part2-local"))
