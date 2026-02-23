from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # 2-player board with blue and red players
        blue_player = Circle().set_color(BLUE).shift(LEFT)
        red_player = Circle().set_color(RED).shift(RIGHT)
        players_2player = Group(blue_player, red_player)

        # 6-player board with different colors
        opponents = [Circle().set_color(color) for color in [BLUE, RED, GREEN, PURPLE, ORANGE]]
        opponents[0].shift(LEFT)
        opponents[1].shift(RIGHT)
        opponents[2].shift(DOWN + LEFT * 0.5)
        opponents[3].shift(DOWN + RIGHT * 0.5)
        opponent_group = Group(*opponents)

        # Animation: Cross out individual opponents and merge into a single 'Red'
        cross_out_animation = VGroup(*opponents).animate.set_color(WHITE)
        cross_out_target = Group(Circle().set_color(RED).shift(RIGHT), Circle().set_color(RED).shift(DOWN))
        cross_out_target.shift(RIGHT)

        self.play(Create(players_2player), Write(MathTex(r"S \in \mathbb{B}^{n \times n \times 3}")))
        self.wait(1)
        self.play(FadeOut(players_2player))
        self.play(Create(opponent_group))
        self.wait(1)
        self.play(cross_out_animation, run_time=2)
        self.play(Transform(opponent_group, cross_out_target))
        self.wait(1)
        self.play(FadeOut(opponent_group), Write(MathTex(r"S \in \mathbb{B}^{n \times n \times 1}").to_edge(RIGHT)))
        self.wait(2)