from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Title and Narration
        goal_text = Text("Hashed Q-Learning: Memory vs. Accuracy", font_size=32).to_edge(UP)
        self.play(Write(goal_text))
        
        # 2. Grid Patterns (Left side)
        def create_mini_grid(pattern):
            grid = VGroup()
            for row in pattern:
                for cell in row:
                    sq = Square(side_length=0.25, stroke_width=1)
                    if cell == 1:
                        sq.set_fill(BLUE, opacity=1)
                    grid.add(sq)
            grid.arrange_in_grid(rows=4, cols=4, buff=0)
            return grid

        patterns = [
            [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]], # Checkered
            [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]], # Blocks
            [[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]  # X-shape
        ]
        
        grids = VGroup(*[create_mini_grid(p) for p in patterns]).arrange(DOWN, buff=0.8)
        grids.to_edge(LEFT, buff=1)
        
        self.play(Create(grids))

        # 3. Hash Function Box (Center)
        hash_box = VGroup(
            Rectangle(width=3, height=1.5, color=YELLOW),
            Text("Hash Function", font_size=24)
        )
        hash_box.move_to(ORIGIN)
        
        self.play(Create(hash_box))

        # 4. Q-Table (Right side)
        q_table_label = Text("Compact Q-Table", font_size=20).shift(RIGHT * 4.5 + UP * 2.2)
        q_table = VGroup(*[
            Rectangle(width=2, height=0.4, stroke_width=2).set_fill(GREY, opacity=0.2)
            for _ in range(6)
        ]).arrange(DOWN, buff=0.1).move_to(RIGHT * 4.5)
        
        self.play(Create(q_table), Write(q_table_label))

        # 5. Connect Grids to Hash Function
        arrows_in = VGroup(*[
            Arrow(start=g.get_right(), end=hash_box.get_left(), buff=0.1, color=WHITE)
            for g in grids
        ])
        
        self.play(Create(arrows_in))

        # 6. Hash Mapping and Collision
        # Grid 0 -> Row 1
        # Grid 1 -> Row 4
        # Grid 2 -> Row 4 (Collision)
        
        arrow_out1 = Arrow(start=hash_box.get_right(), end=q_table[1].get_left(), color=WHITE)
        arrow_out2 = Arrow(start=hash_box.get_right(), end=q_table[4].get_left(), color=WHITE)
        arrow_out3 = Arrow(start=hash_box.get_right(), end=q_table[4].get_left(), color=RED)

        self.play(Create(arrow_out1))
        self.play(q_table[1].animate.set_fill(GREEN, opacity=0.5))
        
        self.play(Create(arrow_out2))
        self.play(q_table[4].animate.set_fill(GREEN, opacity=0.5))
        
        # Collision Highlight
        self.play(Create(arrow_out3))
        self.play(
            Flash(q_table[4], color=RED, flash_radius=0.5),
            q_table[4].animate.set_stroke(RED, width=4)
        )
        
        collision_label = Text("Collision!", color=RED, font_size=24).next_to(q_table[4], DOWN)
        self.play(Write(collision_label))
        self.wait(1)

        # 7. Formula (Bottom)
        formula = MathTex(
            "\\text{Index} = \\text{Hash}(\\text{MatrixState}) \\pmod L",
            font_size=36, color=BLUE
        ).to_edge(DOWN, buff=1)
        
        self.play(Write(formula))
        
        # 8. Caption
        narration = Text(
            "Different patterns map to the same entry, leading to confusion.",
            font_size=20, slant="ITALIC"
        ).next_to(formula, UP, buff=0.2)
        
        self.play(FadeIn(narration))
        self.wait(2)

        # Cleanup
        self.play(
            *[FadeOut(m) for m in [grids, hash_box, q_table, arrows_in, arrow_out1, arrow_out2, arrow_out3, collision_label, q_table_label, formula, narration, goal_text]]
        )
        self.wait(1)