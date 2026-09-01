from pathlib import Path
import sys

import uvicorn

ROOT = Path(__file__).resolve().parent


def run() -> None:
    sys.path.insert(0, str(ROOT))
    uvicorn.run("main:app", reload=True, app_dir=str(ROOT))
