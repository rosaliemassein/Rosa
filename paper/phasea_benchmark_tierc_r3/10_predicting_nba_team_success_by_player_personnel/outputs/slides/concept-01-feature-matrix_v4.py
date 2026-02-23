from manim import *
import numpy as np

class ConceptMatrix(Scene):
    def construct(self):
        # 1. Setup Grid and Formula
        team_shape = (10, 15) # 10 players, 15 metrics
        unit_size = 0.35
        grid = VGroup(*[
            Square(side_length=unit_size, color=BLUE, stroke_width=2) 
            for _ in range(team_shape[0] * team_shape[1])
        ]).arrange_in_grid(rows=team_shape[0], cols=team_shape[1], buff=0.05)
        
        formula = MathTex("n = m \\times p", color=WHITE).to_corner(UP + RIGHT)
        self.add(formula)

        # 2. Silhouettes of 15 players
        # Using a simple shape representation for silhouettes
        player_silhouettes = VGroup(*[
            VGroup(
                Circle(radius=0.12, fill_opacity=1),
                Triangle(fill_opacity=1).scale(0.2).stretch_to_fit_width(0.3).stretch_to_fit_height(0.4)
            ).arrange(DOWN, buff=0.02)
            for _ in range(15)
        ]).arrange(DOWN, buff=0.08).to_edge(LEFT, buff=0.5)
        
        for p in player_silhouettes:
            p.set_color(GRAY)
            
        self.play(FadeIn(player_silhouettes))

        # 3. 'Minutes Played' filter
        minutes_filter = Rectangle(width=0.8, height=0.5, color=YELLOW, stroke_width=4)
        minutes_filter.move_to(player_silhouettes[0])
        
        self.play(Create(minutes_filter))
        # Highlight top 10 players
        self.play(
            minutes_filter.animate.move_to(player_silhouettes[9]),
            *[player_silhouettes[i].animate.set_color(WHITE) for i in range(10)],
            run_time=2
        )
        self.play(FadeOut(minutes_filter))
        
        # Fade out the bottom 5 players
        self.play(FadeOut(player_silhouettes[10:]))

        # 4. Players slide into the rows of the grid
        # Replacing DrawBorderThenFill with Create
        self.play(Create(grid))
        
        move_animations = []
        for i in range(10):
            # i * 15 gets the first cell of each row in a row-major grid
            target_pos = grid[i * 15].get_left() + LEFT * 0.4
            move_animations.append(player_silhouettes[i].animate.scale(0.6).move_to(target_pos))
        
        self.play(*move_animations)

        # 5. Add performance metric labels
        metric_names = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FTM', 'FTA', 'FG3M', 'FG3A', 'PER', 'PIE', 'MIN', '+/-', 'TS%']
        metrics_labels = VGroup()
        for i, name in enumerate(metric_names):
            label = Text(name, font_size=10).next_to(grid[i], UP, buff=0.1).rotate(45 * DEGREES)
            metrics_labels.add(label)
        
        self.play(Write(metrics_labels))

        # 6. Fill grid cells with varying intensities
        fill_animations = []
        for cell in grid:
            intensity = np.random.uniform(0.3, 0.9)
            fill_animations.append(cell.animate.set_fill(BLUE, opacity=intensity))
        
        self.play(*fill_animations, run_time=2)
        self.wait(1)

        # 7. Collapse grid into a single long horizontal vector
        vector = VGroup(*[
            Square(side_length=0.08, stroke_width=0.5, fill_opacity=np.random.uniform(0.3, 0.9), fill_color=BLUE)
            for _ in range(150)
        ]).arrange(RIGHT, buff=0.01).move_to(DOWN * 0.5)
        
        vector_text = Text("150-Element Feature Vector", font_size=20).next_to(vector, UP)

        self.play(
            FadeOut(player_silhouettes[:10]),
            FadeOut(metrics_labels),
            FadeOut(formula),
            Transform(grid, vector),
            Write(vector_text),
            run_time=3
        )
        self.wait(2)

        # Final caption
        end_text = Text("Structured data for machine learning models.", font_size=18).next_to(vector, DOWN, buff=0.5)
        self.play(FadeIn(end_text))
        self.wait(2)