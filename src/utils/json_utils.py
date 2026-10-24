from typing import Any
from pathlib import Path

import json


class JsonUtilsError(ValueError):
    """Base class for all json_utils errors."""


class JsonFileNotFoundError(JsonUtilsError):
    """Raised when the requested file does not exist."""


class JsonFileReadError(JsonUtilsError):
    """Raised when the file exists but cannot be read."""


class JsonParseError(JsonUtilsError):
    """Raised when the file content is not valid JSON."""


class JsonSerializationError(JsonUtilsError):
    """Raised when the data cannot be serialized to JSON."""


class JsonFileWriteError(JsonUtilsError):
    """Raised when the file cannot be written to."""


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
        raise JsonFileNotFoundError(f"File not found: {filename!r}")
    try:
        with open(path) as f:
            raw = f.read()
    except OSError as err:
        raise JsonFileReadError(f"Couldn't read {filename!r}: {err}") from err
    except UnicodeError as err:
        raise JsonFileReadError(
                f"Couldn't decode {filename!r} as UTF-8: {err}"
            ) from err

    text = _strip_comments(raw)
    if not text.strip():
        return {}

    try:
        data: list[Any] | dict[Any, Any] = json.loads(text)
    except json.JSONDecodeError as err:
        raise JsonParseError(f"Invalid JSON in {filename!r}: {err}") from err

    return data


def write_json_to_file(
            filename: str,
            data: dict[Any, Any] | list[Any]
        ) -> None:
    try:
        text = json.dumps(data, indent=4)
    except (TypeError, ValueError) as err:
        raise JsonSerializationError(
                f"Data is not JSON serializable for {filename!r}: {err}"
            ) from err

    try:
        with open(filename, "w") as f:
            f.write(text)
    except OSError as err:
        raise JsonFileWriteError(
                f"Couldn't write to {filename!r}: {err}"
            ) from err
