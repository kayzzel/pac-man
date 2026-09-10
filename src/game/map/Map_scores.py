class Map_scores:
    def __init__(self) -> None:
        self.map_name: str = ""
        self.scores: dict[str, int] = {}

    def load_scores(self, map_name: str, score_file: str):
        ...

    def add_scores(self, name: str, score: int):
        ...
