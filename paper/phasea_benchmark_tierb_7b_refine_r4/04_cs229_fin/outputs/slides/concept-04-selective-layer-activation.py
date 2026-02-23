from manim import *

class LayerActivationAnimation(Scene):
    def construct(self):
        squares = VGroup(*[
            Rectangle(width=0.7, height=1, stroke_width=2, fill_color=GRAY) if i < 7 or i > 10 and i != 23 else
            Rectangle(width=0.7, height=1, stroke_width=2, fill_color=BLUE) if 7 <= i <= 10 else
            Rectangle(width=0.7, height=1, stroke_width=2, fill_color=GRAY) if i > 23 else
            Rectangle(width=0.7, height=1, stroke_width=2, fill_color=ORANGE)
            for i in range(24)
        ]).arrange(RIGHT, buff=0.1)

        for i in range(24):
            label = Text(str(i), font_size=16).move_to(squares[i]).shift(DOWN * 0.3)
            if i in [7, 8, 9]:
                self.add(SurroundingRectangle(label, color=BLUE, buff=0.2))
            if i == 23:
                self.add(SurroundingRectangle(label, color=ORANGE, buff=0.2))
            squares[i].add(label)

        self.play(Create(squares), run_time=5)
        self.wait()

        pulses = []
        for i in range(24):
            if 7 <= i <= 10 or i == 23:
                pulse = AnimationGroup(
                    Indicate(squares[i], color=WHITE, scale_factor=1.2),
                    Flash(squares[i], color=WHITE, flash_radius=0.3)
                )
            else:
                pulse = AnimationGroup(
                    Indicate(squares[i], color=WHITE, scale_factor=1.2),
                )
            pulses.append(pulse)

        self.play(Succession(*pulses, lag_ratio=0.1), run_time=20)
        self.wait()