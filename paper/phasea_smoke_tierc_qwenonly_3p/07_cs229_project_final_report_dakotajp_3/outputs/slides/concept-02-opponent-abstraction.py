from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # Initial 2-player board
        blue_player = Circle().set_color(BLUE).scale(0.5)
        red_player = Circle().set_color(RED).scale(0.5)
        blue_player.shift(RIGHT * 1.5)
        red_player.shift(LEFT * 1.5)
        board_2p = VGroup(blue_player, red_player).to_edge(UP)

        # 6-player board
        opponents = [Circle().set_color(color).scale(0.5) for color in [BLUE, GREEN, YELLOW, PURPLE, ORANGE]]
        opponents_positions = [RIGHT * (i + 1) for i in range(5)]
        board_6p = VGroup(*[opponent.shift(pos) for opponent, pos in zip(opponents, opponents_positions)]).to_edge(UP)

        # Cross-out animation for 6-player board
        cross_out = VGroup(*[Line(start=opponent.get_left(), end=opponent.get_right()).set_color(BLACK) for opponent in opponents])
        self.play(Create(board_6p), Create(cross_out))
        self.wait(1)

        # Transform 6-player board to single 'Opponent Layer'
        unified_opponent = Circle().set_color(RED).scale(1.5)
        self.play(Transform(board_6p, unified_opponent))
        self.wait(1)

        # Check mark animation
        check_mark = MathTex(r"\checkmark").scale(1.5).set_color(GREEN)
        check_mark.shift(DOWN * 2)
        self.play(Create(check_mark))
        self.wait(1)

        # Fade out
        self.play(FadeOut(board_2p), FadeOut(check_mark))
        self.wait(1)