from manim import *

class Concept03PlayerDepthImportance(Scene):
    def construct(self):
        # 1. Create Layout and Data
        # Coefficients based on the narrative: 1st/2nd high, 5th/8th local peaks
        heights = [3.5, 2.8, 1.5, 1.2, 2.2, 1.4, 1.1, 1.8, 0.8, 0.5]
        
        # Player Icons (Circles with numbers)
        player_group = VGroup()
        bars = VGroup()
        
        for i in range(10):
            # Player Icon
            icon = VGroup(
                Circle(radius=0.3, color=WHITE, fill_opacity=0.2),
                Text(str(i+1), font_size=20)
            )
            icon.move_to(RIGHT * (i - 4.5) * 1.2 + DOWN * 2.5)
            player_group.add(icon)
            
            # Vertical Bar (Coefficient)
            bar = Rectangle(
                width=0.6, 
                height=0.01, 
                fill_color=WHITE, 
                fill_opacity=0.8, 
                stroke_width=1
            )
            bar.next_to(icon, UP, buff=0.2)
            bar.align_to(icon, DOWN).shift(UP * 0.7)
            bars.add(bar)

        # 2. Formula Reference
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=32
        ).to_edge(UP, buff=0.5)

        # 3. Animation: Growing Bars
        self.play(Create(player_group), Write(formula))
        self.wait(0.5)
        
        # Growing bars to their respective heights
        grow_animations = []
        for i, bar in enumerate(bars):
            # Calculate new height and shift it so the bottom stays in place
            target_height = heights[i]
            grow_animations.append(
                bar.animate.stretch_to_fit_height(target_height).move_to(
                    player_group[i].get_top() + UP * (target_height / 2 + 0.2)
                )
            )
        
        self.play(*grow_animations, run_time=2)
        self.wait(1)

        # 4. Highlight the "Stars" (1st and 2nd)
        self.play(
            bars[0].animate.set_color(GOLD),
            bars[1].animate.set_color(GOLD)
        )
        
        gold_glow1 = bars[0].copy().set_stroke(GOLD, 10).set_opacity(0.3)
        gold_glow2 = bars[1].copy().set_stroke(GOLD, 10).set_opacity(0.3)
        
        self.play(FadeIn(gold_glow1), FadeIn(gold_glow2))
        self.play(
            Indicate(bars[0], color=GOLD, scale_factor=1.05),
            Indicate(bars[1], color=GOLD, scale_factor=1.05)
        )
        self.wait(1)

        # 5. Highlight the depth (5th and 8th) with pulse
        depth_indices = [4, 7] # 5th and 8th player
        
        self.play(
            *[bars[i].animate.set_color(BLUE) for i in depth_indices]
        )
        
        # Pulsing effect
        for _ in range(2):
            self.play(
                *[Indicate(bars[i], color=BLUE, scale_factor=1.2) for i in depth_indices],
                run_time=1
            )

        # 6. Conclusion Text
        narration_text = Text(
            "Depth is just as measurable as stardom.",
            font_size=28,
            color=BLUE
        ).next_to(player_group, DOWN, buff=0.5)
        
        self.play(Write(narration_text))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(player_group), 
            FadeOut(bars), 
            FadeOut(formula), 
            FadeOut(narration_text), 
            FadeOut(gold_glow1), 
            FadeOut(gold_glow2)
        )
        self.wait()