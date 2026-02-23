from manim import *

class Concept04HashedQLearning(Scene):
    def construct(self):
        # 1. Formula (Reference)
        # Using MathTex with raw string to handle LaTeX symbols
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod{L}")
        formula.to_edge(UP, buff=0.5)
        
        # 2. Function to create 4x4 Grid Patterns
        def create_mini_grid(color_val):
            g = VGroup(*[Square(side_length=0.2, stroke_width=1) for _ in range(16)])
            g.arrange_in_grid(4, 4, buff=0)
            # Apply fill to some squares to represent a "state"
            fill_indices = [0, 2, 5, 7, 8, 10, 13, 15]
            for i in fill_indices:
                g[i].set_fill(color_val, opacity=0.7)
            return g

        # Create three different patterns
        grid1 = create_mini_grid(BLUE).shift(LEFT * 5 + UP * 1.5)
        grid2 = create_mini_grid(GREEN).shift(LEFT * 5 + ORIGIN)
        grid3 = create_mini_grid(YELLOW).shift(LEFT * 5 + DOWN * 1.5)
        grids = VGroup(grid1, grid2, grid3)

        # 3. Hash Function Box (Center)
        hash_box_rect = Rectangle(width=3, height=1.5, color=BLUE, fill_opacity=0.2)
        hash_box_text = Text("Hash Function", font_size=24)
        hash_box = VGroup(hash_box_rect, hash_box_text).move_to(LEFT * 0.5)

        # 4. Q-Table (Right side) - Fixed-size table
        q_table = VGroup(*[
            Rectangle(width=2, height=0.4, stroke_width=2) 
            for _ in range(8)
        ]).arrange(DOWN, buff=0.1)
        q_table.shift(RIGHT * 4)
        q_table_label = Text("Compact Q-Table", font_size=20).next_to(q_table, UP)

        # 5. Connective Arrows
        # From Grids to Hash Box
        arrows_in = VGroup(*[
            Arrow(g.get_right(), hash_box.get_left(), buff=0.1, color=GRAY)
            for g in grids
        ])

        # From Hash Box to Table (Simulating mappings)
        # We'll make Grid 2 and Grid 3 map to the same row (Index 4)
        arrow_out1 = Arrow(hash_box.get_right(), q_table[1].get_left(), buff=0.1, color=BLUE)
        arrow_out2 = Arrow(hash_box.get_right(), q_table[4].get_left(), buff=0.1, color=GREEN)
        arrow_out3 = Arrow(hash_box.get_right(), q_table[4].get_left(), buff=0.1, color=YELLOW)

        # 6. Narration text at the bottom
        narration = Text(
            "To solve the memory problem, we use a Hashed Q-table.",
            font_size=22
        ).to_edge(DOWN, buff=0.5)

        # --- Animation Sequence ---

        # Step 1: Display formula and first narration
        self.play(Write(formula), Write(narration))
        self.wait(1)

        # Step 2: Show grids, hash box, and the compact table
        self.play(
            Create(grids),
            Create(hash_box),
            Create(q_table),
            Write(q_table_label)
        )
        self.wait(1)

        # Step 3: Show the mapping process
        self.play(Create(arrows_in))
        self.play(Create(arrow_out1))
        self.wait(0.5)
        self.play(Create(arrow_out2))
        self.play(Create(arrow_out3))
        
        # Step 4: Highlight the Collision
        collision_msg = Text(
            "Collision: Different patterns share the same table entry.",
            font_size=22, color=RED
        ).to_edge(DOWN, buff=0.5)
        
        # Create a red highlight for the collided entry
        collision_highlight = q_table[4].copy()
        collision_highlight.set_stroke(RED, width=6).set_fill(RED, opacity=0.3)

        self.play(
            Transform(narration, collision_msg),
            FadeIn(collision_highlight)
        )
        
        # Flashing effect using a manual scale-up-and-down to avoid undefined rate functions
        for _ in range(2):
            self.play(
                collision_highlight.animate.scale(1.15),
                grid2.animate.set_color(RED),
                grid3.animate.set_color(RED),
                run_time=0.4
            )
            self.play(
                collision_highlight.animate.scale(1/1.15),
                grid2.animate.set_color(GREEN),
                grid3.animate.set_color(YELLOW),
                run_time=0.4
            )

        # Step 5: Final Narration Update
        final_msg = Text(
            "This efficiency allows handling larger state spaces.",
            font_size=22
        ).to_edge(DOWN, buff=0.5)
        self.play(Transform(narration, final_msg))
        
        self.wait(2)