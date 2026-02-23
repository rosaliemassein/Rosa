from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # Configuration and colors to avoid undefined identifier errors
        COLOR_GREEN = "#83C167"
        COLOR_WHITE = "#FFFFFF"
        COLOR_BLUE_DARK = "#1C758A"
        COLOR_BLUE_LIGHT = "#58C4DD"
        COLOR_BG = "#1a1a1a"
        COLOR_PALETTE = ["#1C758A", "#29ABCA", "#58C4DD", "#73D5E3", "#B1E19A", "#C9E2AE"]
        
        self.camera.background_color = COLOR_BG
        
        # 1. Create a silhouette of 15 basketball players on the left
        players = VGroup(*[
            Circle(radius=0.15, color=COLOR_WHITE, fill_opacity=0.2).set_fill(COLOR_WHITE) 
            for _ in range(15)
        ]).arrange(DOWN, buff=0.15).to_edge(LEFT, buff=1)
        
        player_tags = VGroup(*[
            Text(f"Player {i+1}", font_size=14).next_to(players[i], LEFT, buff=0.1)
            for i in range(15)
        ])
        
        self.play(Create(players), FadeIn(player_tags))
        self.wait(0.5)
        
        # 2. Animate a 'minutes played' filter passing over them
        filter_line = Line(LEFT, RIGHT, color=COLOR_GREEN).set_width(2.5).move_to(players.get_top() + UP * 0.3)
        self.play(Create(filter_line))
        self.play(filter_line.animate.move_to(players[9].get_center()), run_time=1.5)
        
        # Highlight top 10
        top_10 = players[:10]
        others = players[10:]
        self.play(
            top_10.animate.set_color(COLOR_GREEN).set_fill(COLOR_GREEN, opacity=0.7),
            others.animate.set_opacity(0.1),
            filter_line.animate.set_opacity(0)
        )
        
        # 3. Create the 10x15 grid (10 rows for players, 15 columns for stats)
        rows, cols = 10, 15
        cell_size = 0.3
        grid = VGroup()
        cells_list = []
        
        for r in range(rows):
            row_group = VGroup()
            for c in range(cols):
                sq = Square(side_length=cell_size, stroke_width=1, color=COLOR_WHITE)
                sq.move_to([c * cell_size, -r * cell_size, 0])
                # Randomly color cells to simulate data
                intensity = np.random.rand()
                idx = int(intensity * (len(COLOR_PALETTE) - 1))
                sq.set_fill(COLOR_PALETTE[idx], opacity=0.8)
                row_group.add(sq)
                cells_list.append(sq)
            grid.add(row_group)
        
        grid.center().shift(RIGHT * 1.5)
        
        # 4. Players slide into the rows of the grid
        player_movements = []
        for i in range(10):
            player_movements.append(top_10[i].animate.scale(0.4).move_to(grid[i].get_left() + LEFT * 0.4))
        
        self.play(
            *player_movements,
            FadeOut(player_tags),
            FadeOut(others),
            run_time=1.5
        )
        self.play(Create(grid))
        
        # 5. Column Labels
        stat_names = ["PTS", "REB", "AST", "STL", "BLK", "FT%", "3P%", "eFG", "sFT", "TOV", "S%", "B%", "MP", "PIE", "USG"]
        column_labels = VGroup()
        for i, name in enumerate(stat_names):
            lbl = Text(name, font_size=10).next_to(grid[0][i], UP, buff=0.1)
            lbl.rotate(45 * DEGREES)
            column_labels.add(lbl)
            
        self.play(Write(column_labels))
        self.wait(1)
        
        # 6. Collapse the 2D grid into a single horizontal vector
        vector_elements = VGroup(*[
            Square(side_length=0.08, stroke_width=0.1, fill_opacity=0.8).set_fill(cells_list[i].get_fill_color())
            for i in range(len(cells_list))
        ]).arrange(RIGHT, buff=0.01).to_edge(DOWN, buff=1.2)
        
        # Group everything to transform
        all_cells = VGroup(*cells_list)
        
        self.play(
            ReplacementTransform(all_cells, vector_elements),
            FadeOut(column_labels),
            FadeOut(top_10),
            grid.animate.set_stroke(opacity=0),
            run_time=2.5
        )
        
        # 7. Add Formula and Narration
        formula = MathTex("n = m \\times p", color=COLOR_WHITE).next_to(vector_elements, UP, buff=0.5)
        calc = Text("150 = 10 players x 15 metrics", font_size=20, color=COLOR_GREEN).next_to(formula, DOWN)
        
        narration = Text(
            "The team identity is boiled down to a 150-element feature vector.",
            font_size=22,
            color=COLOR_WHITE
        ).to_edge(UP, buff=1)
        
        self.play(Write(formula))
        self.play(FadeIn(calc))
        self.play(Write(narration))
        
        self.wait(3)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    scene = ConceptAnimation()
    scene.render()