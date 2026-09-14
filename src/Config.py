from .utils.json_utils import get_json_from_file

from sys import stderr
from typing import Any
from pydantic import BaseModel, Field, ValidationError


class ConfigValidate(BaseModel):
    model_config = {"extra": "ignore"}

    highscore_filename: str = Field(default="highscore.json", min_length=1)
    nb_level: int = Field(default=10, ge=10)
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=0)
    point_per_pacgum: int = Field(default=10, ge=0)
    point_per_super_pacgum: int = Field(default=50, ge=0)
    point_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=90, ge=1)


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
