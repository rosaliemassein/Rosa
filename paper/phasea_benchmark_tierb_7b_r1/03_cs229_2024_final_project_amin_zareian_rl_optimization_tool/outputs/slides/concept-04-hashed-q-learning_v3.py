import random
from manim import *

class HashedQTableScene(Scene):
    def construct(self):
        # 1. Create three different 4x4 grid patterns
        def create_mini_grid(seed_val):
            grid = VGroup(*[Square(side_length=0.2, stroke_width=1) for _ in range(16)]).arrange_in_grid(4, 4, buff=0)
            for i, sq in enumerate(grid):
                # Simple pattern logic to create variation
                if (i + seed_val + (i // 4)) % 2 == 0:
                    sq.set_fill(WHITE, opacity=1)
                else:
                    sq.set_fill(BLACK, opacity=1)
            return grid

        grid_a = create_mini_grid(1).shift(LEFT * 5 + UP * 2)
        grid_b = create_mini_grid(2).shift(LEFT * 5)
        grid_c = create_mini_grid(3).shift(LEFT * 5 + DOWN * 2)
        grids = VGroup(grid_a, grid_b, grid_c)

        # 2. Central Hash Function Box
        hash_box = VGroup(
            Rectangle(height=1.5, width=3, color=BLUE),
            Text("Hash Function", font_size=24)
        ).move_to(LEFT * 1)

        # 3. Compact Q-Table (Manual construction to avoid Table class constraints)
        table_label = Text("Q-Table", font_size=24).shift(RIGHT * 4 + UP * 2.5)
        rows = VGroup(*[
            VGroup(
                Rectangle(height=0.6, width=2.5),
                Text(f"Entry {i}", font_size=18).move_to(LEFT * 0.6)
            ) for i in range(5)
        ]).arrange(DOWN, buff=0).shift(RIGHT * 4)
        
        # Values inside table using Text instead of DecimalNumber
        values = VGroup(*[
            Text(str(round(random.uniform(-1, 1), 2)), font_size=16).move_to(rows[i].get_right() + LEFT * 0.5)
            for i in range(5)
        ])
        q_table = VGroup(table_label, rows, values)

        # 4. Formula
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L", font_size=32).to_edge(UP)

        # 5. Animation Sequences
        self.play(Write(formula))
        self.play(FadeIn(grids))
        self.play(Create(hash_box))
        
        # Arrows from grids to hash box
        arrows_in = VGroup(*[Arrow(g.get_right(), hash_box.get_left(), buff=0.1) for g in grids])
        self.play(Create(arrows_in))
        self.wait(0.5)

        self.play(FadeIn(q_table))
        self.wait(0.5)

        # 6. Arrows from Hash Box to Q-Table (Illustrating a Collision)
        # We'll map Grid B and Grid C to the same table entry (Index 2)
        arrow_out_a = Arrow(hash_box.get_right(), rows[0].get_left(), buff=0.1, color=WHITE)
        arrow_out_b = Arrow(hash_box.get_right(), rows[2].get_left(), buff=0.1, color=YELLOW)
        arrow_out_c = Arrow(hash_box.get_right(), rows[2].get_left(), buff=0.1, color=ORANGE)

        self.play(Create(arrow_out_a))
        self.play(Create(arrow_out_b))
        self.play(Create(arrow_out_c))
        
        # Collision Visual Cue
        collision_rect = SurroundingRectangle(rows[2], color=RED, buff=0.1)
        collision_text = Text("COLLISION", color=RED, font_size=20).next_to(collision_rect, RIGHT)
        
        self.play(
            Create(collision_rect),
            Write(collision_text),
            Indicate(VGroup(grid_b, grid_c), color=RED)
        )
        # Flashing effect
        self.play(Flash(collision_rect, color=RED, flash_radius=0.5, num_lines=12))
        self.wait(1)

        # 7. Conclusion text
        explanation = Text(
            "Trade-off: Memory efficiency vs. Optimization accuracy", 
            font_size=24, 
            color=BLUE
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(2)