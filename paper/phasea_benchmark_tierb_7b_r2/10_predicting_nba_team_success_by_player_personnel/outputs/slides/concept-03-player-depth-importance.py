from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # Create player icons and labels
        players = [Text(f"{i}th Player").scale(0.5) for i in range(1, 11)]
        player_icons = [Circle(radius=0.3).set_color(WHITE) for _ in range(10)]
        player_icons = VGroup(*player_icons).arrange(DOWN, buff=0.8)
        player_labels = VGroup(*players).arrange(DOWN, buff=0.8)

        # Create bars for Average Coefficient
        bar_heights = [1, 2, 0.5, 1.5, 2.5, 1.8, 2.3, 2.1, 1.7, 0.9]
        bars = [Rectangle(height=h, width=0.5) for h in bar_heights]
        bars = VGroup(*bars).arrange(DOWN, buff=0.8).next_to(player_icons, RIGHT)

        # Highlight the 1st and 2nd bars with a bright gold glow
        self.play(FadeIn(player_icons), FadeIn(player_labels), Create(bars))
        self.wait(0.5)
        highlighted_bars = bars[:2]
        highlighted_bars.set_color(GOLD).shine_in_direction(RIGHT)
        self.play(VGroup(bars).animate.shift(RIGHT * 1.5))
        self.wait(0.5)

        # Highlight the 5th and 8th bars with a pulsing blue light
        self.play(LaggedStart(*[Indicate(bar, color=BLUE) for bar in bars[4:8]]))
        self.wait(2)