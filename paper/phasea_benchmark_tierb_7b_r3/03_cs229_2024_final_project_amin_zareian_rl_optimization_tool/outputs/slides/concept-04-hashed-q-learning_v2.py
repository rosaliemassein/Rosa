from manim import *

class HashedQLearning(Scene):
    def construct(self):
        # 1. Formula at the top
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L")
        formula.to_edge(UP, buff=0.5)
        self.play(Write(formula))

        # 2. Helper to create 4x4 Grid patterns
        def create_grid_pattern(filled_indices):
            grid = VGroup(*[Square(side_length=0.25, stroke_width=1) for _ in range(16)])
            grid.arrange_in_grid(rows=4, cols=4, buff=0)
            for i in filled_indices:
                grid[i].set_fill(WHITE, opacity=1)
            return grid

        # Patterns for the grids
        p1_indices = [0, 2, 5, 7, 8, 10, 13, 15] # Checkerboard variant 1
        p2_indices = [1, 3, 4, 6, 9, 11, 12, 14] # Checkerboard variant 2
        p3_indices = [0, 1, 4, 5, 10, 11, 14, 15] # Block pattern

        g1 = create_grid_pattern(p1_indices)
        g2 = create_grid_pattern(p2_indices)
        g3 = create_grid_pattern(p3_indices)
        
        grids = VGroup(g1, g2, g3).arrange(DOWN, buff=0.8).to_edge(LEFT, buff=1)
        grid_labels = VGroup(
            Text("State A", font_size=18).next_to(g1, LEFT),
            Text("State B", font_size=18).next_to(g2, LEFT),
            Text("State C", font_size=18).next_to(g3, LEFT)
        )

        # 3. Hash Function Box
        hash_rect = Rectangle(height=2, width=3, color=BLUE)
        hash_text = Text("Hash Function", font_size=24).move_to(hash_rect)
        hash_box = VGroup(hash_rect, hash_text).move_to(ORIGIN).shift(LEFT * 0.5)

        # 4. Q-Table
        table_rows = VGroup(*[
            VGroup(
                Rectangle(height=0.5, width=2.5),
                Line(LEFT*1.25, RIGHT*1.25).shift(UP*0.25) # Top border
            ) for _ in range(6)
        ]).arrange(DOWN, buff=0)
        
        # Add a bottom border to the last row
        table_rows.add(Line(LEFT*1.25, RIGHT*1.25).next_to(table_rows[-1], DOWN, buff=0))
        
        table_label = Text("Compact Q-Table", font_size=24).next_to(table_rows, UP)
        q_table = VGroup(table_rows, table_label).to_edge(RIGHT, buff=1)

        # 5. Animations
        self.play(FadeIn(grids), FadeIn(grid_labels))
        self.play(Create(hash_box))
        self.play(Create(q_table))
        self.wait(1)

        # Arrows from Grids to Hash Box
        arrows_in = VGroup(
            Arrow(g1.get_right(), hash_box.get_left(), buff=0.1),
            Arrow(g2.get_right(), hash_box.get_left(), buff=0.1),
            Arrow(g3.get_right(), hash_box.get_left(), buff=0.1)
        )

        # Arrows from Hash Box to Table Rows (Collision on Row 3)
        # We index table_rows from 0 to 5. Let's map g1->0, g2->3, g3->3
        target_indices = [0, 3, 3]
        arrows_out = VGroup(
            Arrow(hash_box.get_right(), table_rows[0].get_left(), buff=0.1),
            Arrow(hash_box.get_right(), table_rows[3].get_left(), buff=0.1),
            Arrow(hash_box.get_right(), table_rows[3].get_left(), buff=0.1, color=RED)
        )

        # Animation sequence for hashing
        # First State
        self.play(GrowArrow(arrows_in[0]))
        self.play(GrowArrow(arrows_out[0]))
        self.play(table_rows[0][0].animate.set_fill(BLUE, opacity=0.3))
        self.wait(0.5)

        # Second State
        self.play(GrowArrow(arrows_in[1]))
        self.play(GrowArrow(arrows_out[1]))
        self.play(table_rows[3][0].animate.set_fill(BLUE, opacity=0.3))
        self.wait(0.5)

        # Third State (The Collision)
        self.play(GrowArrow(arrows_in[2]))
        self.play(GrowArrow(arrows_out[2]))
        
        # Collision Highlight
        collision_highlight = SurroundingRectangle(table_rows[3], color=RED, buff=0.1)
        collision_text = Text("COLLISION!", color=RED, font_size=24).next_to(collision_highlight, RIGHT)
        
        self.play(Create(collision_highlight), Write(collision_text))
        self.play(Flash(collision_highlight, color=RED, flash_radius=0.5))
        
        # Flashing effect
        for _ in range(3):
            self.play(collision_highlight.animate.set_stroke(opacity=0), run_time=0.2)
            self.play(collision_highlight.animate.set_stroke(opacity=1), run_time=0.2)

        self.wait(2)