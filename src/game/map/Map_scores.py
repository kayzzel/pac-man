from ...utils.json_utils import (
            get_json_from_file,
            write_json_to_file,
            JsonUtilsError
        )

from sys import stderr
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError, TypeAdapter


class Score(BaseModel):
    name: str = Field(min_length=1, max_length=10)
    score: int = Field(ge=0)


class Map_scores:
    def __init__(self, map_name: str, score_file: str) -> None:
        self.map_name: str = map_name
        self.score_file: str = score_file
        self.scores: list[Score] = []

        self.load_scores()

    def load_scores(self) -> None:
        Score_list = TypeAdapter(list[Score])

        try:
            data = get_json_from_file(str(self.score_file))
            self.scores = Score_list.validate_python(data)
        except (ValidationError, JsonUtilsError) as err:
            print(
                    "WARNING: couldn't load the score file "
                    f"{self.score_file}: {err}",
                    file=stderr
                )
            self.scores = []
            return

        self.scores.sort(key=(lambda e: e.score), reverse=True)

    def add_score(self, name: str, score: int) -> bool:
        try:
            entry = Score(name=name, score=score)
        except ValidationError:
            print(
                    "WARNING: invalid score entry ignored "
                    f"(name={name!r}, score={score})",
                    file=stderr
              )
            return False

        self.scores.append(entry)
        self.scores.sort(key=(lambda e: e.score), reverse=True)
        write_json_to_file(
                str(self.score_file),
                [e.model_dump() for e in self.scores]
            )

        return True
