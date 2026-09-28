import pyray as pr
from .View import View
from .widget import Panel


class Scores_view(View):

    def __init__(self, app, scores: dict[str, int]) -> None:

        super().__init__(app)

        self.title: str = "BEST SCORES"
        self.scores: list[str] = [
            pl_name + ": " + str(pl_score)
            for pl_name, pl_score in scores.items()
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

    def _update_back_button(self) -> None:

        back_label: str = "back <-|"
        back_font_sz: int = self.h // 20
        back_padding: int = back_font_sz - 5

        back_width: int = (
            pr.measure_text(back_label, back_font_sz)
        ) + back_padding
        back_height: int = back_font_sz + back_padding

        self.back_button: Panel = Panel(
            self.w - back_width - 10,
            self.h - back_height - 10,
            back_width,
            back_height,
            {back_label: (self.app.return_to_prev_view, None)},
            back_font_sz,
            (back_padding, 2, 0.1)
        )

    def _update_scores(self) -> None:

        scores_start: int = self.title_y * 2 + self.title_size

        scores_height: int = self.h - scores_start

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

        self.score_y -= self.score_font_sz

    def _update(self) -> None:

        if pr.is_key_pressed(pr.KEY_ESCAPE):
            self.app.return_to_prev_view()

        if not pr.is_window_resized() and self.is_init:
            return

        self._update_back_button()
        self._update_scores()
        self.is_init = True

    def display_view(self) -> None:

        self._update()

        pr.draw_text(
            self.title,
            self.title_x,
            self.title_y,
            self.title_size,
            pr.RAYWHITE
        )
        self.back_button.display_widget()

        for i, score in enumerate(self.scores):

            pr.draw_text(
                score,
                (self.w - pr.measure_text(score, self.score_font_sz)) // 2,
                self.score_y + self.score_font_sz * i + self.score_font_sz * (i + 1),
                self.score_font_sz,
                pr.RAYWHITE
            )
