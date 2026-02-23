from manim import *

class ConceptScene(Scene):
    def construct(self):
        # 1. Setup Grids (Left side) - Creating distinct 4x4 patterns
        def create_mini_grid(color_indices, base_color):
            grid = VGroup(*[
                Square(side_length=0.2, fill_opacity=0.8, fill_color=base_color if i in color_indices else BLACK, stroke_width=1)
                for i in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.05)
            return grid

        # Patterns representing different states
        grid1 = create_mini_grid([0, 2, 5, 7, 8, 10, 13, 15], BLUE)
        grid2 = create_mini_grid([1, 3, 4, 6, 9, 11, 12, 14], GREEN)
        grid3 = create_mini_grid([0, 1, 2, 3, 12, 13, 14, 15], YELLOW)
        
        grids = VGroup(grid1, grid2, grid3).arrange(DOWN, buff=1).to_edge(LEFT, buff=1)

        # 2. Hash Function Box (Center)
        hash_box = VGroup(
            RoundedRectangle(corner_radius=0.1, width=3, height=1.5, color=WHITE),
            Text("Hash Function", font_size=24)
        ).move_to(ORIGIN)

        # 3. Q-Table (Right side)
        q_table = VGroup(*[
            Rectangle(width=2, height=0.4, stroke_width=2, color=BLUE) for _ in range(8)
        ]).arrange(DOWN, buff=0).to_edge(RIGHT, buff=1)
        q_table_label = Text("Q-Table", font_size=24).next_to(q_table, UP)

        # 4. Formula (Bottom)
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L", font_size=32).to_edge(DOWN, buff=0.8)

        # 5. Initialization
        self.add(grids, hash_box, q_table, q_table_label)
        self.play(Write(formula))
        self.wait(1)

        # 6. Arrows from Grids to Hash Box
        arrows_in = VGroup(*[
            Arrow(g.get_right(), hash_box.get_left(), buff=0.1, color=WHITE)
            for g in grids
        ])
        
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_in], lag_ratio=0.5))
        self.wait(0.5)

        # 7. Arrows from Hash Box to Q-Table (Collision Logic)
        # Grid 1 -> Row 1
        # Grid 2 -> Row 5
        # Grid 3 -> Row 5 (Collision)
        out_arrow1 = Arrow(hash_box.get_right(), q_table[1].get_left(), buff=0.1, color=BLUE)
        out_arrow2 = Arrow(hash_box.get_right(), q_table[5].get_left(), buff=0.1, color=GREEN)
        out_arrow3 = Arrow(hash_box.get_right(), q_table[5].get_left(), buff=0.1, color=YELLOW)

        self.play(GrowArrow(out_arrow1))
        self.wait(0.2)
        self.play(GrowArrow(out_arrow2))
        self.wait(0.2)
        self.play(GrowArrow(out_arrow3))

        # 8. Highlight Collision
        collision_highlight = SurroundingRectangle(q_table[5], color=RED, buff=0.1)
        collision_text = Text("Collision!", color=RED, font_size=24).next_to(collision_highlight, UP)

        self.play(
            Create(collision_highlight),
            Write(collision_text)
        )
        
        # Flashing red highlight effect
        for _ in range(3):
            self.play(collision_highlight.animate.set_fill(RED, opacity=0.5), run_time=0.2)
            self.play(collision_highlight.animate.set_fill(RED, opacity=0), run_time=0.2)

        # 9. Narration / Commentary Text
        narration = Text(
            "Different patterns share the same table entry.",
            font_size=22
        ).to_edge(UP, buff=0.5)
        
        self.play(FadeIn(narration))
        self.wait(2)

        # 10. Objective Note
        goal_note = Text(
            "Goal: Trade-off between memory and accuracy.",
            font_size=20, color=BLUE
        ).next_to(formula, DOWN, buff=0.3)
        self.play(FadeIn(goal_note))
        self.wait(2)