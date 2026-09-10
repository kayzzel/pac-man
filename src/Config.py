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

    def load_config(self, filename: str):
        ...

    @property
    def highscore_filename(self):
        return self.__highscore_filename

    @property
    def nb_level(self):
        return self.__nb_level

    @property
    def lives(self):
        return self.__lives

    @property
    def pacgum(self):
        return self.__pacgum

    @property
    def point_per_pacgum(self):
        return self.__point_per_pacgum

    @property
    def point_per_super_pacgum(self):
        return self.__point_per_super_pacgum

    @property
    def point_per_ghost(self):
        return self.__point_per_ghost

    @property
    def seed(self):
        return self.__seed

    @property
    def level_max_time(self):
        return self.__level_max_time
