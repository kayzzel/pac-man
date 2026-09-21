import pyray as pr
from .View import View


class Scores_menu(View):

    def __init__(self, app, scores: list[tuple[str, int]]) -> None:

        super().__init__(app)

        self.title: str = "BEST SCORES"
        self.scores: list[str] = [
            pl_name + ": " + str(pl_score)
            for pl_name, pl_score in scores
        ]

    @property
    def title_size(self) -> int:

        return self.h // 10

    @property
    def title_x(self) -> int:

        return (self.w - pr.measure_text(self.title, self.title_size)) // 2

    @property
    def title_y(self) -> int:

        return self.h // 15

    def calculate_score_spacing(self) -> None:

        scores_start: int = self.title_y * 2 + self.title_size

        scores_height: int = self.h - self.scores_start

        padding: int = scores_height // 8
        space_remaining: int = scores_height - padding * 2

        self.score_y: int = scores_start + padding

        self.score_font_sz: int = space_remaining // (
            len(self.scores) * 2 - 1
        )

        max_score: str = max(self.scores, key=lambda score: len(score))
        while (
            pr.measure_text(max_score, self.score_font_sz) >= self.w
        ) and (
            self.score_font_sz > 5
        ):
            self.score_font_sz -= 1

    def display_view(self) -> None:

        pr.draw_text(
            self.title,
            self.title_x,
            self.title_y,
            self.title_size,
            pr.RAYWHITE
        )

        self.calculate_score_spacing()
        self.score_y -= self.score_font_sz

        for i, score in enumerate(self.scores):

            pr.draw_text(
                score,
                (self.w - pr.measure_text(score, self.score_font_sz)) // 2,
                self.score_y + self.score_font_sz * i + self.score_font_sz * (i + 1),
                self.score_font_sz,
                pr.RAYWHITE
            )
