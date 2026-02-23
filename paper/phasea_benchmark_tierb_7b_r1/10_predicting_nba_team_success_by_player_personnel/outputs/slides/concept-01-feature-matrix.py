from manim import *

class FeatureMatrixScene(Scene):
    def construct(self):
        # Create the silhouette of players
        players = [Circle(radius=0.5, color=YELLOW) for _ in range(15)]
        player_group = VGroup(*players).arrange_in_grid(rows=1, cols=15)
        player_group.to_edge(LEFT)

        # Create the minutes played filter
        minutes_filter = Rectangle(width=3, height=0.5, color=BLUE)
        minutes_filter.shift(LEFT * 2)

        # Animate the minutes played filter passing over players
        self.play(Create(player_group))
        self.wait(0.5)
        for i in range(15):
            self.play(minutes_filter.animate.shift(RIGHT))
            self.wait(0.2)
        self.play(FadeOut(minutes_filter))

        # Highlight the top 10 players
        for i in range(15):
            if i < 10:
                self.play(players[i].animate.set_color(RED))

        # Slide the top 10 players into the feature matrix
        feature_matrix = [[Square(side_length=0.5, color=WHITE) for _ in range(15)] for _ in range(10)]
        feature_matrix_group = VGroup(*sum(feature_matrix, [])).arrange_in_grid(rows=10, cols=15)
        feature_matrix_group.shift(RIGHT * 3)

        self.play(Transform(player_group, VGroup(*[players[i] if i < 10 else Circle(radius=0.5, color=WHITE) for i in range(15)])))
        self.play(Create(feature_matrix_group))

        # Add labels for performance metrics
        metrics = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PIE']
        metric_labels = [Text(metric) for metric in metrics]
        metric_group = VGroup(*metric_labels).arrange_in_grid(rows=1, cols=len(metrics))
        metric_group.shift(UP * 2.5)
        self.play(Create(metric_group))

        # Fill the grid cells with varying intensities of color
        for i in range(10):
            for j in range(15):
                color_intensity = (i * 15 + j) % 3
                if color_intensity == 0:
                    feature_matrix_group[i][j].set_color(BLUE)
                elif color_intensity == 1:
                    feature_matrix_group[i][j].set_color(GREEN)
                else:
                    feature_matrix_group[i][j].set_color(RED)

        self.wait(2)

        # Collapse the 2D grid into a single long horizontal vector
        collapsed_vector = VGroup(*feature_matrix_group).arrange_in_line()
        collapsed_vector.shift(RIGHT * 3)
        self.play(Transform(feature_matrix_group, collapsed_vector))

        self.wait(2)