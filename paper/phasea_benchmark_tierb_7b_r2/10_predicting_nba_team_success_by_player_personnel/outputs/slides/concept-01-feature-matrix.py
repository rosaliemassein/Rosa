from manim import *

class FeatureMatrixScene(Scene):
    def construct(self):
        # Create a silhouette of 15 basketball players
        player_silhouettes = [Square(color=YELLOW) for _ in range(15)]
        player_silhouettes[0:10].set_color(GREEN).scale(2)

        # Arrange players side by side
        player_silhouettes = VGroup(*player_silhouettes).arrange(RIGHT, buff=0.5).to_edge(LEFT)

        # Create a 10x15 grid of squares
        team_matrix = [[Square(color=WHITE) for _ in range(15)] for _ in range(10)]
        team_matrix = VGroup(*[VGroup(*row) for row in team_matrix]).arrange(DOWN, buff=0.5).next_to(player_silhouettes, RIGHT)

        # Animate 'minutes played' filter passing over players
        minutes_played = MathTex(r"Minutes Played").scale(0.8).next_to(player_silhouettes, UP)
        minutes_animation = AnimationGroup(*[Indicate(player) for player in player_silhouettes[0:10]], lag_ratio=0.2)
        self.play(minutes_animation, Write(minutes_played))
        self.wait(1)

        # Move top 10 players into the grid
        for i in range(10):
            self.play(Transform(player_silhouettes[i], team_matrix[i][i]))

        # Animate labels for 'PTS', 'REB', 'AST', up to 'PIE' appearing above the columns
        labels = [MathTex(rf"{stat}").scale(0.5) for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'FG%', '3P%', 'FT%', 'ORB', 'DRB', 'REB%', 'AST%', 'PIE']]
        labels = VGroup(*labels).arrange(RIGHT, buff=0.5).next_to(team_matrix, UP)

        # Fill the grid cells with varying intensities of color
        for i in range(10):
            for j in range(15):
                team_matrix[i][j].set_color(BLUE)

        # Collapse this 2D grid into a single long horizontal vector of 150 elements
        collapsed_vector = team_matrix.flatten().arrange(RIGHT, buff=0.1)
        collapsed_vector.to_edge(RIGHT)

        # Create an arrow to indicate the transformation
        arrow = Arrow(start=team_matrix.get_edge_center(RIGHT), end=collapsed_vector.get_edge_center(LEFT), color=GREEN)
        self.play(Create(arrow))

        # Finalize the animation
        self.wait(2)