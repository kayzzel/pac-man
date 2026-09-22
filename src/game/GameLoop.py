import time
from typing import Callable


class GameLoop:
    """Fixed-timestep loop, capped at `tick_rate` (<=100/s), pausable with
    minimal drift: paused time is never added to the elapsed timer."""

    def __init__(
        self,
        update: Callable[[float], None],
        tick_rate: float = 100.0,
        duration: float = 90,
    ) -> None:
        self.__update = update
        self.__dt: float = 1.0 / min(tick_rate, 100.0)
        self.__duration = duration       # active (unpaused) seconds; None = no limit
        self.__elapsed_active: float = 0.0
        self.__paused = False
        self.__running = False

    @property
    def timer(self) -> int:
        return int(self.__duration - self.__elapsed_active)

    def pause(self) -> None:
        self.__paused = True

    def resume(self) -> None:
        self.__paused = False

    def stop(self) -> None:
        self.__running = False

    def run(self) -> None:
        self.__running = True
        accumulator = 0.0
        last_time = time.perf_counter()

        while self.__running:
            now = time.perf_counter()
            frame_time = now - last_time
            last_time = now

            if self.__paused:
                time.sleep(self.__dt)   # avoid a busy spin while idle
                continue

            # clamp: prevents a "spiral of death" after a long stall
            # (breakpoint, OS scheduling hiccup, window drag, etc.)
            frame_time = min(frame_time, 0.25)
            accumulator += frame_time

            while accumulator >= self.__dt:
                self.__update(self.__dt)
                accumulator -= self.__dt
                self.__elapsed_active += self.__dt

                if self.__duration is not None \
                        and self.__elapsed_active >= self.__duration:
                    self.__running = False
                    break

            sleep_time = self.__dt - accumulator
            if sleep_time > 0:
                self.__precise_sleep(sleep_time)

    @staticmethod
    def __precise_sleep(seconds: float) -> None:
        """time.sleep() alone can overshoot by several ms on some OSes.
        Sleep the bulk of the wait, then busy-spin the last ~1ms for accuracy."""
        target = time.perf_counter() + seconds
        margin = 0.001
        if seconds > margin:
            time.sleep(seconds - margin)
        while time.perf_counter() < target:
            pass
