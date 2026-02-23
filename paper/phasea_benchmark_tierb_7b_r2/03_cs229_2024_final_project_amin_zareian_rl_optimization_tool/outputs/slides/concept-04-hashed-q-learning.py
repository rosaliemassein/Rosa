from manim import *

class HashedQLearning(Scene):
    def construct(self):
        # Grid patterns
        grid_1 = Square(tiles=4, fill_color=BLUE).shift(LEFT * 2)
        grid_2 = Square(tiles=4, fill_color=GREEN).shift(RIGHT * 2)
        grid_3 = Square(tiles=4, fill_color=YELLOW).shift(UP * 2)

        # Hash function box
        hash_function = Rectangle(width=3, height=1, fill_color=WHITE).shift(ORIGIN)
        hash_function_text = MathTex(r"\text{Hash Function}", font_size=24).next_to(hash_function, UP)

        # Q-Table
        q_table = VGroup(
            MathTex(r"\text{Q}(A,0)", font_size=24).shift(RIGHT * 1.5),
            MathTex(r"\text{Q}(B,0)", font_size=24).shift(RIGHT * 3.5),
            MathTex(r"\text{Q}(C,0)", font_size=24).shift(DOWN * 1.5),
            MathTex(r"\text{Q}(D,0)", font_size=24).shift(DOWN * 3.5)
        ).arrange(RIGHT, buff=1)

        # Lines from grids to hash function
        line_1 = Line(grid_1.get_center(), hash_function.get_bottom()).shift(DOWN * 0.5)
        line_2 = Line(grid_2.get_center(), hash_function.get_bottom()).shift(DOWN * 0.5)
        line_3 = Line(grid_3.get_center(), hash_function.get_bottom()).shift(DOWN * 0.5)

        # Lines from hash function to Q-Table
        line_1_out = Line(hash_function.get_top(), q_table[0].get_bottom()).shift(RIGHT * 0.5)
        line_2_out = Line(hash_function.get_top(), q_table[1].get_bottom()).shift(RIGHT * 0.5)
        line_3_out = Line(hash_function.get_top(), q_table[2].get_bottom()).shift(RIGHT * 0.5)

        # Collision
        collision_text = MathTex(r"\text{Collision}", font_size=24).set_color(RED).next_to(q_table[0], DOWN, buff=1)

        # Animation
        self.play(Create(grid_1), Create(grid_2), Create(grid_3))
        self.wait(1)
        self.play(Create(hash_function), Write(hash_function_text))
        self.wait(1)
        self.play(Create(q_table))
        self.wait(1)
        self.play(Create(line_1), Create(line_2), Create(line_3))
        self.wait(1)
        self.play(Create(line_1_out), Transform(q_table[0], collision_text))
        self.wait(1)
        self.play(Create(line_2_out), Transform(q_table[1], collision_text))
        self.wait(1)
        self.play(Create(line_3_out), Transform(q_table[2], collision_text))
        self.wait(1)