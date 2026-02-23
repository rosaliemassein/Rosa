import numpy as np
from manim import *

class TeamFeatureMatrix(Scene):
    def construct(self):
        # 1. Background Setup: 10x15 grid
        # We create the grid first but keep it invisible/faded
        grid = VGroup(*[
            Square(side_length=0.35, stroke_width=1, fill_opacity=0).set_color(WHITE)
            for _ in range(150)
        ]).arrange_in_grid(rows=10, cols=15, buff=0.05).shift(RIGHT * 1.5)

        # 2. Silhouettes of 15 players
        # Using a simple shape to represent a silhouette
        def get_silhouette():
            head = Circle(radius=0.12, color=BLUE, fill_opacity=1)
            body = Polygon([-0.15, -0.4, 0], [0.15, -0.4, 0], [0.1, -0.12, 0], [-0.1, -0.12, 0], 
                           color=BLUE, fill_opacity=1)
            return VGroup(head, body)

        players = VGroup(*[get_silhouette().scale(0.6) for _ in range(15)])
        players.arrange_in_grid(rows=5, cols=3, buff=0.4).to_edge(LEFT, buff=0.5)

        # Narration start
        self.play(FadeIn(players))
        self.wait(1)

        # 3. 'Minutes played' filter passing over them
        filter_box = Rectangle(width=0.5, height=5, color=YELLOW, stroke_width=2)
        filter_box.move_to(players.get_left() + LEFT * 0.5)
        
        self.play(filter_box.animate.move_to(players.get_right() + RIGHT * 0.5), run_time=2)

        # Highlight top 10, dim the rest
        top_10 = players[:10]
        others = players[10:]
        self.play(
            top_10.animate.set_color(GOLD),
            others.animate.set_opacity(0.2),
            FadeOut(filter_box)
        )
        self.wait(1)

        # 4. Players slide into the rows of the grid
        # Align players to the left of the rows they represent
        row_indicators = VGroup(*[
            Dot(radius=0.08, color=GOLD).move_to(grid[i*15].get_left() + LEFT * 0.3)
            for i in range(10)
        ])

        self.play(
            ReplacementTransform(top_10.copy(), row_indicators),
            Create(grid),
            run_time=2
        )

        # 5. Column Labels
        metrics_list = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "FG%", "FT%", "3P%", "ORB", "DRB", "MIN", "OFF", "DEF", "PIE"]
        labels = VGroup(*[
            Text(m, font_size=10).next_to(grid[i], UP, buff=0.1).rotate(45*DEGREES)
            for i, m in enumerate(metrics_list)
        ])
        
        self.play(Write(labels))
        self.wait(1)

        # 6. Fill grid cells with intensities
        fill_anims = []
        for i, sq in enumerate(grid):
            # Generate a pseudo-random intensity
            intensity = (np.sin(i * 0.5) + 1) / 2 
            fill_anims.append(sq.animate.set_fill(BLUE, opacity=intensity))
        
        self.play(*fill_anims, run_time=2)
        self.wait(2)

        # 7. Collapse 2D grid into single horizontal vector
        # Scale down squares to fit 150 in one line
        vector = VGroup(*[
            Square(side_length=0.08, stroke_width=0.2, fill_opacity=sq.get_fill_opacity(), fill_color=BLUE)
            for sq in grid
        ]).arrange(RIGHT, buff=0.01).move_to(DOWN * 2)

        formula = MathTex("n = 10 \\times 15 = 150", font_size=36).next_to(vector, UP)

        self.play(
            FadeOut(players),
            FadeOut(labels),
            FadeOut(row_indicators),
            ReplacementTransform(grid, vector),
            Write(formula),
            run_time=2
        )
        self.wait(3)

# Note: Ensure numpy is installed as 'np' is used for generating intensity.