from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # 1. Title and Formula
        title = Text("Opponent Abstraction", font_size=36).to_edge(UP)
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").next_to(title, DOWN)
        self.play(Write(title), Write(formula))
        self.wait(1)

        # 2. 2-PLAYER BOARD REPRESENTATION
        # Representing the channels visually
        p2_label = Text("2-Player Representation", font_size=24).shift(UP * 1.5)
        blue_square = Square(side_length=1.5, fill_opacity=0.8, color=BLUE)
        red_square = Square(side_length=1.5, fill_opacity=0.8, color=RED).shift(RIGHT * 2)
        two_player_group = VGroup(blue_square, red_square).center().shift(UP * 0.5)
        
        self.play(FadeIn(p2_label), FadeIn(two_player_group))
        self.wait(1)

        # 3. 6-PLAYER BOARD REPRESENTATION
        # Instead of 1 red square, show 5 different colored squares
        p6_label = Text("6-Player Representation", font_size=24).move_to(p2_label)
        opponent_colors = [RED, GREEN, PURPLE, ORANGE, YELLOW]
        five_opponents = VGroup(*[
            Square(side_length=0.6, fill_opacity=0.8, color=c) for c in opponent_colors
        ]).arrange(RIGHT, buff=0.1).move_to(red_square.get_center())

        self.play(
            FadeOut(p2_label),
            FadeIn(p6_label),
            ReplacementTransform(red_square, five_opponents)
        )
        self.wait(1)

        # 4. CROSS-OUT ANIMATION
        # Create crosses manually using lines to ensure compatibility
        crosses = VGroup()
        for obj in five_opponents:
            c = VGroup(
                Line(obj.get_corner(UL), obj.get_corner(DR), color=WHITE, stroke_width=4),
                Line(obj.get_corner(UR), obj.get_corner(DL), color=WHITE, stroke_width=4)
            )
            crosses.add(c)
        
        self.play(Create(crosses))
        self.wait(1)

        # 5. MERGING INTO UNIFIED LAYER
        # Merge the 5 identities back into a single "Opponent Layer" (Red)
        unified_opp_layer = Square(side_length=1.5, fill_opacity=0.8, color=RED).move_to(five_opponents.get_center())
        unified_label = Text("Unified Opponent Layer", font_size=24, color=RED).next_to(unified_opp_layer, DOWN)

        self.play(
            FadeOut(crosses),
            ReplacementTransform(five_opponents, unified_opp_layer),
            FadeOut(p6_label),
            Write(unified_label)
        )
        
        # 6. CHECK MARK
        # Create a check mark manually
        check_mark = VGroup(
            Line(ORIGIN, DOWN * 0.5 + RIGHT * 0.5, color=GREEN, stroke_width=8),
            Line(DOWN * 0.5 + RIGHT * 0.5, UP * 0.5 + RIGHT * 1.5, color=GREEN, stroke_width=8)
        ).scale(0.5).move_to(unified_opp_layer.get_center())
        
        self.play(Create(check_mark))
        self.play(unified_opp_layer.animate.set_stroke(GREEN, 6))
        self.wait(2)

        # 7. FINAL STRUCTURE
        # Show how it fits the 3-layer formula: Me, Board, Opponents
        final_stack = VGroup(
            Square(side_length=1.5, fill_opacity=0.3, color=BLUE), # Me
            Square(side_length=1.5, fill_opacity=0.3, color=GREY), # Board/Environment
            unified_opp_layer.copy().set_opacity(0.3)             # Unified Field
        ).arrange(RIGHT, buff=-1.1).shift(DOWN * 1.5)
        
        layer_explanation = Text("1: Me  2: Board  3: Opponent Field", font_size=20).next_to(final_stack, DOWN)
        
        self.play(
            FadeOut(two_player_group[0]),
            FadeOut(unified_opp_layer),
            FadeOut(check_mark),
            FadeOut(unified_label),
            FadeIn(final_stack),
            FadeIn(layer_explanation)
        )
        self.wait(3)