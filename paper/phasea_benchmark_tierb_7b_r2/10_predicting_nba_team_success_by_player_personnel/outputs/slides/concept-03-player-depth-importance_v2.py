from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # Create player icons and average coefficient bars
        players = [Text(f"Player {i}") for i in range(1, 11)]
        bars = [Rectangle(height=(i+2)/2, width=0.5) for i in range(10)]
        labels = [MathTex(rf"\beta_{i+1}(\\text{{PIE}})").scale(0.5) for i in range(9)]

        # Position players and bars
        for player, bar, label in zip(players, bars, labels):
            player.shift(LEFT * 3 + DOWN * (i / 2))
            bar.next_to(player, UP)
            label.next_to(bar, LEFT)

        # Draw players and bars
        self.play(FadeIn(VGroup(*players)), FadeIn(VGroup(*bars)))
        self.wait(1)

        # Highlight star players with gold glow
        stars = [Indicate(bars[i], color=GOLD) for i in [0, 1]]
        self.play(LaggedStart(*stars))
        self.wait(1)

        # Highlight depth players with pulsing blue light
        depth_players = [Indicate(bars[i], color=BLUE) for i in [4, 7]]
        self.play(LaggedStart(*depth_players))
        self.wait(1)