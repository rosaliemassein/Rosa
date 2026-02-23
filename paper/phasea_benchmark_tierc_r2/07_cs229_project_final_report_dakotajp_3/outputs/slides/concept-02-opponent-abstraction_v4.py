from manim import *
import numpy as np

class Concept02OpponentAbstraction(Scene):
    def construct(self):
        # 1. Title and Formula
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").to_edge(UP)
        self.play(Write(formula))
        self.wait(0.5)

        # 2. Grid creation function
        def create_grid(colors_positions, base_color=GRAY_E):
            grid = VGroup()
            for x in range(3):
                for y in range(3):
                    square = Square(side_length=0.8, stroke_color=WHITE, stroke_width=2)
                    square.set_fill(base_color, opacity=0.5)
                    square.move_to(np.array([x * 0.8, y * 0.8, 0]))
                    grid.add(square)
            
            pieces = VGroup()
            for pos, color in colors_positions:
                idx = pos[0] * 3 + pos[1]
                dot = Dot(radius=0.25, color=color).move_to(grid[idx].get_center())
                pieces.add(dot)
            return VGroup(grid, pieces)

        # 3. 2-Player Board Representation
        two_player_board = create_grid([((0,0), BLUE), ((1,1), RED), ((2,2), RED), ((0,2), BLUE)])
        two_player_board.move_to(LEFT * 3)
        label_2p = Text("2-Player Board", font_size=24).next_to(two_player_board, DOWN)

        self.play(FadeIn(two_player_board), Write(label_2p))
        self.wait(1)

        # 4. 6-Player Board Representation (5 different opponent colors)
        opp_colors = [RED, GREEN, YELLOW, ORANGE, PURPLE]
        six_player_positions = [
            ((0,0), BLUE), ((1,1), RED), ((2,2), GREEN), 
            ((0,2), YELLOW), ((1,0), ORANGE), ((2,1), PURPLE)
        ]
        six_player_board = create_grid(six_player_positions)
        six_player_board.move_to(RIGHT * 3)
        label_6p = Text("6-Player Board", font_size=24).next_to(six_player_board, DOWN)

        self.play(FadeIn(six_player_board), Write(label_6p))
        self.wait(2)

        # 5. Transition to Abstraction Layer
        self.play(
            FadeOut(two_player_board), 
            FadeOut(label_2p),
            label_6p.animate.to_edge(LEFT).shift(UP*2),
            six_player_board.animate.scale(0.8).to_edge(LEFT).shift(DOWN*0.5)
        )

        # Create the 3 layers mentioned in the formula (n x n x 3)
        layers = VGroup()
        layer_colors = [BLUE, GRAY_B, RED] # Channel 0 (Me), Channel 1 (Board), Channel 2 (Opponent)
        for i in range(3):
            layer = create_grid([], base_color=layer_colors[i])
            layer[0].set_fill(layer_colors[i], opacity=0.2)
            # Offset layers to give a stacked 3D feel
            layer.shift(RIGHT * 2 + UP * i * 0.5 + RIGHT * i * 0.5)
            layers.add(layer)
        
        layer_labels = VGroup(
            Text("Me (Channel 0)", font_size=20, color=BLUE),
            Text("Board (Channel 1)", font_size=20, color=WHITE),
            Text("Opponent Layer (Channel 2)", font_size=20, color=RED)
        )
        for i, lbl in enumerate(layer_labels):
            lbl.next_to(layers[i], RIGHT)

        self.play(Create(layers))
        self.play(Write(layer_labels))
        self.wait(1)

        # 6. Merge 5 opponent colors into the unified 'Red' layer
        opponents_on_board = six_player_board[1][1:] # First piece is BLUE, others are opponents
        crosses = VGroup(*[
            VGroup(
                Line(UL, DR, color=RED, stroke_width=4), 
                Line(UR, DL, color=RED, stroke_width=4)
            ).scale(0.2).move_to(obj.get_center()) 
            for obj in opponents_on_board
        ])
        
        self.play(Create(crosses))
        self.wait(1)

        # Animate merging into the third layer
        self.play(
            opponents_on_board.animate.set_color(RED),
            FadeOut(crosses)
        )
        
        # Unified layer check mark
        check = Text("✓", color=GREEN, font_size=60).move_to(layers[2].get_center() + UP*0.5)
        self.play(Write(check))
        self.wait(1)

        # 7. Final narration text summary
        narration = Text(
            "Me vs. The Field: Unified Opponent Channel",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(narration))
        self.play(Indicate(formula))
        self.wait(3)