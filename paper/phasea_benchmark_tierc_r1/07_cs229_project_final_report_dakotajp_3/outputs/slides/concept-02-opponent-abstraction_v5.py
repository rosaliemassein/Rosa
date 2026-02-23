from manim import *

class Concept02OpponentAbstraction(Scene):
    def construct(self):
        # 1. Formula Display
        # Reference formula: S in B^{n x n x 3}
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").to_edge(UP)
        self.play(Write(formula))
        self.wait(0.5)

        # 2. Colors and Configuration
        # Avoid PINK to ensure compatibility, using standard colors and hex
        ME_COLOR = BLUE
        OPP_UNIFIED_COLOR = RED
        INDIVIDUAL_COLORS = [RED, YELLOW, GREEN, ORANGE, PURPLE]
        
        # 3. Create 2-Player Representation
        # Grid on the left
        grid_2p = VGroup(*[Square(side_length=0.7) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.1)
        grid_2p.shift(LEFT * 3)
        label_2p = Text("2-Player Game", font_size=20).next_to(grid_2p, UP)
        
        # Two distinct colors: Blue (Me) vs Red (Opponent)
        me_2p = VGroup(
            self.make_piece(grid_2p[4], ME_COLOR),
            self.make_piece(grid_2p[0], ME_COLOR)
        )
        opp_2p = VGroup(
            self.make_piece(grid_2p[2], OPP_UNIFIED_COLOR),
            self.make_piece(grid_2p[8], OPP_UNIFIED_COLOR)
        )
        
        self.play(Create(grid_2p), Write(label_2p))
        self.play(FadeIn(me_2p), FadeIn(opp_2p))
        self.wait(1)

        # 4. Create 6-Player Representation
        # Grid on the right
        grid_6p = VGroup(*[Square(side_length=0.7) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.1)
        grid_6p.shift(RIGHT * 3)
        label_6p = Text("6-Player Game", font_size=20).next_to(grid_6p, UP)
        
        me_6p = self.make_piece(grid_6p[4], ME_COLOR)
        
        # 5 different opponent colors
        opp_indices = [0, 1, 2, 6, 8]
        opps_6p = VGroup(*[
            self.make_piece(grid_6p[idx], INDIVIDUAL_COLORS[i])
            for i, idx in enumerate(opp_indices)
        ])
        
        self.play(Create(grid_6p), Write(label_6p))
        self.play(FadeIn(me_6p), FadeIn(opps_6p))
        self.wait(1)

        # 5. Cross-out animation over individual identities
        # Manually create Cross to avoid potential identifier errors
        crosses = VGroup()
        for piece in opps_6p:
            p1, p2 = piece.get_corner(UL), piece.get_corner(DR)
            p3, p4 = piece.get_corner(UR), piece.get_corner(DL)
            crosses.add(VGroup(Line(p1, p2, color=WHITE), Line(p3, p4, color=WHITE)))
        
        self.play(Create(crosses))
        self.wait(1)

        # 6. Merge opponent colors into a single 'Red' intensity
        # This represents the "opponent layer" abstraction
        unified_opps_6p = VGroup(*[
            self.make_piece(grid_6p[idx], OPP_UNIFIED_COLOR)
            for idx in opp_indices
        ])
        
        self.play(
            FadeOut(crosses),
            ReplacementTransform(opps_6p, unified_opps_6p),
            run_time=2
        )
        
        # 7. Check mark over unified layer
        # Manual check mark to be safe
        check_mark = VGroup(
            Line(ORIGIN, 0.4 * DOWN + 0.4 * RIGHT),
            Line(0.4 * DOWN + 0.4 * RIGHT, 1.0 * UP + 1.0 * RIGHT)
        ).set_color(GREEN).scale(0.4).next_to(grid_6p, RIGHT)
        
        self.play(Create(check_mark))
        
        # 8. Final narration label
        abstraction_label = Text("Unified 'Opponent Layer'", font_size=24, color=RED).to_edge(DOWN)
        self.play(Write(abstraction_label))
        
        # Highlight similarity between the two boards
        self.play(
            Indicate(opp_2p),
            Indicate(unified_opps_6p),
            color=WHITE,
            run_time=2
        )
        
        self.wait(2)

    def make_piece(self, cell, color):
        """Helper to create a board piece inside a grid cell."""
        return Square(
            side_length=0.6, 
            fill_color=color, 
            fill_opacity=1, 
            stroke_width=0
        ).move_to(cell.get_center())