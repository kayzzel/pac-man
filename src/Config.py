from .utils.json_utils import get_json_from_file

from sys import stderr
from typing import Any, Annotated
from pydantic import BaseModel, Field, ValidationError


class ConfigValidate(BaseModel):
    """The pydantic model validating each value of the config file."""
    model_config = {"extra": "ignore"}

    highscore_filename: str = Field(default="highscore.json", min_length=1)
    nb_level: int = Field(default=10, ge=10)
    levels_dimensions: tuple[
        Annotated[int, Field(ge=10, le=50)],
        Annotated[int, Field(ge=10, le=50)]
    ] = (15, 15)
    lives: int = Field(default=3, ge=1)
    point_per_pacgum: int = Field(default=10, ge=0)
    point_per_super_pacgum: int = Field(default=50, ge=0)
    point_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=90, ge=1)


class Config:
    """The loaded config: every game value, with safe defaults."""

    def __init__(self) -> None:
        """
            Description:
        Create a config holding every default value, ready to be
        loaded from a file (or used as is, for custom games).
        """
        self.__highscore_filename: str = "highscore.json"
        self.__nb_level: int = 10
        self.__levels_dimensions: tuple[int, int] = (15, 15)
        self.__lives: int = 3
        self.__point_per_pacgum: int = 10
        self.__point_per_super_pacgum: int = 50
        self.__point_per_ghost: int = 200
        self.__seed: int = 42
        self.__level_max_time: int = 90

    def load_config(self, filename: str) -> None:
        """
            Description:
        Load a json config file (comments supported): every missing or
        invalid value falls back to its default with a warning, and
        unknown keys are ignored, so a loaded config is always
        complete and valid.

            Parameters:
        filename -> path of the json config file
        """
        config_data = get_json_from_file(filename)
        if not isinstance(config_data, dict):
            print(
                    "ERROR: Config file must contain a dict, using defaults",
                    file=stderr
                )
            config_data = {}

        result: dict[str, Any] = {}
        for name, field in ConfigValidate.model_fields.items():
            if name not in config_data:
                print(
                    f"WARNING: missing '{name}', "
                    f"using default {field.default}",
                    file=stderr,
                )
            raw_value = config_data.get(name, field.default)
            try:
                result[name] = getattr(
                    ConfigValidate.model_validate({name: raw_value}), name
                )
            except ValidationError:
                print(
                        f"WARNING: invalid '{name}', "
                        f"using default {field.default}",
                        file=stderr
                    )
                result[name] = field.default

        config = ConfigValidate(**result)
        self.__highscore_filename = config.highscore_filename
        self.__nb_level = config.nb_level
        self.__levels_dimensions = config.levels_dimensions
        self.__lives = config.lives
        self.__point_per_pacgum = config.point_per_pacgum
        self.__point_per_super_pacgum = config.point_per_super_pacgum
        self.__point_per_ghost = config.point_per_ghost
        self.__seed = config.seed
        self.__level_max_time = config.level_max_time

    @property
    def highscore_filename(self) -> str:
        """
            Description:
        Give the file where the mandatory game keeps its scores.

            Returns value:
        return the score file path of the mandatory game
        """
        return self.__highscore_filename

    @property
    def nb_level(self) -> int:
        """
            Description:
        Give the number of levels of the mandatory game.

            Returns value:
        return the number of levels, at least 10
        """
        return self.__nb_level

    @property
    def levels_dimensions(self) -> tuple[int, int]:
        """
            Description:
        Give the (width, height) of the generated levels, in cells.

            Returns value:
        return the dimensions of a level
        """
        return self.__levels_dimensions

    @property
    def lives(self) -> int:
        """
            Description:
        Give the number of lives the player starts with.

            Returns value:
        return the starting lives
        """
        return self.__lives

    @property
    def point_per_pacgum(self) -> int:
        """
            Description:
        Give the points awarded for one pacgum.

            Returns value:
        return the value of a pacgum
        """
        return self.__point_per_pacgum

    @property
    def point_per_super_pacgum(self) -> int:
        """
            Description:
        Give the points awarded for one super pacgum.

            Returns value:
        return the value of a super pacgum
        """
        return self.__point_per_super_pacgum

    @property
    def point_per_ghost(self) -> int:
        """
            Description:
        Give the points awarded for one eaten ghost.

            Returns value:
        return the value of an eaten ghost
        """
        return self.__point_per_ghost

    @property
    def seed(self) -> int:
        """
            Description:
        Give the seed generating the first level of the mandatory
        game: same seed, same first level.

            Returns value:
        return the seed of the first level
        """
        return self.__seed

    @property
    def level_max_time(self) -> int:
        """
            Description:
        Give the active seconds allowed per level: beyond that the
        game is lost.

            Returns value:
        return the time limit of a level, in seconds
        """
        return self.__level_max_time
