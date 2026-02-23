from manim import *

class FeatureMatrixScene(Scene):
    def construct(self):
        # Create player silhouettes
        players = [Square(color=WHITE).scale(0.5) for _ in range(15)]
        player_labels = [Text(f"Player {i+1}", font_size=20).next_to(players[i], LEFT) for i in range(15)]

        # Arrange players on the left side
        VGroup(*players, *player_labels).arrange(DOWN).to_edge(LEFT)

        # Create team matrix grid
        rows, cols = 10, 15
        matrix = [[Square(color=WHITE).scale(0.2) for _ in range(cols)] for _ in range(rows)]
        matrix_group = VGroup(*[VGroup(*row).arrange(DOWN) for row in matrix]).next_to(VGroup(*player_labels), RIGHT)

        # Animate minutes played filter passing over players
        minutes_filter = Rectangle(width=1, height=0.5, color=BLUE).next_to(players[5], LEFT)
        self.play(Create(minutes_filter))
        self.wait(0.2)
        self.play(FadeOut(minutes_filter))
        self.wait(0.2)

        # Highlight top 10 players
        top_10_players = [players[i] for i in range(5, 15)]
        self.play(*[Transform(player, player.set_color(GREEN)) for player in top_10_players])

        # Slide top 10 players into rows of the grid
        for i, player in enumerate(top_10_players):
            self.play(Transform(player, matrix[i][4].copy().set_color(GREEN)))

        # Add labels for stats
        stat_labels = [Text(label, font_size=20).next_to(matrix[0][i], UP) for i, label in enumerate(['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PIE'])]
        stat_group = VGroup(*stat_labels).next_to(matrix_group, UP)
        self.play(Create(stat_group))

        # Fill grid cells with varying intensities of color
        for i in range(rows):
            for j in range(cols):
                cell = matrix[i][j]
                if j >= 4:
                    cell.set_color(BLUE if i < 5 else YELLOW)
                self.play(Transform(cell, cell.copy().set_color(BLUE if i < 5 else YELLOW)))

        # Collapse the 2D grid into a single long horizontal vector
        vector = VGroup(*[Square(color=WHITE).scale(0.1) for _ in range(rows*cols)]).arrange(RIGHT)
        vector.to_edge(RIGHT)

        for i in range(rows*cols):
            cell = matrix[i // cols][i % cols]
            self.play(Transform(vector[i], cell.copy()))

        self.wait()