from manim import *

class HashedQLearningConcept(Scene):
    def construct(self):
        # 1. Setup Formula
        formula_tex = r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L"

        # 2. Create Grids (Left)
        def create_grid(color_indices):
            grid = VGroup(*[
                Square(side_length=0.2, fill_opacity=0.8, fill_color=WHITE if i in color_indices else BLACK, stroke_width=1) 
                for i in range(16)
            ])
            grid.arrange_in_grid(4, 4, buff=0.05)
            return grid

        # Create three distinct 4x4 patterns
        pattern1 = create_grid([0, 2, 5, 7, 8, 10, 13, 15])
        pattern2 = create_grid([1, 3, 4, 6, 9, 11, 12, 14])
        pattern3 = create_grid([0, 1, 2, 3, 4, 8, 12])
        
        patterns = VGroup(pattern1, pattern2, pattern3).arrange(DOWN, buff=0.8).to_edge(LEFT, buff=1.0)

        # 3. Create Hash Function Box (Center)
        hash_box = VGroup(
            Rectangle(height=1.5, width=3, color=YELLOW),
            Text("Hash Function", font_size=24)
        ).move_to(ORIGIN)

        # 4. Create Q-Table (Right)
        q_table = VGroup(*[
            Rectangle(height=0.4, width=2, stroke_color=WHITE, stroke_width=2)
            for _ in range(8)
        ]).arrange(DOWN, buff=0.1).to_edge(RIGHT, buff=1.5)
        q_table_label = Text("Q-Table", font_size=24).next_to(q_table, UP)

        # 5. Animation Sequence
        self.play(FadeIn(patterns), FadeIn(hash_box), FadeIn(q_table), Write(q_table_label))
        self.wait(0.5)

        # Create input arrows
        arrows_in = VGroup(*[
            Arrow(p.get_right(), hash_box.get_left(), buff=0.1, color=GREY)
            for p in patterns
        ])
        
        # Mapping definition
        # Pattern 0 -> Index 1
        # Pattern 1 -> Index 5
        # Pattern 2 -> Index 5 (Collision)
        arrow_out_1 = Arrow(hash_box.get_right(), q_table[1].get_left(), buff=0.1, color=GREEN)
        arrow_out_2 = Arrow(hash_box.get_right(), q_table[5].get_left(), buff=0.1, color=BLUE)
        arrow_out_3 = Arrow(hash_box.get_right(), q_table[5].get_left(), buff=0.1, color=RED)

        # Step-by-step mapping
        # Pattern 1
        self.play(Create(arrows_in[0]))
        self.play(Create(arrow_out_1))
        self.play(q_table[1].animate.set_fill(GREEN, opacity=0.5))
        self.wait(0.5)

        # Pattern 2
        self.play(Create(arrows_in[1]))
        self.play(Create(arrow_out_2))
        self.play(q_table[5].animate.set_fill(BLUE, opacity=0.5))
        self.wait(0.5)

        # Pattern 3 (Collision)
        self.play(Create(arrows_in[2]))
        self.play(Create(arrow_out_3))
        
        # Highlight collision at Index 5
        collision_rect = SurroundingRectangle(q_table[5], color=RED, buff=0.05)
        collision_text = Text("Collision!", color=RED, font_size=20).next_to(collision_rect, RIGHT)
        
        self.play(Create(collision_rect))
        self.play(Flash(collision_rect, color=RED, line_length=0.3))
        self.play(Write(collision_text))
        self.wait(1)

        # 6. Add Formula and Title
        formula = MathTex(formula_tex).to_edge(DOWN, buff=1.0)
        title = Text("Hashed Q-Learning Concept", font_size=32, color=YELLOW).to_edge(UP, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(formula))
        self.wait(1)

        # 7. Summary Remark
        summary = Text("Collisions lead to sub-optimal 'almost-checkered' designs.", font_size=20, color=GREY).next_to(formula, DOWN, buff=0.2)
        self.play(FadeIn(summary))
        self.wait(3)