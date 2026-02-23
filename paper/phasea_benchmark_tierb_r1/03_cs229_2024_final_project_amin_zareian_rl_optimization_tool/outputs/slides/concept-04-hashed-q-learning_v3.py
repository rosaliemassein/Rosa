from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Grids (Left side)
        def create_mini_grid(pattern_type="random", offset=ORIGIN):
            grid = VGroup()
            for i in range(4):
                for j in range(4):
                    color = BLACK
                    if pattern_type == "checkered":
                        if (i + j) % 2 == 0: color = WHITE
                    elif pattern_type == "random":
                        if np.random.rand() > 0.5: color = WHITE
                    elif pattern_type == "other":
                        if i < 2: color = WHITE
                    
                    square = Square(side_length=0.2, fill_opacity=1, fill_color=color, stroke_width=1)
                    square.move_to(np.array([j*0.2, -i*0.2, 0]))
                    grid.add(square)
            grid.move_to(offset)
            return grid

        grid1 = create_mini_grid("random", offset=LEFT * 5 + UP * 2)
        grid2 = create_mini_grid("checkered", offset=LEFT * 5)
        grid3 = create_mini_grid("other", offset=LEFT * 5 + DOWN * 2)
        grids = VGroup(grid1, grid2, grid3)

        # 2. Hash Function Box (Center)
        hash_box = VGroup(
            Rectangle(width=3, height=1.5, color=BLUE),
            Text("Hash Function", font_size=24)
        ).shift(LEFT * 1)

        # 3. Formula (Top)
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L", font_size=36)
        formula.to_edge(UP)

        # 4. Q-Table (Right side)
        table_rows = VGroup(*[
            Rectangle(width=2, height=0.4, stroke_width=2) 
            for _ in range(8)
        ]).arrange(DOWN, buff=0.1).shift(RIGHT * 4)
        table_label = Text("Hashed Q-Table", font_size=20).next_to(table_rows, UP)
        q_table = VGroup(table_rows, table_label)

        # 5. Animation sequence
        self.play(Write(formula))
        self.play(Create(grids))
        self.play(Create(hash_box))
        self.play(Create(q_table))

        # Arrows from grids to hash box
        arrows_in = VGroup(*[
            Arrow(g.get_right(), hash_box.get_left(), buff=0.1)
            for g in grids
        ])
        self.play(Create(arrows_in))

        # Arrows from hash box to specific rows
        # Grid 1 -> Row 1
        # Grid 2 -> Row 5 (Collision)
        # Grid 3 -> Row 5 (Collision)
        arrow_out1 = Arrow(hash_box.get_right(), table_rows[1].get_left(), buff=0.1, color=WHITE)
        arrow_out2 = Arrow(hash_box.get_right(), table_rows[5].get_left(), buff=0.1, color=WHITE)
        arrow_out3 = Arrow(hash_box.get_right(), table_rows[5].get_left(), buff=0.1, color=RED)

        self.play(Create(arrow_out1))
        self.play(Create(arrow_out2))
        
        # Highlight Collision
        self.wait(0.5)
        self.play(
            Create(arrow_out3),
            table_rows[5].animate.set_fill(RED, opacity=0.5),
            run_time=1
        )
        
        collision_text = Text("Collision!", color=RED, font_size=30).next_to(table_rows[5], RIGHT)
        flash = Flash(table_rows[5], color=RED, flash_radius=0.5)
        
        self.play(
            Write(collision_text),
            flash
        )
        
        # Final Text for Goal
        goal_text = Text(
            "Goal: Memory Efficiency vs. Optimization Accuracy", 
            font_size=24, 
            color=YELLOW
        ).to_edge(DOWN)
        self.play(FadeIn(goal_text))
        
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 30
    scene = ConceptAnimation()
    scene.render()