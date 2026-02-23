from manim import *
import numpy as np

class ConceptMatrix(Scene):
    def construct(self):
        # 1. Silhouettes of 15 basketball players
        # We represent players with simple geometric shapes (Circle + Rectangle)
        player_silhouettes = VGroup(*[
            VGroup(
                Circle(radius=0.12),
                Rectangle(height=0.25, width=0.2).next_to(Circle(radius=0.12), DOWN, buff=0.02)
            )
            for _ in range(15)
        ]).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)
        
        for p in player_silhouettes:
            p.set_color(GRAY)
        
        self.play(FadeIn(player_silhouettes))
        self.wait(0.5)
        
        # 2. Minutes played filter
        # Highlight top 10 players based on the conceptual filter
        filter_frame = SurroundingRectangle(player_silhouettes[:10], color=YELLOW, buff=0.1)
        filter_label = Text("Top 10 (Minutes Played)", font_size=18, color=YELLOW).next_to(filter_frame, UP)
        
        self.play(Create(filter_frame), Write(filter_label))
        self.play(
            player_silhouettes[:10].animate.set_color(WHITE),
            player_silhouettes[10:].animate.set_opacity(0.1)
        )
        self.wait(1)
        
        # 3. Create 10x15 feature matrix grid
        # 10 rows (players) x 15 columns (stats)
        grid = VGroup()
        for i in range(150):
            cell = Square(side_length=0.35, stroke_width=1)
            # Random opacity represents normalized data values
            cell.set_fill(BLUE, opacity=np.random.uniform(0.1, 0.9))
            grid.add(cell)
        
        grid.arrange_in_grid(rows=10, cols=15, buff=0.05).shift(DOWN * 0.7)
        
        # 4. Animate players sliding into rows
        self.play(
            FadeOut(filter_label),
            FadeOut(filter_frame),
            FadeOut(player_silhouettes[10:]),
            player_silhouettes[:10].animate.arrange(DOWN, buff=0.18).scale(0.7).next_to(grid, LEFT, buff=0.3)
        )
        
        # 5. Column Labels for basketball metrics
        stat_labels = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "FG%", "FT%", "3P%", "OFF", "DEF", "PF", "MIN", "PER", "PIE"]
        label_objs = VGroup(*[
            Text(stat_labels[i], font_size=12).next_to(grid[i], UP, buff=0.15).rotate(45 * DEGREES)
            for i in range(15)
        ])
        
        self.play(FadeIn(grid), FadeIn(label_objs))
        self.wait(1)
        
        # 6. Show the formula reference
        formula = MathTex("n = m \\times p", color=YELLOW).to_edge(UR, buff=0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 7. Collapse the 2D grid into a single horizontal 1D vector
        # First clear out the peripheral elements
        self.play(
            FadeOut(player_silhouettes[:10]),
            FadeOut(label_objs),
            FadeOut(formula)
        )
        
        # Animate the grid cells into a single row to visualize the feature vector
        self.play(
            grid.animate.arrange(RIGHT, buff=0.01).scale(0.4).move_to(ORIGIN),
            run_time=2.5
        )
        
        # 8. Mark the vector (using a manual line and text since Brace is restricted)
        vector_line = Line(grid.get_left(), grid.get_right(), color=WHITE).shift(DOWN * 0.3)
        tick_left = Line(vector_line.get_left() + UP*0.1, vector_line.get_left() + DOWN*0.1)
        tick_right = Line(vector_line.get_right() + UP*0.1, vector_line.get_right() + DOWN*0.1)
        
        vector_desc = Text("150-element Feature Vector", font_size=24).next_to(vector_line, DOWN, buff=0.3)
        
        self.play(Create(vector_line), Create(tick_left), Create(tick_right))
        self.play(FadeIn(vector_desc))
        self.wait(2)