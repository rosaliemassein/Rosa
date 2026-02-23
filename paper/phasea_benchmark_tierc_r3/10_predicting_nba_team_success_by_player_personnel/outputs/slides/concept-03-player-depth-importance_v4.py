from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # 1. Formula display
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=32
        ).to_edge(UP, buff=0.8)

        # 2. Player Icons
        # A horizontal row of 10 circles with rank numbers
        player_icons = VGroup(*[
            VGroup(
                Circle(radius=0.2, color=WHITE),
                Text(str(i+1), font_size=18)
            ) for i in range(10)
        ]).arrange(RIGHT, buff=0.4).shift(DOWN * 2.5)

        # 3. Coefficient Bars
        # Mock data based on the concept that 1st, 2nd, 5th, and 8th are most significant
        height_data = [3.5, 3.0, 1.2, 1.1, 2.2, 1.0, 0.9, 1.8, 0.6, 0.4]
        bars = VGroup()
        for i in range(10):
            bar = Rectangle(
                width=0.3,
                height=height_data[i],
                fill_opacity=0.5,
                stroke_width=2,
                color=WHITE
            )
            # Position the bar's bottom edge 0.1 units above the icon's top
            # move_to with aligned_edge=DOWN ensures the bottom is at the target point
            bar.move_to(player_icons[i].get_top() + UP * 0.1, aligned_edge=DOWN)
            bars.add(bar)

        # --- Animation sequence ---

        # 1. Show Formula and Icons
        self.play(Write(formula))
        self.play(Create(player_icons))
        self.wait(0.5)

        # 2. Animate the bars being created (simulating growth)
        self.play(Create(bars), run_time=2)
        self.wait(0.5)

        # 3. Highlight stars (1st and 2nd) with yellow color
        self.play(
            bars[0].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8),
            bars[1].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8)
        )
        self.wait(0.5)

        # 4. Highlight crucial depth positions (5th and 8th) with blue color
        # Index 4 is the 5th player, Index 7 is the 8th player
        self.play(
            bars[4].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            bars[7].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8)
        )
        
        # 5. Pulse effect for the 5th and 8th bars to emphasize importance
        self.play(Indicate(bars[4], color=BLUE))
        self.play(Indicate(bars[7], color=BLUE))

        # 6. Conclusion text based on the voiceover concept
        summary = Text(
            "Depth is just as measurable as stardom",
            font_size=24
        ).next_to(player_icons, DOWN, buff=0.5)
        
        self.play(FadeIn(summary))
        self.wait(2)