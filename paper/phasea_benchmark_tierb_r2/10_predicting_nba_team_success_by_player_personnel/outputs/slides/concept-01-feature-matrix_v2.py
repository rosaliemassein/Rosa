from manim import *
import numpy as np

class ConceptMatrix(Scene):
    def construct(self):
        # 1. Create player silhouettes (15 players)
        players = VGroup(*[
            VGroup(Circle(radius=0.2, color=GRAY_B, fill_opacity=1), 
                   Triangle(color=GRAY_B, fill_opacity=1).scale(0.3).next_to(ORIGIN, DOWN, buff=0))
            for _ in range(15)
        ]).arrange_in_grid(rows=5, cols=3, buff=0.4).to_edge(LEFT, buff=1)
        
        player_label = Text("Roster (15 Players)", font_size=24).next_to(players, UP)
        self.play(FadeIn(players), Write(player_label))
        self.wait(1)

        # 2. Minutes Played Filter
        filter_rect = Rectangle(height=3.5, width=1.5, color=YELLOW).move_to(players.get_center())
        filter_text = Text("Minutes Filter", color=YELLOW, font_size=20).next_to(filter_rect, UP)
        
        self.play(Create(filter_rect), Write(filter_text))
        
        # Highlight top 10 players (first 10 for simplicity)
        top_10_players = players[:10]
        others = players[10:]
        
        self.play(
            top_10_players.animate.set_color(BLUE),
            others.animate.set_opacity(0.2),
            filter_rect.animate.surround(top_10_players, buff=0.1)
        )
        self.wait(1)

        # 3. Initialize Grid (10 rows for 10 players, 15 columns for stats)
        grid = VGroup(*[
            Square(side_length=0.35, stroke_width=1, fill_opacity=0.5) 
            for _ in range(150)
        ]).arrange_in_grid(rows=10, cols=15, buff=0.05).shift(RIGHT * 2)

        # 4. Animate players sliding into rows
        self.play(
            FadeOut(player_label),
            FadeOut(filter_rect),
            FadeOut(filter_text),
            FadeOut(others),
            ReplacementTransform(top_10_players.copy(), grid[::15]) # Transform players to first column basically
        )
        self.play(FadeIn(grid))
        
        # 5. Column Labels (15 metrics)
        metrics = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "PF", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "ORB", "PIE"]
        labels = VGroup(*[
            Text(m, font_size=12).rotate(45*DEGREES)
            for m in metrics
        ])
        for i, label in enumerate(labels):
            label.next_to(grid[i], UP, buff=0.2)
        
        self.play(Write(labels))
        self.wait(1)

        # 6. Fill grid with "normalized data" (random intensities)
        fill_animations = []
        for cell in grid:
            fill_animations.append(cell.animate.set_fill(BLUE, opacity=np.random.random()))
        
        self.play(*fill_animations, run_time=2)
        
        # 7. Collapse into 1D Vector
        # Reposition grid cells into a single horizontal line
        vector = VGroup(*grid).copy()
        
        formula = MathTex("n = m \\times p", font_size=36).to_edge(UP)
        self.play(Write(formula))

        self.play(
            vector.animate.arrange(RIGHT, buff=0.01).scale(0.3).to_edge(DOWN, buff=1.5),
            FadeOut(labels),
            grid.animate.set_opacity(0.3),
            run_time=2
        )
        
        vector_label = Text("150-element Feature Vector", font_size=20, color=YELLOW).next_to(vector, UP)
        self.play(Write(vector_label))
        
        # Final Highlight of the vector
        self.play(vector.animate.set_color(YELLOW))
        self.wait(2)