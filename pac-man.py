from src.App import App


def main() -> None:
    app = App()
    app.load_config("config.json")


if __name__ == "__main__":
    main()
