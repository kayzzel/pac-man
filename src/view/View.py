from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, app) -> None:
        self.app = app

    def update(self) -> None:
        ...
