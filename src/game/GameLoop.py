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
        """
            Description:
        Create a loop calling update at a fixed rate, at most 100
        times per second, for the given duration of active time.

            Parameters:
        update -> the function called at each tick, given the game
        tick_rate -> wanted ticks per second, capped at 100
        duration -> active seconds before the game is lost
        """
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
        """
            Description:
        Give the seconds of active time left before the game is lost.

            Returns value:
        return the remaining seconds, as an int
        """
        return int(self.__duration - self.__elapsed_active)

    @property
    def elapsed_time(self) -> float:
        """
            Description:
        Give the active seconds elapsed since the last reset, pauses
        excluded.

            Returns value:
        return the elapsed active time, in seconds
        """
        return self.__elapsed_active

    def pause(self) -> None:
        """
            Description:
        Pause the loop: the thread parks on an event, consuming no
        CPU, until resume() or stop() is called.
        """
        self.__paused = True
        self.__resume_event.clear()

    def resume(self) -> None:
        """
            Description:
        Unpause the loop, waking the parked thread instantly, and
        start counting the active time again.
        """
        self.__paused = False
        self.__resume_event.set()

    def stop(self) -> None:
        """
            Description:
        Ask the loop to end: it also wakes a parked thread so stop
        never hangs on a paused loop.
        """
        self.__running = False
        self.__resume_event.set()

    def reset(self) -> None:
        """
            Description:
        Put the elapsed active time back to 0, typically for a new
        level.
        """
        self.__elapsed_active = 0.0

    def run(self, game: "Game") -> None:
        """
            Description:
        Run the fixed-timestep loop until it is stopped: missed time
        is caught up (500 ms at most per frame), so the game clock
        follows the wall clock, and the game is lost when the
        duration of active time is reached.

            Parameters:
        game -> the game given to the update at each tick
        """
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
