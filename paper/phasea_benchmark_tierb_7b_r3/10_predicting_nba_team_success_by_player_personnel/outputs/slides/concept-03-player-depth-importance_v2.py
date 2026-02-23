from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # Create player icons and coefficient bars
        players = [Text(f"{i+1}") for i in range(10)]
        bars = [Rectangle(height=i/2, width=0.5) for i in range(10)]

        # Position players and bars
        players = VGroup(*players).arrange(RIGHT, buff=1)
        bars = VGroup(*bars).arrange(RIGHT, buff=1)

        for bar in bars:
            bar.set_color(GREY)

        # Animate bars growing to their respective heights
        for bar, player in zip(bars, players):
            self.play(Create(bar), Write(player))

        # Highlight 1st and 2nd bars with bright gold glow
        self.play(FadeIn(bars[0].set_color(GOLD)), FadeIn(players[0].set_color(GOLD)))
        self.play(FadeIn(bars[1].set_color(GOLD)), FadeIn(players[1].set_color(GOLD)))

        # Highlight 5th and 8th bars with pulsing blue light
        self.play(FadeIn(bars[4].set_color(BLUE), run_time=1))
        self.play(FadeIn(bars[7].set_color(BLUE), run_time=1))
        self.play(bars[4].animate.scale(1.2).scale(0.8, about_point=bars[4].get_center()).wait(1), 
                  bars[7].animate.scale(1.2).scale(0.8, about_point=bars[7].get_center()).wait(1))

        # Indicate the non-linear relationship
        self.play(Create(Text("Wins ≈ β1(1st PIE) + β5(5th PIE) + ... + β8(8th PIE)").next_to(bars, DOWN)))