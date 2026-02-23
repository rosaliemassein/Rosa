from manim import *

class HashedQLearning(Scene):
    def construct(self):
        # Title and Formula
        title = Text("Hashed Q-Learning", font_size=36).to_edge(UP)
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L", font_size=32).next_to(title, DOWN)
        self.add(title, formula)

        # Helper to create a 4x4 mini-grid
        def create_mini_grid(color=BLUE):
            cells = VGroup(*[Square(side_length=0.2, stroke_width=1, fill_opacity=0.5, fill_color=color) for _ in range(16)])
            cells.arrange_in_grid(4, 4, buff=0)
            return cells

        # Grids on the left
        grid1 = create_mini_grid(BLUE).shift(LEFT * 5 + UP * 1.5)
        grid2 = create_mini_grid(GREEN).shift(LEFT * 5)
        grid3 = create_mini_grid(YELLOW).shift(LEFT * 5 + DOWN * 1.5)
        grids = VGroup(grid1, grid2, grid3)

        # Hash Function box in the center
        hash_box = VGroup(
            Rectangle(width=3, height=1.5, color=WHITE),
            Text("Hash Function", font_size=24)
        ).shift(LEFT * 1)

        # Q-Table on the right
        table_label = Text("Q-Table", font_size=24).shift(RIGHT * 3.5 + UP * 2.5)
        q_table = VGroup(*[
            Rectangle(width=2, height=0.6, stroke_width=2).shift(RIGHT * 3.5 + UP * (1.5 - i * 0.7))
            for i in range(5)
        ])
        q_labels = VGroup(*[
            MathTex(rf"Q[{i}]", font_size=20).move_to(q_table[i].get_center())
            for i in range(5)
        ])
        table_group = VGroup(table_label, q_table, q_labels)

        # Connections
        # Grid 1 -> Hash -> Row 0
        arrow1_in = Arrow(grid1.get_right(), hash_box.get_left(), buff=0.1)
        arrow1_out = Arrow(hash_box.get_right(), q_table[0].get_left(), buff=0.1)

        # Grid 2 -> Hash -> Row 3
        arrow2_in = Arrow(grid2.get_right(), hash_box.get_left(), buff=0.1)
        arrow2_out = Arrow(hash_box.get_right(), q_table[3].get_left(), buff=0.1)

        # Grid 3 -> Hash -> Row 0 (Collision)
        arrow3_in = Arrow(grid3.get_right(), hash_box.get_left(), buff=0.1)
        arrow3_out = Arrow(hash_box.get_right(), q_table[0].get_left(), buff=0.1, color=RED)

        # Animation Sequence
        self.play(FadeIn(grids))
        self.play(Create(hash_box))
        self.play(Create(table_group))
        self.wait(1)

        # First Grid mapping
        self.play(Create(arrow1_in))
        self.play(Create(arrow1_out))
        self.play(q_table[0].animate.set_fill(BLUE, opacity=0.3))
        self.wait(0.5)

        # Second Grid mapping
        self.play(Create(arrow2_in))
        self.play(Create(arrow2_out))
        self.play(q_table[3].animate.set_fill(GREEN, opacity=0.3))
        self.wait(0.5)

        # Third Grid mapping (Collision)
        self.play(Create(arrow3_in))
        self.play(Create(arrow3_out))
        
        # Collision Highlight
        collision_warning = Text("COLLISION!", color=RED, font_size=30).next_to(q_table[0], RIGHT)
        self.play(
            Flash(q_table[0], color=RED, line_length=0.3),
            q_table[0].animate.set_stroke(RED, width=5),
            Write(collision_warning)
        )
        self.play(Indicate(q_table[0], color=RED))
        
        self.wait(2)