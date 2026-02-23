from manim import *

class FeatureMatrix(Scene):
    def construct(self):
        # Title and narration
        title = Text("Feature Matrix for Team Success Prediction")
        self.play(Write(title))
        self.wait(2)

        # Description
        description = Text("Teams are represented as a matrix of player statistics.")
        self.play(FadeIn(description))
        self.wait(3)

        # Players silhouette
        players = VGroup(*[Square(color=BLUE) for _ in range(15)]).arrange(RIGHT, buff=0.2)
        players.next_to(description, DOWN)
        self.play(FadeIn(players))
        self.wait(1)

        # Minutes played filter
        minutes_played = MathTex(r"minutes \, played")
        minutes_filter = Rectangle(width=0.5, height=15).next_to(players, LEFT)
        minutes_filter.set_color(GREEN)
        self.play(Create(minutes_filter), Write(minutes_played))
        self.wait(1)

        # Highlight top 10 players
        top_players = players[:10]
        for player in top_players:
            self.play(FadeIn(player))
        self.wait(1)

        # Move top 10 players to matrix
        matrix = VGroup(*[Square(color=WHITE) for _ in range(10*15)]).arrange(RIGHT, buff=0.2, row_buff=0.5)
        matrix.next_to(title, DOWN).shift(UP * 2)
        for i in range(len(top_players)):
            player = top_players[i]
            matrix_row = VGroup(*[Square(color=WHITE) for _ in range(15)]).next_to(matrix, RIGHT)
            matrix.add(matrix_row)
            self.play(Transform(player, matrix_row[i]))
        self.wait(1)

        # Label columns
        labels = VGroup(*[Text(label) for label in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PIE']]).arrange(DOWN, buff=0.5)
        labels.next_to(matrix, LEFT).shift(LEFT * 1.5)
        self.play(FadeIn(labels))
        self.wait(1)

        # Fill matrix with color
        for i in range(len(matrix)):
            for j in range(15):
                cell = matrix[i][j]
                if cell not in top_players:
                    self.play(FadeIn(cell))
        self.wait(1)

        # Collapse matrix into vector
        vector = VGroup(*[Square(color=WHITE) for _ in range(150)]).arrange(RIGHT, buff=0.2)
        vector.shift(DOWN * 3)
        self.play(FadeIn(vector))
        self.wait(1)

        # Animation of collapse
        for i in range(len(matrix)):
            for j in range(15):
                cell = matrix[i][j]
                vector_cell = vector[(i % 10) * 15 + j]
                if cell not in top_players:
                    self.play(Transform(cell, vector_cell))
        self.wait(2)

        # Final narration
        final_text = Text("This vector of 150 elements enters the model for prediction.")
        final_text.next_to(vector, DOWN)
        self.play(Write(final_text))
        self.wait(3)

        # Cleanup
        self.play(FadeOut(title), FadeOut(description), FadeOut(players), FadeOut(minutes_filter), FadeOut(labels), FadeOut(matrix), FadeOut(vector), FadeOut(final_text))
        self.wait(1)