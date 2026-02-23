from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create a 5x5 pixel grid
        grid = VGroup()
        pixel_values = [np.random.choice([0, 1]) for _ in range(25)]
        for val in pixel_values:
            sq = Square(side_length=0.5, fill_opacity=float(val), color=WHITE)
            txt = MathTex(str(val), font_size=24).move_to(sq.get_center())
            grid.add(VGroup(sq, txt))
        grid.arrange_in_grid(rows=5, cols=5, buff=0.1).shift(LEFT * 4)

        grid_label = Text("5x5 Grid", font_size=24).next_to(grid, UP)
        self.play(FadeIn(grid), Write(grid_label))
        self.wait(1)

        # 2. Flatten to vector
        vector = grid.copy()
        self.play(
            vector.animate.arrange(DOWN, buff=0.05).scale(0.4).shift(RIGHT * 5),
            FadeOut(grid_label),
            grid.animate.scale(0.7).to_edge(LEFT, buff=0.5)
        )
        
        vec_rect = SurroundingRectangle(vector, color=BLUE, buff=0.1)
        vec_label = Text("1D Vector (25 values)", font_size=20).next_to(vec_rect, UP)
        self.play(Create(vec_rect), Write(vec_label))

        # 3. Neural Network layers
        hidden_layer = VGroup(*[Circle(radius=0.12, color=BLUE, fill_opacity=0.5) for _ in range(8)])
        hidden_layer.arrange(DOWN, buff=0.2).shift(RIGHT * 1.5)
        
        output_layer = VGroup(*[Circle(radius=0.1, color=GREEN, fill_opacity=0.5) for _ in range(25)])
        output_layer.arrange(DOWN, buff=0.05).scale(0.8).shift(RIGHT * 4.5)
        
        # Connections (Sampling some lines for visual clarity)
        conn_in_hidden = VGroup()
        for i in [0, 6, 12, 18, 24]:
            for h in hidden_layer:
                conn_in_hidden.add(Line(vector[i].get_right(), h.get_left(), stroke_width=0.5, stroke_opacity=0.2))
        
        conn_hidden_out = VGroup()
        for h in hidden_layer:
            for o in [0, 6, 12, 18, 24]:
                conn_hidden_out.add(Line(h.get_right(), output_layer[o].get_left(), stroke_width=0.5, stroke_opacity=0.2))

        nn_title = Text("Deep Q-Network", font_size=24).next_to(output_layer, UP).shift(LEFT * 1.5)
        self.play(
            FadeIn(hidden_layer),
            FadeIn(output_layer),
            Create(conn_in_hidden),
            Create(conn_hidden_out),
            Write(nn_title)
        )

        # 4. Highlight highest value output node
        target_idx = 12
        self.play(
            Indicate(output_layer[target_idx], scale_factor=2, color=YELLOW),
            output_layer[target_idx].animate.set_color(YELLOW)
        )
        
        action_label = Text(f"Flip Pixel {target_idx}", font_size=18, color=YELLOW).next_to(output_layer[target_idx], RIGHT)
        self.play(Write(action_label))
        
        # 5. Flip corresponding pixel in the original grid
        original_pixel = grid[target_idx]
        new_val = 1 - pixel_values[target_idx]
        
        # Create the replacement pixel
        flipped_sq = Square(side_length=0.5 * 0.7, fill_opacity=float(new_val), color=RED).move_to(original_pixel[0])
        flipped_txt = MathTex(str(new_val), font_size=24 * 0.7).move_to(original_pixel[1])
        flipped_pixel = VGroup(flipped_sq, flipped_txt)
        
        self.play(
            Indicate(original_pixel),
            Transform(original_pixel, flipped_pixel)
        )
        self.wait(1)

        # 6. Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)