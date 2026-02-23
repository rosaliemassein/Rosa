from manim import *
import numpy as np

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image Placeholder
        # Use a simple rectangle if the image file is missing to ensure compilation
        try:
            image = ImageMobject("img-11.jpeg").scale_to_fit_width(7)
            self.add(image)
        except:
            image = Rectangle(width=7, height=5, fill_color="#333333", fill_opacity=0.5, stroke_width=0)
            self.add(image)

        # 2. Manual 7x7 Grid (Replacing NumberPlane)
        grid = VGroup()
        x_vals = np.linspace(-3.5, 3.5, 8)
        y_vals = np.linspace(-2.5, 2.5, 8)
        for x in x_vals:
            grid.add(Line([x, -2.5, 0], [x, 2.5, 0], stroke_width=1, stroke_opacity=0.4))
        for y in y_vals:
            grid.add(Line([-3.5, y, 0], [3.5, y, 0], stroke_width=1, stroke_opacity=0.4))
        self.play(Create(grid))

        # 3. Target Cell Highlight
        # Calculate center for a cell (e.g., column 2, row 3)
        cell_w = 1.0
        cell_h = 5.0 / 7.0
        cell_x = -3.5 + 2 * cell_w + cell_w / 2
        cell_y = -2.5 + 3 * cell_h + cell_h / 2
        target_cell = Rectangle(width=cell_w, height=cell_h, color=RED, stroke_width=4)
        target_cell.move_to([cell_x, cell_y, 0])
        self.play(Create(target_cell))

        # 4. Predicted Box and Ground Truth Box
        # Using a standard Rectangle for ground truth instead of DashedVMobject
        gt_box = Rectangle(width=2.2, height=1.3, color=GREEN, stroke_width=3).move_to([cell_x + 0.1, cell_y - 0.1, 0])
        pred_box = Rectangle(width=1.8, height=1.0, color=BLUE, stroke_width=3).move_to([cell_x - 0.2, cell_y + 0.2, 0])
        self.play(Create(gt_box), Create(pred_box))

        # 5. Arrows for coordinate errors
        arrow_x = Arrow(pred_box.get_center(), [gt_box.get_center()[0], pred_box.get_center()[1], 0], color=YELLOW, buff=0, stroke_width=2)
        arrow_y = Arrow([gt_box.get_center()[0], pred_box.get_center()[1], 0], gt_box.get_center(), color=YELLOW, buff=0, stroke_width=2)
        self.play(Create(arrow_x), Create(arrow_y))

        # 6. Loss Formula (Split for highlighting)
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}",
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)",
            r" + ",
            r"\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}",
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)"
        ).scale(0.6).to_edge(DOWN, buff=0.3)
        
        # Formula Background (Replacing BackgroundRectangle)
        formula_bg = Rectangle(
            width=formula.get_width() + 0.4, 
            height=formula.get_height() + 0.4, 
            fill_color=BLACK, 
            fill_opacity=0.85, 
            stroke_width=0
        ).move_to(formula)
        
        self.add(formula_bg)
        self.play(Write(formula))

        # 7. Mock Training Animation
        # Coordinate Alignment
        self.play(
            formula[1].animate.set_color(YELLOW),
            pred_box.animate.move_to(gt_box.get_center()),
            FadeOut(arrow_x), 
            FadeOut(arrow_y),
            run_time=2
        )
        self.wait(0.5)

        # Dimension Alignment
        self.play(
            formula[4].animate.set_color(BLUE),
            pred_box.animate.stretch_to_fit_width(2.2).stretch_to_fit_height(1.3),
            run_time=2
        )

        self.wait(2)