from manim import *

class FeatureMatrix(Scene):
    def construct(self):
        # Create silhouette of 15 basketball players
        player_silhouettes = VGroup(*[Square(side_length=0.5).to_edge(LEFT) for _ in range(15)])
        player_silhouettes.shift(RIGHT * 3)

        # Create 10x15 grid of squares
        matrix_grid = VGroup(*[VGroup(*[Square(side_length=0.4) for _ in range(15)]) for _ in range(10)])
        matrix_grid.arrange(RIGHT, buff=0.25).arrange(DOWN, buff=0.25)
        matrix_grid.shift(RIGHT * 1)

        # Animate 'minutes played' filter passing over players
        self.play(FadeIn(player_silhouettes))
        for i in range(10):
            self.play(Indicate(player_silhouettes[i]))
        self.wait(0.5)

        # Move top 10 players into the grid
        top_players = player_silhouettes[:10]
        self.play(FadeOut(player_silhouettes[10:]))
        self.play(Transform(VGroup(*top_players), matrix_grid))

        # Create labels for 'PTS', 'REB', 'AST' up to 'PIE' above the columns
        labels = VGroup(*[Text(label, font_size=14) for label in ['PTS', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'MPG', 'FG%', '3P%', 'FT%', 'REB%', 'AST%', 'PIE']])
        labels.arrange(DOWN, buff=0.2).to_edge(LEFT)
        self.play(FadeIn(labels))

        # Fill the grid cells with varying intensities of color
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
        for i in range(10):
            for j in range(15):
                color = colors[i % len(colors)]
                matrix_grid[i][j].set_fill(color, opacity=0.8)

        # Collapse 2D grid into a single long horizontal vector of 150 elements
        flattened_vector = VGroup(*[matrix_grid[i][j] for i in range(10) for j in range(15)])
        flattened_vector.arrange(RIGHT, buff=0.2)
        flattened_vector.shift(LEFT * 1)

        self.play(FadeIn(flattened_vector))
        self.wait(2)