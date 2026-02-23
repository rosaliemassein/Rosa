from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        # Define colors via hex to avoid undefined identifier errors
        COLOR_TEAL = "#008080"
        COLOR_GOLD = "#FFD700"
        COLOR_BLUE = "#0000FF"
        COLOR_WHITE = "#FFFFFF"

        # 1. Formula Display
        formula = MathTex(
            r"\text{Wins} \approx \beta_1(\text{1st\_PIE}) + \beta_5(\text{5th\_PIE}) + \dots + \beta_8(\text{8th\_PIE})",
            font_size=36
        ).to_edge(UP, buff=0.5)
        
        # 2. Player Icons (Representing 1st through 10th man)
        player_icons = VGroup()
        for i in range(10):
            head = Circle(radius=0.15, color=COLOR_WHITE)
            body = Rectangle(width=0.4, height=0.4, color=COLOR_WHITE).set_fill(COLOR_WHITE, opacity=1)
            body.next_to(head, DOWN, buff=0.05)
            player = VGroup(head, body)
            player_icons.add(player)
            
        player_icons.arrange(RIGHT, buff=0.5).shift(DOWN * 2.5)
        
        labels = VGroup(*[
            Text(f"{i+1}", font_size=20).next_to(player_icons[i], DOWN, buff=0.2)
            for i in range(10)
        ])

        # 3. Vertical Bars
        height_values = [3.2, 2.0, 0.8, 0.6, 1.8, 0.7, 0.5, 1.4, 0.4, 0.3]
        bars = VGroup()
        for i, h in enumerate(height_values):
            bar = Rectangle(
                width=0.4,
                height=h,
                fill_color=COLOR_TEAL,
                fill_opacity=0.7,
                stroke_color=COLOR_WHITE,
                stroke_width=1
            )
            bar.next_to(player_icons[i], UP, buff=0.1)
            bar.align_to(player_icons[i], DOWN).shift(UP * 0.7) # Aligning base to top of icon area
            bars.add(bar)

        # 4. Animation Sequence
        self.play(Write(formula))
        self.play(FadeIn(player_icons), Write(labels))
        self.wait(0.5)

        # Bars growing
        self.play(
            *[Create(bar) for bar in bars],
            run_time=2
        )
        self.wait(1)

        # Highlight 1st and 2nd (Stars)
        star_indices = [0, 1]
        stars_glow = VGroup(*[
            SurroundingRectangle(bars[i], color=COLOR_GOLD, buff=0.1)
            for i in star_indices
        ])
        
        self.play(
            Create(stars_glow),
            *[bars[i].animate.set_fill(COLOR_GOLD) for i in star_indices]
        )
        self.play(
            *[Indicate(bars[i], color=COLOR_GOLD) for i in star_indices]
        )
        self.wait(1)

        # Highlight 5th and 8th (Depth)
        depth_indices = [4, 7] 
        
        self.play(
            *[bars[i].animate.set_fill(COLOR_BLUE) for i in depth_indices],
            *[bars[i].animate.set_stroke(COLOR_BLUE, width=4) for i in depth_indices]
        )

        # Pulsing effect for 5th and 8th
        for _ in range(2):
            self.play(
                *[Indicate(bars[i], color=COLOR_BLUE, scale_factor=1.2) for i in depth_indices],
                run_time=0.8
            )

        # Voice/Text summary as requested in idea
        voice_text = Text(
            "The 5th and 8th players are crucial depth positions.",
            font_size=24,
            color=COLOR_BLUE
        ).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(voice_text))
        self.play(
            Indicate(bars[4], scale_factor=1.4, color=COLOR_BLUE),
            Indicate(bars[7], scale_factor=1.4, color=COLOR_BLUE),
            run_time=2
        )
        
        self.wait(3)