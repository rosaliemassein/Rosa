from manim import *

class Concept02OpponentAbstraction(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").to_edge(UP)
        self.play(Write(formula))

        # 2. 2-Player Board Representation
        # Me (Blue) vs Opponent (Red)
        p1_label = Text("Me", font_size=24).set_color(BLUE)
        p2_label = Text("Opponent", font_size=24).set_color(RED)
        
        board_2p = VGroup(
            Square(side_length=1, fill_opacity=1, color=BLUE),
            Square(side_length=1, fill_opacity=1, color=RED)
        ).arrange(RIGHT, buff=0.5)
        
        labels_2p = VGroup(p1_label, p2_label)
        for i, label in enumerate(labels_2p):
            label.next_to(board_2p[i], DOWN)

        title_2p = Text("2-Player Representation", font_size=32).next_to(board_2p, UP, buff=0.5)
        
        self.play(Create(board_2p), Write(labels_2p), Write(title_2p))
        self.wait(2)

        # 3. Transition to 6-Player Board
        # 1 Me (Blue) + 5 Opponents (Distinct colors)
        opponent_colors = [RED, GREEN, YELLOW, ORANGE, PURPLE]
        
        board_6p = VGroup(
            Square(side_length=0.8, fill_opacity=1, color=BLUE),
            *[Square(side_length=0.8, fill_opacity=1, color=c) for c in opponent_colors]
        ).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        
        title_6p = Text("6-Player Board (Individual Channels)", font_size=32).next_to(board_6p, UP, buff=0.5)

        self.play(
            FadeOut(board_2p, labels_2p, title_2p),
            FadeIn(board_6p),
            Write(title_6p)
        )
        self.wait(1.5)

        # 4. Merging into 'Opponent Layer'
        # Group the 5 opponents (index 1 to 5)
        opponents_group = board_6p[1:]
        
        # Cross-out animation over individual identities (Manual replacement for Cross)
        crosses = VGroup()
        for sq in opponents_group:
            cross = VGroup(
                Line(sq.get_corner(UL), sq.get_corner(DR), color=RED, stroke_width=6),
                Line(sq.get_corner(UR), sq.get_corner(DL), color=RED, stroke_width=6)
            )
            crosses.add(cross)
            
        self.play(Create(crosses))
        self.wait(0.5)

        # Animate merging colors into a single 'Red' intensity
        unified_opponent_layer = Square(side_length=0.8, fill_opacity=1, color=RED).move_to(opponents_group.get_center())
        unified_label = Text("Opponent Layer", font_size=24, color=RED).next_to(unified_opponent_layer, DOWN)
        
        # Checkmark
        check = Text("✔", color=GREEN).scale(1.5).next_to(unified_opponent_layer, UP)

        self.play(
            opponents_group.animate.set_color(RED),
            FadeOut(crosses)
        )
        self.play(
            ReplacementTransform(opponents_group, unified_opponent_layer),
            Write(unified_label),
            Write(check),
            title_6p.animate.become(Text("Unified 'Opponent Layer' Abstraction", font_size=32).next_to(board_6p[0], UP).shift(RIGHT * 1.5))
        )
        
        # Show final state: Blue (Me) vs Red (Unified Field)
        final_group = VGroup(board_6p[0], unified_opponent_layer)
        self.play(final_group.animate.arrange(RIGHT, buff=1).move_to(ORIGIN))
        
        me_label = Text("Me", font_size=24, color=BLUE).next_to(board_6p[0], DOWN)
        unified_label.next_to(unified_opponent_layer, DOWN)
        check.next_to(unified_opponent_layer, UP)
        
        self.play(Write(me_label))
        self.wait(3)