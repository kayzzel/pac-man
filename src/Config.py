from .utils.json_utils import get_json_from_file
from typing import Any
from pydantic import BaseModel, Field, ValidationError


class ConfigValidate(BaseModel):
    model_config = {"extra": "ignore"}

    highscore_filename: str = Field(min_length=1)
    nb_level: int = Field(ge=10)
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=0)
    point_per_pacgum: int = Field(ge=0)
    point_per_super_pacgum: int = Field(ge=0)
    point_per_ghost: int = Field(ge=0)
    seed: int = Field(ge=0)
    level_max_time: int = Field(ge=1)


class Config:
    def __init__(self) -> None:
        self.__highscore_filename: str = "highscore.json"
        self.__nb_level: int = 10
        self.__lives: int = 3
        self.__pacgum: int = 42
        self.__point_per_pacgum: int = 10
        self.__point_per_super_pacgum: int = 50
        self.__point_per_ghost: int = 200
        self.__seed: int = 42
        self.__level_max_time: int = 90

    def load_config(self, filename: str) -> None:
        try:
            config_data: Any = get_json_from_file(filename)
        except ValueError as err:
            raise ValueError(err) from err

        if (not isinstance(config_data, dict)):
            raise ValueError("ERROR: Config file must contain a dict")

        try:
            config = ConfigValidate(**config_data)
        except ValidationError as err:
            raise ValueError(
                f"ERROR: Config file do not match expected schema: {err}"
            ) from err

        self.__highscore_filename = config.highscore_filename
        self.__nb_level = config.nb_level
        self.__lives = config.lives
        self.__pacgum = config.pacgum
        self.__point_per_pacgum = config.point_per_pacgum
        self.__point_per_super_pacgum = config.point_per_super_pacgum
        self.__point_per_ghost = config.point_per_ghost
        self.__seed = config.seed
        self.__level_max_time = config.level_max_time

    @property
    def highscore_filename(self) -> str:
        return self.__highscore_filename

    @property
    def nb_level(self) -> int:
        return self.__nb_level

    @property
    def lives(self) -> int:
        return self.__lives

    @property
    def pacgum(self) -> int:
        return self.__pacgum

    @property
    def point_per_pacgum(self) -> int:
        return self.__point_per_pacgum

    @property
    def point_per_super_pacgum(self) -> int:
        return self.__point_per_super_pacgum

    @property
    def point_per_ghost(self) -> int:
        return self.__point_per_ghost

    @property
    def seed(self) -> int:
        return self.__seed

    @property
    def level_max_time(self) -> int:
        return self.__level_max_time
