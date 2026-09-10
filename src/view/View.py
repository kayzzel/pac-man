from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...
