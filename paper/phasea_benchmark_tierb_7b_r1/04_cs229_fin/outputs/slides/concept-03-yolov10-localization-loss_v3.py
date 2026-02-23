from manim import *
import math

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # Load image
        image = ImageMobject("img-11.jpeg").scale(0.5)

        # Create 7x7 grid
        grid = VGroup(*[
            VGroup(*[Square(side_length=0.1, color=WHITE) for _ in range(7)])
            for _ in range(7)
        ]).arrange(DOWN, buff=0).arrange(RIGHT, buff=0)

        # Highlight specific cell
        target_cell = grid[2][3]
        target_cell.set_color(RED)

        # Draw predicted bounding box
        predicted_box = SurroundingRectangle(target_cell, color=BLUE, stroke_width=2)
        self.play(FadeIn(image), Create(grid))
        self.wait(1)
        self.play(Create(predicted_box))
        self.wait(1)

        # Draw ground truth bounding box
        gt_box = SurroundingRectangle(target_cell.shift(UP * 0.1 + LEFT * 0.1), color=GREEN, stroke_width=2)
        self.play(Create(gt_box))
        self.wait(1)

        # Arrows showing x and y differences
        x_arrow = Arrow(predicted_box.get_center(), gt_box.get_left(), color=RED)
        y_arrow = Arrow(predicted_box.get_top(), gt_box.get_bottom(), color=BLUE)

        self.play(Create(x_arrow), Create(y_arrow))
        self.wait(1)

        # Arrows showing w and h differences
        w_arrow = Arrow(predicted_box.get_width() * RIGHT, gt_box.get_width() * RIGHT, color=RED)
        h_arrow = Arrow(predicted_box.get_height() * UP, gt_box.get_height() * UP, color=BLUE)

        self.play(Create(w_arrow), Create(h_arrow))
        self.wait(1)

        # Final loss formula
        loss_formula = MathTex(r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right) + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)", color=BLACK)
        loss_formula.to_edge(DOWN, buff=1)

        self.play(Write(loss_formula))
        self.wait(2)