from manim import *

class Concept02OpponentAbstraction(Scene):
    def construct(self):
        # 1. Setup Colors and Basic UI
        # Using standard colors and hex to avoid potential "PINK" or specific color naming errors
        c_me = BLUE
        c_opp_unified = RED
        c_others = [RED, YELLOW, GREEN, ORANGE, PURPLE]
        
        title = Text("Opponent Abstraction", font_size=36).to_edge(UP)
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").to_edge(DOWN)
        
        # Helper to create a grid layer
        def get_layer(color, opacity=0.6):
            return VGroup(*[
                Square(side_length=0.4, fill_color=color, fill_opacity=opacity, stroke_width=1)
                for _ in range(9)
            ]).arrange_in_grid(rows=3, cols=3, buff=0.05)

        # 2. 2-Player Representation (Left side of screen)
        label_2p = Text("2-Player Game", font_size=20).shift(LEFT * 3.5 + DOWN * 1.5)
        # We stack them slightly offset for a 3D effect
        me_2p = get_layer(c_me).shift(LEFT * 3.5 + UP * 0.5)
        opp_2p = get_layer(c_opp_unified).shift(LEFT * 3.3 + UP * 0.7)
        # Background/Metadata layer to represent the '3' in the formula
        bg_2p = get_layer(WHITE, opacity=0.1).shift(LEFT * 3.7 + UP * 0.3)
        
        self.play(Write(title))
        self.play(FadeIn(bg_2p), Create(me_2p), Create(opp_2p))
        self.play(Write(label_2p))
        self.wait(0.5)

        # 3. 6-Player Representation (Right side of screen)
        label_6p = Text("6-Player Game", font_size=20).shift(RIGHT * 2.5 + DOWN * 1.5)
        bg_6p = get_layer(WHITE, opacity=0.1).shift(RIGHT * 1.8 + UP * 0.3)
        me_6p = get_layer(c_me).shift(RIGHT * 2.0 + UP * 0.5)
        
        # 5 distinct opponent layers
        opp_layers_6p = VGroup()
        for i, color in enumerate(c_others):
            layer = get_layer(color).shift(RIGHT * (2.2 + i * 0.2) + UP * (0.7 + i * 0.2))
            opp_layers_6p.add(layer)
            
        self.play(FadeIn(bg_6p), Create(me_6p))
        self.play(AnimationGroup(*[Create(l) for l in opp_layers_6p], lag_ratio=0.1))
        self.play(Write(label_6p))
        self.wait(1)

        # 4. Cross-out animation (Manual Crosses for robustness)
        crosses = VGroup()
        for layer in opp_layers_6p:
            cross_lines = VGroup(
                Line(layer.get_corner(UL), layer.get_corner(DR), color=WHITE, stroke_width=2),
                Line(layer.get_corner(UR), layer.get_corner(DL), color=WHITE, stroke_width=2)
            )
            crosses.add(cross_lines)
        
        self.play(Create(crosses))
        self.wait(0.5)

        # 5. Merge opponents into a single 'Opponent Layer'
        # Target unified layer (The Red intensity layer)
        unified_opp_layer = get_layer(RED, opacity=0.9).move_to(opp_layers_6p[0].get_center())
        
        self.play(
            FadeOut(crosses),
            FadeOut(opp_layers_6p[1:]),
            opp_layers_6p[0].animate.become(unified_opp_layer),
            run_time=2
        )
        
        # 6. Check Mark animation (Manual lines)
        c_line1 = Line(LEFT * 0.2 + DOWN * 0.1, ORIGIN, color=GREEN, stroke_width=6)
        c_line2 = Line(ORIGIN, RIGHT * 0.4 + UP * 0.5, color=GREEN, stroke_width=6)
        check_mark = VGroup(c_line1, c_line2).move_to(unified_opp_layer.get_center())
        
        self.play(Create(check_mark))
        self.wait(0.5)

        # 7. Formula and final narration
        self.play(Write(formula))
        
        voice_caption = Text(
            "Me vs. The Field: Strategy naturally scales.",
            font_size=22,
            color=GRAY_A
        ).next_to(formula, UP)
        
        self.play(Write(voice_caption))
        self.play(Indicate(me_6p), Indicate(opp_layers_6p[0]))
        self.wait(3)