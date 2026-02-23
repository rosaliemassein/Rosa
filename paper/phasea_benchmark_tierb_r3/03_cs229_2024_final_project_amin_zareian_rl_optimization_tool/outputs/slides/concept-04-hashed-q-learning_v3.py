from manim import *
import random

class Concept04HashedQLearning(Scene):
    def construct(self):
        # 1. Define Formula and Narration
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L")
        formula.to_edge(UP, buff=0.5)

        # 2. Create Grid Patterns (Left)
        def create_grid(seed_val, color):
            random.seed(seed_val)
            grid = VGroup(*[
                Square(side_length=0.2, stroke_width=1, fill_opacity=0.3, fill_color=GRAY)
                for _ in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.05)
            # Fill some squares to create a pattern
            for i in range(16):
                if random.random() > 0.5:
                    grid[i].set_fill(color, opacity=1)
            return grid

        p1 = create_grid(10, BLUE).shift(UP * 2.2)
        p2 = create_grid(20, GREEN)
        p3 = create_grid(30, YELLOW).shift(DOWN * 2.2)
        patterns = VGroup(p1, p2, p3).to_edge(LEFT, buff=1)

        # 3. Create Hash Function Box (Center)
        hash_box = VGroup(
            Rectangle(width=2.5, height=1.2, color=WHITE),
            Text("Hash Function", font_size=20)
        ).move_to(ORIGIN)

        # 4. Create Q-Table (Right)
        table_rows = VGroup(*[
            Rectangle(width=1.8, height=0.4, stroke_width=1)
            for _ in range(8)
        ]).arrange(DOWN, buff=0).to_edge(RIGHT, buff=1)
        table_label = Text("Q-Table", font_size=24).next_to(table_rows, UP)
        q_table = VGroup(table_rows, table_label)

        # 5. Display Initial Elements
        self.play(Write(formula))
        self.play(FadeIn(patterns, shift=RIGHT))
        self.play(Create(hash_box))
        self.play(Create(q_table))
        self.wait(1)

        # 6. Animation: Map Grid 1 -> Row 1
        a1_in = Arrow(p1.get_right(), hash_box.get_left(), buff=0.1)
        a1_out = Arrow(hash_box.get_right(), table_rows[0].get_left(), buff=0.1)
        self.play(GrowArrow(a1_in))
        self.play(GrowArrow(a1_out))
        self.play(table_rows[0].animate.set_fill(BLUE, opacity=0.6))
        self.wait(0.5)

        # 7. Animation: Map Grid 2 -> Row 5
        a2_in = Arrow(p2.get_right(), hash_box.get_left(), buff=0.1)
        a2_out = Arrow(hash_box.get_right(), table_rows[4].get_left(), buff=0.1)
        self.play(GrowArrow(a2_in))
        self.play(GrowArrow(a2_out))
        self.play(table_rows[4].animate.set_fill(GREEN, opacity=0.6))
        self.wait(0.5)

        # 8. Animation: Map Grid 3 -> Row 1 (COLLISION)
        a3_in = Arrow(p3.get_right(), hash_box.get_left(), buff=0.1)
        a3_out = Arrow(hash_box.get_right(), table_rows[0].get_left(), buff=0.1, color=RED)
        
        self.play(GrowArrow(a3_in))
        self.play(GrowArrow(a3_out))
        
        # Flashing red highlight to indicate collision
        collision_rect = table_rows[0].copy().set_stroke(RED, width=6).set_fill(RED, opacity=0.3)
        self.play(FadeIn(collision_rect))
        self.play(Flash(collision_rect, color=RED, line_length=0.3, num_lines=10))
        
        collision_label = Text("COLLISION!", color=RED, font_size=24).next_to(table_rows[0], RIGHT)
        self.play(Write(collision_label))
        
        # Shake the rows to show "confusion"
        self.play(table_rows[0].animate.shift(LEFT*0.1), run_time=0.1)
        self.play(table_rows[0].animate.shift(RIGHT*0.2), run_time=0.1)
        self.play(table_rows[0].animate.shift(LEFT*0.1), run_time=0.1)

        self.wait(2)

        # Clear arrows and labels for final look
        self.play(
            FadeOut(a1_in), FadeOut(a1_out),
            FadeOut(a2_in), FadeOut(a2_out),
            FadeOut(a3_in), FadeOut(a3_out),
            FadeOut(collision_label),
            collision_rect.animate.set_fill(opacity=0.8)
        )
        self.wait(1)