from src.App import App
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config.json>", file=sys.stderr)
        return 1
    app = App()
    return app.load_config(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
