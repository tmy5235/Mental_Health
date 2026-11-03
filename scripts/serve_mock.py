"""Serve an explicitly selected fictional test database; never read live settings."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
import uvicorn
from app.config import Settings
from app.main import create_app

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--database', type=Path, required=True)
parser.add_argument('--port', type=int, default=8000)
args = parser.parse_args()
uvicorn.run(create_app(args.database.resolve(), Settings()), host='127.0.0.1', port=args.port)
