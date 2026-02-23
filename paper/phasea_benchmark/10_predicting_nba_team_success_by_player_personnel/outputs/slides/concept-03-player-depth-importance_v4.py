from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Header Formula
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=36
        ).to_edge(UP, buff=0.5)

        # 2. Create Player Icons and Labels
        player_icons = VGroup()
        labels = VGroup()
        for i in range(1, 11):
            # Create a simple representation of a basketball player icon (circle + cross)
            circ = Circle(radius=0.25, color=WHITE)
            l1 = Line(circ.get_top(), circ.get_bottom(), stroke_width=1)
            l2 = Line(circ.get_left(), circ.get_right(), stroke_width=1)
            icon = VGroup(circ, l1, l2)
            
            # Create labels (1st, 2nd, 3rd, etc.)
            suffix = "th"
            if i == 1: suffix = "st"
            elif i == 2: suffix = "nd"
            elif i == 3: suffix = "rd"
            label = Text(f"{i}{suffix}", font_size=18)
            
            player_icons.add(icon)
            labels.add(label)

        player_icons.arrange(RIGHT, buff=0.4).shift(DOWN * 1)
        for i in range(10):
            labels[i].next_to(player_icons[i], DOWN, buff=0.2)

        # 3. Create Coefficient Bars
        # Heights reflecting the prompt's finding (1st, 2nd strong, 5th and 8th surprisingly high)
        heights = [3.5, 3.0, 1.2, 1.0, 2.5, 1.1, 0.8, 2.0, 0.6, 0.4]
        bars = VGroup()
        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.4, 
                height=h, 
                fill_opacity=0.6, 
                stroke_width=1, 
                color=WHITE
            )
            bar.next_to(player_icons[i], UP, buff=0)
            bars.add(bar)

        # 4. Animation Sequence
        self.play(Write(formula))
        self.wait(0.3)
        self.play(
            Create(player_icons),
            FadeIn(labels, shift=UP),
            run_time=1.5
        )

        # Animate bars growing (using FadeIn with shift as a fallback for GrowFromEdge)
        self.play(
            LaggedStart(*[
                FadeIn(bar, shift=UP) for bar in bars
            ], lag_ratio=0.1),
            run_time=2
        )
        self.wait(1)

        # Highlight 1st and 2nd (Stars) with Gold
        self.play(
            bars[0].animate.set_color(GOLD).set_fill(GOLD, opacity=0.8),
            bars[1].animate.set_color(GOLD).set_fill(GOLD, opacity=0.8),
        )
        self.play(Indicate(bars[0], color=GOLD), Indicate(bars[1], color=GOLD))
        self.wait(0.5)

        # Highlight 5th and 8th (Crucial Depth) with Pulsing Blue
        self.play(
            bars[4].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            bars[7].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
        )
        # Pulse effect
        for _ in range(2):
            self.play(
                Indicate(bars[4], scale_factor=1.2, color=BLUE),
                Indicate(bars[7], scale_factor=1.2, color=BLUE),
                run_time=0.8
            )

        # 5. Narration Text
        narration_str = "A team's floor is set by its 5th starter and final rotation player."
        narration = Text(narration_str, font_size=22, color=GREEN).to_edge(DOWN, buff=0.4)
        self.play(Write(narration))
        self.wait(3)