from manim import *

class Concept03PlayerDepthImportance(Scene):
    def construct(self):
        # 1. Formula reference from the prompt
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=32
        ).to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. Create 10 basketball player icons (represented as simple geometric groups)
        players = VGroup(*[
            VGroup(
                Circle(radius=0.15, color=WHITE, fill_opacity=0.2),
                Line(ORIGIN, DOWN * 0.2, color=WHITE).shift(DOWN * 0.15)
            ) for _ in range(10)
        ]).arrange(RIGHT, buff=0.5).shift(DOWN * 2.5)

        labels = VGroup(*[
            Text(str(i+1), font_size=18).next_to(players[i], DOWN, buff=0.1)
            for i in range(10)
        ])
        self.add(players, labels)

        # 3. Create vertical bars representing 'Average Coefficient'
        # Heights are set to visualize the hierarchy (high for stars, specific peaks for 5 and 8)
        heights = [3.4, 2.7, 1.1, 1.0, 2.2, 0.8, 0.7, 1.8, 0.5, 0.4]
        bars = VGroup()
        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.3, 
                height=h, 
                color=PURPLE, 
                fill_opacity=0.6,
                stroke_width=1
            )
            # Position the bottom of the bar just above the player icon
            bar.move_to(players[i].get_top() + UP * (h/2 + 0.1))
            bars.add(bar)

        # Animate bars growing
        self.play(Create(bars), run_time=2)
        self.wait(1)

        # 4. Highlight the Stars (1st and 2nd bars) with a gold glow
        star_bars = VGroup(bars[0], bars[1])
        self.play(
            star_bars.animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.8),
            run_time=1
        )
        self.play(Indicate(star_bars, color=YELLOW, scale_factor=1.1))
        self.wait(0.5)

        # 5. Highlight the 5th and 8th bars with pulsing blue light
        # Using indices 4 and 7 for the 5th and 8th players
        depth_bars = VGroup(bars[4], bars[7])
        self.play(
            depth_bars.animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            run_time=1
        )
        
        # Manual pulse animation
        for _ in range(2):
            self.play(depth_bars.animate.scale(1.2), run_time=0.4)
            self.play(depth_bars.animate.scale(1/1.2), run_time=0.4)

        # 6. Conclusion text based on the voiceover concept
        conclusion = Text(
            "Depth is just as measurable as stardom.",
            font_size=24,
            color=BLUE
        ).next_to(formula, DOWN, buff=0.4)
        
        self.play(Write(conclusion))
        self.wait(2)