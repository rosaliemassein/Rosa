from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # Create player icons
        players = VGroup(*[Circle(radius=0.2) for _ in range(1, 11)]).arrange(RIGHT, buff=0.5)
        players.shift(LEFT * 3)

        # Create vertical bars for coefficients
        bar_heights = [2, 1.5, 1, 0.8, 1.2, 0.9, 1.1, 1.3, 0.7, 1.4]  # Example heights
        bars = VGroup(*[Rectangle(height=h, width=0.2).next_to(player, UP) for h, player in zip(bar_heights, players)])
        bars.shift(UP * 2)

        # Create labels for player ranks
        labels = VGroup(*[Text(f"{i}").next_to(player, DOWN) for i, player in enumerate(range(1, 11), start=1)]).scale(0.7)
        labels.shift(RIGHT * 3)

        # Animate bars growing to their heights
        for bar in bars:
            self.play(bar.animate.set_height(bar.height), run_time=1)

        # Highlight 1st and 2nd bars with gold glow
        stars = [bar for bar in bars[:2]]
        for star in stars:
            self.play(FadeIn(star.set_color(GOLD)), run_time=0.5)

        # Highlight 5th and 8th bars with pulsing blue light
        depth_positions = [bars[4], bars[7]]
        for pos in depth_positions:
            self.play(Indicate(pos, color=BLUE, scale_factor=1.2), run_time=1)
            self.play(Indicate(pos, color=BLUE, scale_factor=0.8), run_time=1)
            self.play(Indicate(pos, color=BLUE, scale_factor=1.2), run_time=1)

        # Add formula
        formula = MathTex(r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})").next_to(labels, DOWN * 2)
        self.play(Write(formula), run_time=2)

        self.wait(3)