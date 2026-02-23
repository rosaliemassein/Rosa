from manim import *

class FeatureMatrixAnimation(Scene):
    def construct(self):
        # Create the 10x15 grid
        team_matrix = [[Square() for _ in range(15)] for _ in range(10)]
        team_matrix_grid = VGroup(*team_matrix)
        team_matrix_grid.arrange_in_grid(rows=10, cols=15, buff=0.5)
        team_matrix_grid.shift(LEFT*2)

        # Create player silhouettes
        players = [Square() for _ in range(15)]
        players_group = VGroup(*players)
        players_group.arrange_in_grid(rows=1, cols=15, buff=0.5)
        players_group.shift(LEFT*2)

        # Animate 'minutes played' filter passing over the players
        for player in players:
            self.play(Create(player))
        minutes_filter = Rectangle(width=2, height=0.5).next_to(players_group, UP)
        self.play(Create(minutes_filter))
        for player in players[:10]:
            self.play(Transform(player, player.set_fill(GREEN, opacity=0.5)))
        self.wait()

        # Move the top 10 players into the rows of the grid
        for i in range(15):
            self.play(Transform(players[i], players_group[i*10:(i+1)*10][0]))
        self.wait()

        # Add labels for 'PTS', 'REB', 'AST', up to 'PIE' above the columns
        metrics = MathTex(r"\text{PTS}", r"\text{REB}", r"\text{AST}", r"\text{STL}", r"\text{BLK}", r"\text{TUR}", 
                          r"\text{TO}", r"\text{PF}", r"\text{FGP}", r"\text{FTP}", r"\text{TP3%}", r"\text{PIE}").arrange(RIGHT, buff=0.5)
        metrics_group = VGroup(*metrics).move_to(team_matrix_grid.get_top())
        self.play(Create(metrics_group))
        self.wait()

        # Fill the grid cells with varying intensities of color
        for i in range(10):
            for j in range(15):
                cell = team_matrix_grid[i][j]
                color_intensity = (i*15 + j) / 150
                cell.set_fill(BLUE, opacity=color_intensity)
        self.wait()

        # Collapse the 2D grid into a single long horizontal vector
        vector = VGroup(*[Arrow(DOWN, RIGHT).next_to(cell[-1], DOWN) for cell in team_matrix_grid])
        vector_group = VGroup(*vector).next_to(team_matrix_grid, DOWN)
        self.play(Create(vector_group))
        self.wait()