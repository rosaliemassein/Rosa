from manim import *
import numpy as np

class FeatureMatrixScene(Scene):
    def construct(self):
        # 1. Setup Silhouettes (15 players)
        def create_player():
            head = Circle(radius=0.15)
            body = Line(DOWN * 0.15, DOWN * 0.4)
            arms = Line(LEFT * 0.2 + DOWN * 0.2, RIGHT * 0.2 + DOWN * 0.2)
            legs = VGroup(Line(DOWN * 0.4, LEFT * 0.15 + DOWN * 0.65), Line(DOWN * 0.4, RIGHT * 0.15 + DOWN * 0.65))
            return VGroup(head, body, arms, legs).set_stroke(width=2)

        players = VGroup(*[create_player() for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0.5)
        players.to_edge(LEFT, buff=1)
        
        self.play(Create(players))
        self.wait(0.5)

        # 2. Minutes Played Filter
        filter_rect = SurroundingRectangle(players[:10], color=YELLOW, buff=0.2)
        filter_label = Text("Top 10 (Minutes Played)", font_size=24).next_to(filter_rect, UP)
        
        self.play(Create(filter_rect), Write(filter_label))
        self.play(players[:10].animate.set_color(GREEN), players[10:].animate.set_opacity(0.2))
        self.wait(1)

        # 3. Create the 10x15 Grid
        grid = VGroup()
        rows, cols = 10, 15
        cell_size = 0.3
        
        for r in range(rows):
            row_group = VGroup(*[Square(side_length=cell_size).set_stroke(WHITE, width=1) for _ in range(cols)])
            row_group.arrange(RIGHT, buff=0.02)
            grid.add(row_group)
        
        grid.arrange(DOWN, buff=0.02).shift(RIGHT * 2.5)

        # 4. Animate Top 10 players into rows
        player_targets = VGroup()
        for i in range(10):
            target = players[i].copy().scale(0.5).next_to(grid[i], LEFT, buff=0.3)
            player_targets.add(target)

        self.play(
            FadeOut(filter_rect),
            FadeOut(filter_label),
            FadeOut(players[10:]),
            ReplacementTransform(players[:10], player_targets),
            Create(grid),
            run_time=2
        )
        self.wait(0.5)

        # 5. Column Labels
        stat_names = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'FG%', '3P%', 'FT%', 'ORB', 'DRB', 'REB%', 'AST%', 'PIE']
        labels = VGroup(*[Text(s, font_size=10) for s in stat_names])
        for i, label in enumerate(labels):
            label.next_to(grid[0][i], UP, buff=0.1)
        
        self.play(Write(labels))
        self.wait(0.5)

        # 6. Fill grid with color intensities
        fill_animations = []
        for row in grid:
            for cell in row:
                intensity = np.random.uniform(0.2, 0.9)
                fill_animations.append(cell.animate.set_fill(BLUE, opacity=intensity))
        
        self.play(*fill_animations, run_time=1.5)
        self.wait(1)

        # 7. Collapse into a long horizontal vector
        # Flatten all cells into a single list
        flat_cells = VGroup(*[cell for row in grid for cell in row])
        
        vector_cell_width = 0.06
        # Create the visual target for the 150 elements
        vector = VGroup(*[Rectangle(width=vector_cell_width, height=0.4, fill_opacity=cell.fill_opacity, fill_color=BLUE, stroke_width=0.1) 
                         for cell in flat_cells])
        vector.arrange(RIGHT, buff=0.01).to_edge(DOWN, buff=1.5)
        
        formula = MathTex("n = m \\times p").next_to(vector, UP, buff=0.5)

        self.play(
            FadeOut(labels),
            FadeOut(player_targets),
            ReplacementTransform(flat_cells, vector),
            Write(formula),
            run_time=2.5
        )
        self.wait(2)