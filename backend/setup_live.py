"""Run privately in a terminal. Does not contact a provider or overwrite .env."""
import getpass
import os
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    target = root / "backend" / ".env"
    if target.exists():
        print("backend/.env already exists; preserved it. Edit that file locally if needed.")
        return 1
    ignored = subprocess.run(["git", "check-ignore", "--quiet", "backend/.env"], cwd=root)
    if ignored.returncode != 0:
        print("Stopped: backend/.env must be ignored by Git first.")
        return 1
    if not sys.stdin.isatty():
        print("Run this in an interactive terminal; the key must not enter a command or log.")
        return 1
    print("Set up optional OpenAI chat. API usage may incur charges. No call is made by this setup.")
    key = getpass.getpass("OpenAI API key (hidden; press Enter to cancel): ").strip()
    if not key:
        print("Cancelled. Demo mode remains available.")
        return 0
    if any(char.isspace() for char in key):
        print("Key contains whitespace. Nothing saved.")
        return 1
    # O_EXCL preserves any file created concurrently; 0600 is owner-only.
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(f"PROVIDER_MODE=openai\nOPENAI_API_KEY={key}\nOPENAI_MODEL=gpt-4.1-mini\nDEMO_SESSION_ID=part2-local\n")
    print("Saved privately to backend/.env. Restart FastAPI, then reload Chat.")
    print("A successful live reply still needs verification. The persistent cap is 50 calls (two per exchange).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
