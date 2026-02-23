from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # Define colors
        blue = BLUE
        red = RED
        opponent_colors = [GREEN, PURPLE, ORANGE, YELLOW]

        # Create 2-player board
        board_2p = [[Square(color=blue if j % 2 == 0 else red) for j in range(2)] for i in range(2)]
        board_2p_group = VGroup(*[VGroup(row) for row in board_2p]).arrange(RIGHT).shift(LEFT * 3)

        # Create 6-player board
        board_6p = [[Square(color=color) for color in opponent_colors] for _ in range(2)]
        board_6p_group = VGroup(*[VGroup(row) for row in board_6p]).arrange(RIGHT).shift(RIGHT * 3)

        # Show initial boards
        self.play(FadeIn(board_2p_group))
        self.wait(1)
        self.play(Transform(board_6p_group, board_2p_group))
        self.wait(1)

        # Cross-out individual opponent colors
        cross_out = VGroup(*[Line(start=opponent, end=[opponent[0] + 1.5, opponent[1], 0]) for opponent in board_6p_group])
        self.play(LaggedStart(*[Create(cross_out_section) for cross_out_section in cross_out]))
        self.wait(1)

        # Replace with unified 'Opponent Layer'
        opponent_layer = Circle(radius=0.5, color=red).shift(RIGHT * 3)
        self.play(Transform(board_6p_group, opponent_layer))
        self.wait(1)

        # Add 'Check' mark
        check_mark = MathTex(r"\checkmark", font_size=24).shift(RIGHT * 3)
        self.play(Create(check_mark))
        self.wait(2)

        # Animate the formula
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}", font_size=24).shift(UP * 2)
        self.play(FadeIn(formula))
        self.wait(2)

        # Fade out all elements
        self.play(FadeOut(board_6p_group), FadeOut(check_mark), FadeOut(formula))
        self.wait(1)