from manim import *
import numpy as np

class Concept03YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image (Fallback to a shaded rectangle if file is missing)
        try:
            background_img = ImageMobject("img-11.jpeg").scale_to_fit_height(6)
            self.add(background_img)
        except:
            bg_rect = Rectangle(width=8, height=6, fill_opacity=0.1, color=WHITE)
            self.add(bg_rect)

        # 2. 7x7 Grid (Manually created as NumberPlane is disallowed)
        grid_lines = VGroup()
        # Create 8 lines to form 7 intervals
        for i in range(8):
            coord = -3.5 + i
            # Vertical lines
            grid_lines.add(Line(start=[coord, -3.5, 0], end=[coord, 3.5, 0], stroke_width=1, stroke_opacity=0.4))
            # Horizontal lines
            grid_lines.add(Line(start=[-3.5, coord, 0], end=[3.5, coord, 0], stroke_width=1, stroke_opacity=0.4))
        
        self.play(Create(grid_lines))

        # 3. Highlight a specific cell (where a soda can's center might lie)
        # Center of cell (1, 1) in our coordinate system
        cell_highlight = Rectangle(width=1, height=1, color=YELLOW, stroke_width=4)
        cell_highlight.move_to([1, 1, 0])
        self.play(Create(cell_highlight))

        # 4. Predicted Bounding Box (Blue)
        pred_box = Rectangle(width=2.2, height=2.8, color=BLUE, stroke_width=4)
        pred_box.move_to([0.7, 1.3, 0])

        # 5. Ground Truth Bounding Box (Red)
        # Using a regular Rectangle as DashedVMobject is undefined
        true_box = Rectangle(width=1.8, height=2.4, color=RED, stroke_width=3)
        true_box.move_to([1.2, 0.8, 0])
        # Add some visual distinction to the "ground truth"
        true_box.set_stroke(opacity=0.7)

        self.play(Create(true_box), Create(pred_box))
        self.wait(0.5)

        # 6. Arrows showing differences (x, y, w, h)
        # Center distance (x, y)
        center_arrow = Arrow(start=pred_box.get_center(), end=true_box.get_center(), color=YELLOW, buff=0, tip_length=0.15)
        
        # Width difference arrow (Horizontal double arrow)
        # Using Line with add_tip at both ends as DoubleArrow is undefined
        w_diff_line = Line(
            start=[pred_box.get_left()[0], pred_box.get_top()[1] + 0.3, 0],
            end=[true_box.get_left()[0], pred_box.get_top()[1] + 0.3, 0],
            color=GREEN
        )
        w_diff_line.add_tip(tip_length=0.1)
        w_diff_line.add_tip(tip_length=0.1, at_start=True)

        # Height difference arrow (Vertical double arrow)
        h_diff_line = Line(
            start=[pred_box.get_right()[0] + 0.3, pred_box.get_top()[1], 0],
            end=[pred_box.get_right()[0] + 0.3, true_box.get_top()[1], 0],
            color=ORANGE
        )
        h_diff_line.add_tip(tip_length=0.1)
        h_diff_line.add_tip(tip_length=0.1, at_start=True)

        # 7. Loss Formula
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)",
            r" + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)",
            font_size=22
        ).to_edge(DOWN, buff=0.3)

        # Animation sequence for arrows and math
        self.play(GrowArrow(center_arrow), Write(formula[0]))
        self.wait(0.5)
        self.play(Create(w_diff_line), Create(h_diff_line), Write(formula[1]))
        self.wait(1)

        # 8. Mock Training: Predicted box converges to Ground Truth
        self.play(
            pred_box.animate.move_to(true_box.get_center()).set_width(1.8).set_height(2.4),
            FadeOut(center_arrow),
            FadeOut(w_diff_line),
            FadeOut(h_diff_line),
            formula[0].animate.set_color(YELLOW),
            formula[1].animate.set_color(GREEN),
            run_time=2
        )

        self.wait(2)