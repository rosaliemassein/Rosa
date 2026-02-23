from manim import *
import numpy as np

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image (with fallback)
        try:
            image = ImageMobject("img-11.jpeg")
            image.set_height(7)
            self.add(image)
        except:
            image = Rectangle(width=12, height=7, color=GRAY, fill_opacity=0.1)
            self.add(image)

        # 2. 7x7 Grid (Manually created to avoid NumberPlane constraints)
        grid = VGroup()
        ticks = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        for x in ticks:
            grid.add(Line([x, -3.5, 0], [x, 3.5, 0], stroke_width=1, color=WHITE, stroke_opacity=0.4))
        for y in ticks:
            grid.add(Line([-3.5, y, 0], [3.5, y, 0], stroke_width=1, color=WHITE, stroke_opacity=0.4))
        self.play(Create(grid))

        # 3. Highlight specific cell (where a soda can center might lie)
        # Choosing cell with center at (1, 0)
        target_cell_pos = [1, 0, 0]
        cell_highlight = Square(side_length=1, color=YELLOW, stroke_width=4).move_to(target_cell_pos)
        self.play(Create(cell_highlight))

        # 4. Ground Truth and Predicted Boxes
        # Ground Truth: Red dashed box
        gt_box = Rectangle(width=1.8, height=1.4, color=RED).move_to([1.0, 0.0, 0])
        gt_box.set_stroke(dash_pattern=[0.1, 0.1])
        
        # Predicted Box: Blue box
        pred_box = Rectangle(width=2.4, height=1.9, color=BLUE).move_to([1.3, 0.4, 0])
        pred_box.set_fill(BLUE, opacity=0.3)
        self.play(Create(gt_box), Create(pred_box))

        # 5. Coordinate and Dimension difference arrows
        # (x, y) distance arrows
        x_arr = Arrow([1.0, 0.0, 0], [1.3, 0.0, 0], buff=0, color=GREEN, stroke_width=3)
        y_arr = Arrow([1.3, 0.0, 0], [1.3, 0.4, 0], buff=0, color=GREEN, stroke_width=3)
        
        # (w, h) difference arrows (showing the gap between edges)
        # Width diff: from Pred right edge to GT right edge
        w_arr = Arrow([1.3 + 1.2, 0.4, 0], [1.0 + 0.9, 0.4, 0], buff=0, color=YELLOW, stroke_width=3)
        # Height diff: from Pred top edge to GT top edge
        h_arr = Arrow([1.3, 0.4 + 0.95, 0], [1.3, 0.0 + 0.7, 0], buff=0, color=YELLOW, stroke_width=3)
        
        self.play(Create(x_arr), Create(y_arr))
        self.play(Create(w_arr), Create(h_arr))

        # 6. Loss Formula
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)", 
            r" + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)"
        ).scale(0.6).to_edge(UP, buff=0.2)
        formula.set_background_stroke(color=BLACK, width=4)
        self.play(Write(formula))

        # 7. Mock Training Animation
        # Highlight coordinate terms as center aligns
        coord_rect = SurroundingRectangle(formula[1], color=GREEN)
        size_rect = SurroundingRectangle(formula[3], color=YELLOW)
        
        self.play(Create(coord_rect))
        self.play(
            pred_box.animate.move_to(gt_box.get_center()),
            FadeOut(x_arr), FadeOut(y_arr),
            run_time=2
        )
        
        # Highlight dimension terms as size aligns
        self.play(ReplacementTransform(coord_rect, size_rect))
        self.play(
            pred_box.animate.set_width(1.8).set_height(1.4),
            FadeOut(w_arr), FadeOut(h_arr),
            run_time=2
        )
        self.play(FadeOut(size_rect))

        self.wait(2)