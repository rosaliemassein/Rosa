from manim import *
import numpy as np

class Concept01FeatureMatrix(Scene):
    def construct(self):
        voice_text = "To predict a team's success, we can't just look at their total points. Instead, we represent each team as a high-dimensional matrix. We take the top ten players—ranked by minutes played—and for each one, we track fifteen distinct performance metrics. This creates a feature vector where the identity of the team is boiled down to the individual fingerprints of its rotation players."
        
        # 1. Create player silhouettes
        players = VGroup()
        for i in range(15):
            head = Circle(radius=0.12, color=WHITE)
            body = Polygon([-0.2, -0.4, 0], [0.2, -0.4, 0], [0.15, 0, 0], [-0.15, 0, 0], color=WHITE)
            player = VGroup(head, body).scale(0.8)
            players.add(player)
            
        players.arrange(DOWN, buff=0.1).to_edge(LEFT, buff=0.5)
        
        self.play(FadeIn(players))
        self.wait(1)

        # 2. Minutes played filter
        filter_rect = Rectangle(width=0.8, height=players[:10].get_height() + 0.2, color=YELLOW)
        filter_rect.move_to(players[:10].get_center())
        filter_text = Text("Top 10", font_size=20, color=YELLOW).next_to(filter_rect, UP)
        
        self.play(Create(filter_rect), Write(filter_text))
        self.play(players[10:].animate.set_opacity(0.2))
        self.wait(1)

        # 3. Create the 10x15 grid (Team Matrix)
        matrix_rows = 10
        matrix_cols = 15
        cell_size = 0.3
        grid = VGroup()
        for r in range(matrix_rows):
            for c in range(matrix_cols):
                square = Square(side_length=cell_size, stroke_width=1)
                grid.add(square)
        grid.arrange_in_grid(rows=matrix_rows, cols=matrix_cols, buff=0.05)
        grid.shift(RIGHT * 2)
        
        # 4. Slide top 10 players into rows
        player_anims = []
        for i in range(10):
            target = grid[i * matrix_cols].get_left() + LEFT * 0.4
            player_anims.append(players[i].animate.scale(0.4).move_to(target))
        
        self.play(
            *player_anims,
            FadeOut(filter_rect),
            FadeOut(filter_text),
            FadeOut(players[10:]),
            Create(grid)
        )

        # 5. Stats labels
        stats = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '3PM', '3PA', 'FTM', 'FTA', 'ORB', 'DRB', '+/-', 'PIE']
        stat_labels = VGroup()
        for i, s in enumerate(stats):
            label = Text(s, font_size=10).rotate(60 * DEGREES)
            label.move_to(grid[i].get_top() + UP * 0.3)
            stat_labels.add(label)
        
        self.play(Write(stat_labels))
        self.wait(1)

        # 6. Fill grid with intensities (Custom color list to avoid BLUE_A/BLUE_E errors)
        colors = ["#D7EEFF", "#A6D8FF", "#75C1FF", "#44AAFF", "#1393FF", "#0077E6", "#005BB3"]
        fill_anims = []
        for cell in grid:
            color_idx = np.random.randint(0, len(colors))
            fill_anims.append(cell.animate.set_fill(colors[color_idx], opacity=0.8))
        
        self.play(*fill_anims, run_time=2)
        
        # 7. Formula reference
        formula = MathTex("n = m \\times p").to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # 8. Collapse to horizontal vector
        self.play(
            FadeOut(stat_labels),
            FadeOut(players[:10]),
            FadeOut(formula)
        )
        
        vector_grid = grid.copy()
        self.play(
            vector_grid.animate.arrange(RIGHT, buff=0.01).scale(0.3).move_to(ORIGIN),
            run_time=2
        )
        
        # Manual bracket replacement (since Brace is disallowed)
        bracket_line = Line(vector_grid.get_left() + DOWN * 0.4, vector_grid.get_right() + DOWN * 0.4)
        tick_l = Line(bracket_line.get_left() + UP * 0.1, bracket_line.get_left() + DOWN * 0.1)
        tick_r = Line(bracket_line.get_right() + UP * 0.1, bracket_line.get_right() + DOWN * 0.1)
        bracket = VGroup(bracket_line, tick_l, tick_r)
        
        vector_label = Text("150-element Vector", font_size=24).next_to(bracket, DOWN)
        
        self.play(Create(bracket), Write(vector_label))
        
        # Display narration snippet
        narration = Text(voice_text[:60] + "...", font_size=18).to_edge(DOWN, buff=0.4)
        self.play(Write(narration))
        self.wait(2)