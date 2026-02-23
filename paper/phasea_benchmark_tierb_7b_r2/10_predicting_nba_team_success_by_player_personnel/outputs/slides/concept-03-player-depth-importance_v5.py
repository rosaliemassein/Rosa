from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # 1. Create 10 player icons (Circles)
        players = VGroup(*[
            Circle(radius=0.15, color=BLUE, fill_opacity=0.7) 
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.5).shift(DOWN * 1.5)
        
        player_labels = VGroup(*[
            Text(str(i + 1), font_size=24).next_to(players[i], DOWN) 
            for i in range(10)
        ])
        
        self.play(Create(players), Write(player_labels))
        self.wait(0.5)

        # 2. Average Coefficient bars
        # Representing relative weights (1st/2nd high, 5th and 8th also significant)
        bar_heights = [3.5, 3.0, 1.2, 1.1, 2.2, 0.9, 0.8, 1.8, 0.6, 0.5]
        bars = VGroup()
        for i in range(10):
            bar = Rectangle(
                width=0.4, 
                height=bar_heights[i], 
                color=WHITE, 
                fill_opacity=0.5
            )
            bar.next_to(players[i], UP, buff=0.1)
            # Set initial state for growth animation (very small height)
            bar.scale(0.01, about_edge=DOWN)
            bars.add(bar)

        # Animation: Bars growing to their respective heights
        self.play(
            LaggedStart(
                *[bar.animate.scale(100, about_edge=DOWN) for bar in bars],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait(0.5)

        # 3. Highlight 1st and 2nd bars (The Stars) with Gold/Yellow
        self.play(
            bars[0].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8),
            bars[1].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8)
        )
        self.play(
            Indicate(bars[0], color=YELLOW), 
            Indicate(bars[1], color=YELLOW)
        )
        self.wait(0.5)

        # 4. Highlight 5th and 8th bars with Blue pulsing (The crucial depth players)
        # Using index 4 for 5th and index 7 for 8th player
        self.play(
            bars[4].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            bars[7].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8)
        )
        
        # Pulse effect (Scale up and down)
        for _ in range(2):
            self.play(
                bars[4].animate.scale(1.2, about_edge=DOWN),
                bars[7].animate.scale(1.2, about_edge=DOWN),
                run_time=0.4
            )
            self.play(
                bars[4].animate.scale(1/1.2, about_edge=DOWN),
                bars[7].animate.scale(1/1.2, about_edge=DOWN),
                run_time=0.4
            )
        self.wait(0.5)

        # 5. Formula display at the top
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=36
        ).to_edge(UP, buff=0.8)
        
        self.play(Write(formula))
        self.wait(2)