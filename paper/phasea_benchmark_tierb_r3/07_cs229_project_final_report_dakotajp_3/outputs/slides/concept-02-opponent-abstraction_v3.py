from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup and Formula
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}", color=YELLOW).to_edge(UP)
        self.play(Write(formula))
        self.wait(0.5)

        # Helper to create a grid layer
        def create_grid(color, opacity=0.6):
            return VGroup(*[
                Square(side_length=0.3, fill_color=color, fill_opacity=opacity, stroke_width=1)
                for _ in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.05)

        # 2. 2-Player Representation
        # Layers: Me (Blue), Opponent (Red), Constants (Gray)
        me_2p = create_grid(BLUE).shift(LEFT * 3 + UP * 0.5)
        opp_2p = create_grid(RED).shift(LEFT * 2.8 + UP * 0.3)
        const_2p = create_grid(GREY).shift(LEFT * 2.6 + UP * 0.1)
        
        label_2p = Text("2-Player Mode", font_size=24).next_to(const_2p, DOWN, buff=0.5)
        group_2p = VGroup(me_2p, opp_2p, const_2p, label_2p)
        
        self.play(FadeIn(group_2p))
        self.wait(1)

        # 3. 6-Player Naive Representation
        # 5 different opponent colors
        opp_colors = ["#FF0000", "#FF69B4", "#FFA500", "#800000", "#A52A2A"]
        me_6p = create_grid(BLUE).shift(RIGHT * 1.5 + UP * 0.5)
        
        opp_layers_6p = VGroup()
        for i, color in enumerate(opp_colors):
            layer = create_grid(color).shift(RIGHT * (1.7 + i * 0.15) + UP * (0.3 - i * 0.15))
            opp_layers_6p.add(layer)
        
        const_6p = create_grid(GREY).shift(RIGHT * (1.7 + 5 * 0.15) + UP * (0.3 - 5 * 0.15))
        label_6p = Text("6-Player (Individual)", font_size=24).next_to(opp_layers_6p, DOWN, buff=0.8)

        self.play(FadeIn(me_6p), FadeIn(opp_layers_6p), FadeIn(const_6p), Write(label_6p))
        self.wait(1)

        # 4. Cross-out individual identities
        # Manual Cross implementation to avoid undefined identifier
        crosses = VGroup()
        for layer in opp_layers_6p:
            c = VGroup(
                Line(layer.get_corner(UL), layer.get_corner(DR), color=WHITE, stroke_width=3),
                Line(layer.get_corner(UR), layer.get_corner(DL), color=WHITE, stroke_width=3)
            )
            crosses.add(c)
        
        self.play(Create(crosses))
        self.wait(1)

        # 5. Merging into a single "Red" intensity (Opponent Layer)
        unified_opp_layer = create_grid(RED, opacity=0.9).move_to(opp_layers_6p[2])
        unified_label = Text("Unified Opponent Layer", font_size=24, color=RED).next_to(unified_opp_layer, DOWN, buff=0.5)
        # Success checkmark using MathTex
        check_mark = MathTex(r"\checkmark", color=GREEN).scale(1.5).next_to(unified_label, RIGHT)

        self.play(
            FadeOut(crosses),
            FadeOut(opp_layers_6p),
            FadeOut(label_6p),
            FadeIn(unified_opp_layer),
            Write(unified_label)
        )
        self.play(Write(check_mark))
        self.wait(1)

        # 6. Final Abstraction: Pointing out identical structures
        rect_2p = SurroundingRectangle(VGroup(me_2p, opp_2p, const_2p), color=YELLOW, buff=0.2)
        rect_6p = SurroundingRectangle(VGroup(me_6p, unified_opp_layer, const_6p), color=YELLOW, buff=0.2)
        
        identical_text = Text("Structurally Identical (3 Layers)", font_size=30, color=YELLOW).to_edge(DOWN)
        
        self.play(
            Create(rect_2p),
            Create(rect_6p),
            Write(identical_text)
        )
        
        # Highlight the '3' in the formula one last time
        self.play(Indicate(formula))
        self.wait(3)