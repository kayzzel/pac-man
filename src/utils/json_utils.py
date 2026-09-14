from typing import Any
from pathlib import Path

import json


def get_json_from_file(filename: str) -> list[Any] | dict[Any, Any]:
    path = Path(filename)
    if not path.exists():
        raise ValueError(f"ERROR: config file not found: {filename}")
    try:
        with open(path) as f:
            data: list[Any] | dict[Any, Any] = json.load(f)
    except json.JSONDecodeError as err:
        raise ValueError(f"ERROR: Invalid JSON in dataset: {err}")
    except Exception as err:
        raise ValueError(f"ERROR: Couldn't open the dataset: {err}") from err

    return data
