from typing import Any
from pathlib import Path

import json


def _strip_comments(text: str) -> str:
    """Remove #, // and /* */ comments while leaving string content intact."""
    out = []
    i, n = 0, len(text)
    in_string = False
    escape = False
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
            i += 1
            continue

        if c == '"':
            in_string = True
            out.append(c)
            i += 1
        elif c == "#" or (c == "/" and i + 1 < n and text[i + 1] == "/"):
            while i < n and text[i] != "\n":
                i += 1
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def get_json_from_file(filename: str) -> list[Any] | dict[Any, Any]:
    path = Path(filename)
    if not path.exists():
        raise ValueError(f"ERROR: config file not found: {filename}")
    try:
        with open(path) as f:
            raw = f.read()
        text = _strip_comments(raw)
        if not text.strip():
            return {}
        data: list[Any] | dict[Any, Any] = json.loads(text)
    except json.JSONDecodeError as err:
        raise ValueError(f"ERROR: Invalid JSON in dataset: {err}")
    except Exception as err:
        raise ValueError(f"ERROR: Couldn't open the dataset: {err}") from err

    return data
