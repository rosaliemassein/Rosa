from manim import *

class Concept04HashedQLearning(Scene):
    def construct(self):
        # 1. Formula at the top
        formula = MathTex(r"\text{Index} = \text{Hash}(\text{MatrixState}) \pmod L", font_size=36)
        formula.to_edge(UP, buff=0.5)
        self.play(Write(formula))

        # 2. Define 4x4 Grid Patterns (Left side)
        def create_4x4_grid(pattern_type=0):
            grid = VGroup()
            for i in range(16):
                row, col = i // 4, i % 4
                if pattern_type == 0: # Checkered
                    color = WHITE if (row + col) % 2 == 0 else BLACK
                elif pattern_type == 1: # Vertical Stripes
                    color = WHITE if col % 2 == 0 else BLACK
                else: # Random-ish / Collision state
                    color = WHITE if (i * 3 + 1) % 5 < 2 else BLACK
                
                sq = Square(side_length=0.3, fill_opacity=1, fill_color=color, stroke_width=1, stroke_color=GRAY)
                grid.add(sq)
            return grid.arrange_in_grid(4, 4, buff=0)

        grid1 = create_4x4_grid(0)
        grid2 = create_4x4_grid(1)
        grid3 = create_4x4_grid(2)
        
        grids = VGroup(grid1, grid2, grid3).arrange(DOWN, buff=0.6).to_edge(LEFT, buff=1)
        grid_labels = VGroup(
            Text("State A", font_size=16).next_to(grid1, LEFT),
            Text("State B", font_size=16).next_to(grid2, LEFT),
            Text("State C", font_size=16).next_to(grid3, LEFT)
        )

        # 3. Hash Function Box (Center)
        hash_box = VGroup(
            Rectangle(height=1.5, width=2.5, color=BLUE, fill_opacity=0.2),
            Text("Hash Function", font_size=24)
        ).move_to(ORIGIN)

        # 4. Q-Table (Right side)
        q_table_slots = VGroup(*[
            Rectangle(height=0.4, width=2.2, color=WHITE) for _ in range(6)
        ]).arrange(DOWN, buff=0).to_edge(RIGHT, buff=1.2)
        q_table_label = Text("Compact Q-Table", font_size=24).next_to(q_table_slots, UP)
        
        # Animations: Initial setup
        self.play(
            FadeIn(grids), 
            FadeIn(grid_labels),
            Create(hash_box), 
            Create(q_table_slots), 
            Write(q_table_label)
        )
        self.wait(1)

        # 5. Draw Arrows from Grids to Hash Function
        arrows_in = VGroup(*[
            Arrow(g.get_right(), hash_box.get_left(), buff=0.1, stroke_width=3)
            for g in grids
        ])
        self.play(Create(arrows_in))
        self.wait(0.5)

        # 6. Draw Arrows from Hash Function to Q-Table with a Collision
        # Grid 1 maps to Slot 1
        # Grid 2 and 3 both map to Slot 4 (Collision)
        arrow_out1 = Arrow(hash_box.get_right(), q_table_slots[1].get_left(), buff=0.1)
        arrow_out2 = Arrow(hash_box.get_right(), q_table_slots[4].get_left(), buff=0.1)
        arrow_out3 = Arrow(hash_box.get_right(), q_table_slots[4].get_left(), buff=0.1, color=RED)

        self.play(Create(arrow_out1))
        self.wait(0.5)
        self.play(Create(arrow_out2))
        self.wait(0.5)
        
        # Highlight Collision
        self.play(Create(arrow_out3))
        collision_rect = q_table_slots[4].copy().set_color(RED).set_stroke(width=6)
        
        self.play(
            Flash(q_table_slots[4], color=RED, flash_radius=0.5),
            Create(collision_rect)
        )
        
        collision_text = Text("COLLISION!", color=RED, font_size=24).next_to(q_table_slots[4], RIGHT)
        self.play(Write(collision_text))
        
        # 7. Final Polish: "Almost-checkered" design hint
        confusion_hint = Text("Agent confused between\nState B and State C", 
                              font_size=18, color=YELLOW).next_to(collision_text, DOWN, buff=0.5)
        self.play(Write(confusion_hint))

        self.wait(3)

        # Optional Clean up for voiceover timing
        self.play(
            FadeOut(collision_text),
            FadeOut(confusion_hint),
            collision_rect.animate.set_stroke(width=2)
        )
        self.wait(1)