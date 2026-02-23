from manim import *
import numpy as np

class FeatureMatrix(Scene):
    def construct(self):
        # 1. Setup Narrator Text (Voiceover representation)
        voice_text = Text(
            "Representing teams as high-dimensional matrices...", 
            font_size=24
        ).to_edge(UP)
        self.play(Write(voice_text))
        self.wait(1)

        # 2. Players silhouettes (15 players)
        def create_player():
            head = Circle(radius=0.15, fill_opacity=1, color=GRAY_A)
            body = RoundedRectangle(corner_radius=0.1, width=0.4, height=0.5, fill_opacity=1, color=GRAY_A).next_to(head, DOWN, buff=0.05)
            return VGroup(head, body).scale(0.7)

        players = VGroup(*[create_player() for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0.5)
        players.center().shift(LEFT * 3)
        self.play(Create(players))
        self.wait(1)

        # 3. Minutes Played Filter
        filter_rect = Rectangle(height=6, width=0.5, color=YELLOW, stroke_width=2)
        filter_rect.move_to(players.get_left() + LEFT * 0.5)
        filter_label = Text("Minutes Played", font_size=20, color=YELLOW).next_to(filter_rect, UP)

        self.play(Create(filter_rect), Write(filter_label))
        self.play(filter_rect.animate.move_to(players.get_right() + RIGHT * 0.5), run_time=2)
        
        # Highlight top 10
        top_10_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        top_players = VGroup(*[players[i] for i in top_10_indices])
        other_players = VGroup(*[players[i] for i in range(10, 15)])
        
        self.play(
            top_players.animate.set_color(BLUE),
            other_players.animate.set_opacity(0.2),
            FadeOut(filter_rect),
            FadeOut(filter_label)
        )
        self.wait(1)

        # 4. Create Matrix (10x15)
        grid_cells = VGroup(*[
            Square(side_length=0.3, stroke_width=1, fill_opacity=0).set_color(WHITE)
            for _ in range(10 * 15)
        ]).arrange_in_grid(rows=10, cols=15, buff=0.05)
        grid_cells.center().shift(RIGHT * 2)

        # Slide top 10 players into rows
        row_targets = [grid_cells[i*15] for i in range(10)]
        
        self.play(
            voice_text.animate.become(Text("Top 10 players form the rows...", font_size=24).to_edge(UP)),
            FadeOut(other_players),
            *[top_players[i].animate.scale(0.4).move_to(row_targets[i].get_left() + LEFT * 0.4) for i in range(10)],
            Create(grid_cells)
        )
        self.wait(1)

        # 5. Labels for columns
        col_labels_text = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "PF", "PIE", "FG%", "3P%", "FT%", "OREB", "DREB", "MIN", "EFF"]
        col_labels = VGroup(*[
            Text(txt, font_size=12).next_to(grid_cells[i], UP, buff=0.2).rotate(45*DEGREES)
            for i, txt in enumerate(col_labels_text)
        ])
        
        self.play(Write(col_labels))
        self.wait(1)

        # 6. Fill grid cells with intensities
        animations = []
        for cell in grid_cells:
            random_val = np.random.rand()
            animations.append(cell.animate.set_fill(BLUE, opacity=random_val))
        
        self.play(
            LaggedStart(*animations, lag_ratio=0.01),
            voice_text.animate.become(Text("15 performance metrics create the features.", font_size=24).to_edge(UP))
        )
        self.wait(1)

        # 7. Formula display
        formula = MathTex("n = m \\times p", color=YELLOW).next_to(grid_cells, DOWN, buff=0.5)
        formula_desc = Text("10 players x 15 stats = 150 features", font_size=20).next_to(formula, DOWN)
        self.play(Write(formula), Write(formula_desc))
        self.wait(1)

        # 8. Collapse Matrix into Vector
        vector_cells = grid_cells.copy()
        vector_target = VGroup(*[
            Square(side_length=0.08, stroke_width=0.5, fill_opacity=cell.get_fill_opacity(), fill_color=BLUE)
            for cell in grid_cells
        ]).arrange(RIGHT, buff=0.01).center().to_edge(DOWN, buff=1.5)

        self.play(
            FadeOut(top_players),
            FadeOut(col_labels),
            FadeOut(formula),
            FadeOut(formula_desc),
            FadeOut(voice_text),
            Transform(vector_cells, vector_target),
            run_time=2
        )
        
        final_label = Text("150-Element Feature Vector", font_size=24).next_to(vector_target, UP)
        self.play(Write(final_label))
        
        # 9. Conclusion
        model_box = Rectangle(width=3, height=1.5, color=GREEN).shift(UP * 1)
        model_text = Text("ML Model", color=GREEN).move_to(model_box)
        
        self.play(
            Create(model_box),
            Write(model_text),
            vector_cells.animate.scale(0.5).next_to(model_box, DOWN),
            final_label.animate.scale(0.8).next_to(model_box, UP)
        )
        
        self.play(vector_cells.animate.move_to(model_box.get_center()).set_opacity(0))
        self.wait(2)

        # Final cleanup
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)

if __name__ == "__main__":
    scene = FeatureMatrix()
    scene.render()