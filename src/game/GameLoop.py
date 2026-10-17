from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Game import Game   # only imported by type checkers, not at runtime
from ..utils.enum_utils import Game_state

from typing import Callable

import time
import threading


class GameLoop:
    """Fixed-timestep loop, capped at `tick_rate` (<=100/s), pausable with
    minimal drift: paused time is never added to the elapsed timer."""

    def __init__(
        self,
        update: Callable[["Game"], None],
        tick_rate: float = 100.0,
        duration: float = 90,
    ) -> None:
        self.__update = update
        self.__dt: float = 1.0 / min(tick_rate, 100.0)
        self.__duration = duration
        self.__elapsed_active: float = 0.0
        self.__paused = False
        self.__running = False
        self.__resume_event = threading.Event()
        self.__resume_event.set()

    @property
    def timer(self) -> int:
        return int(self.__duration - self.__elapsed_active)

    @property
    def elapsed_time(self) -> float:
        return self.__elapsed_active

    def pause(self) -> None:
        self.__paused = True
        self.__resume_event.clear()

    def resume(self) -> None:
        self.__paused = False
        self.__resume_event.set()

    def stop(self) -> None:
        self.__running = False
        self.__resume_event.set()

    def reset(self) -> None:
        self.__elapsed_active = 0.0

    def run(self, game: "Game") -> None:
        self.__running = True
        accumulator = 0.0
        last_time = time.perf_counter()

        while self.__running:
            now = time.perf_counter()
            frame_time = now - last_time
            last_time = now

            if self.__paused:
                self.__resume_event.wait()
                last_time = time.perf_counter()
                continue

            frame_time = min(frame_time, 0.25)
            accumulator += frame_time

            while accumulator >= self.__dt:
                self.__update(game)
                accumulator -= self.__dt
                self.__elapsed_active += self.__dt

                if self.__elapsed_active >= self.__duration:
                    self.__running = False
                    game.state = Game_state.LOST
                    break

            sleep_time = self.__dt - accumulator
            if sleep_time > 0:
                time.sleep(sleep_time)
