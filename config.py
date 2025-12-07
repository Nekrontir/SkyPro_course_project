from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.resolve()

PATHS = {
    "data": PROJECT_ROOT / "data",
    "logs": PROJECT_ROOT / "logs",
    "get_data": PROJECT_ROOT / "data" / "operations.xlsx",
    "user_settings": PROJECT_ROOT / "user_settings.json",
}

for path in [PATHS["data"], PATHS["logs"]]:
    path.mkdir(exist_ok=True)
