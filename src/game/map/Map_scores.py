from ...utils.json_utils import (
            get_json_from_file,
            write_json_to_file,
            JsonUtilsError
        )

from sys import stderr
from pathlib import Path
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    TypeAdapter,
    field_validator
)


class Score(BaseModel):
    """One highscore entry: a player name and their score."""
    name: str = Field(min_length=1, max_length=10)
    score: int = Field(ge=0)

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        """
            Description:
        Keep the player names meaningful: 1 to 10 characters, made of
        letters, digits and spaces only, and never spaces alone.

            Parameters:
        value -> the name read from the file or given by the player

            Returns value:
        return the name when it is valid

            Raises:
        ValueError when the name breaks one of the rules
        """
        if (
                not all(
                    char.isascii() and char.isalnum() or
                    char == " " for char in value
                )
                or not value.strip()
        ):
            raise ValueError(
                "name must be alphanumeric characters and spaces only"
            )
        return value


class Map_scores:
    """The persistent top-10 scores of one map or game mode."""

    def __init__(self, map_name: str, score_path: Path) -> None:
        """
            Description:
        Create the scores of one map on its score file, loading it:
        a missing or broken file starts from an empty score board,
        so a fresh install just works.

            Parameters:
        map_name -> the name of the map or mode the scores belong to
        score_path -> the json file keeping the scores
        """
        self.map_name: str = map_name
        self.score_file: Path = score_path
        self.score_file.parent.mkdir(parents=True, exist_ok=True)
        self.scores: list[Score] = []

        self.load_scores()

    def load_scores(self) -> None:
        """
            Description:
        Load the score file, sorted from the best score down and
        capped to the top 10: an unreadable or invalid file is only
        a warning, and the scores start empty.
        """
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
        self.scores = self.scores[0:10]

    def add_score(self, name: str, score: int) -> bool:
        """
            Description:
        Add a score entry, keep the board sorted from the best score
        down, capped to the top 10, and save it to the file: a new
        best score ends up in first position, a weak one only takes
        a spot in the top 10.

            Parameters:
        name -> the player name, validated by the Score model
        score -> the player score, 0 or more

            Returns value:
        return True when the entry was valid and saved, False when
        the name or the score was refused
        """
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
        self.scores = self.scores[0:10]
        write_json_to_file(
                str(self.score_file),
                [e.model_dump() for e in self.scores]
            )

        return True
