import numpy as np
from manim import *

class YOLOV10LocalizationLoss(Scene):
    def construct(self):
        # 1. Formula Setup
        # Splitting formula to highlight terms individually
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)", 
            r"+", 
            r"\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)",
            font_size=24
        ).to_edge(UP, buff=0.5)

        # 2. Manual Grid Creation (Avoiding NumberPlane as it was disallowed)
        grid_side = 7
        cell_size = 0.5
        grid = VGroup()
        for i in range(grid_side + 1):
            # Vertical lines
            grid.add(Line([i * cell_size, 0, 0], [i * cell_size, grid_side * cell_size, 0]))
            # Horizontal lines
            grid.add(Line([0, i * cell_size, 0], [grid_side * cell_size, i * cell_size, 0]))
        grid.set_color(BLUE).center().shift(LEFT * 3)
        
        # Helper to get grid cell center
        grid_origin = grid.get_corner(DL)
        def get_cell_center(r, c):
            return grid_origin + np.array([(c + 0.5) * cell_size, (r + 0.5) * cell_size, 0])

        target_cell_center = get_cell_center(3, 3)

        # 3. Highlight Cell
        cell_highlight = Square(side_length=cell_size, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        cell_highlight.move_to(target_cell_center)

        # 4. Image Placeholder
        image_placeholder = Rectangle(width=4, height=3, color=GRAY_B, fill_opacity=0.1)
        image_placeholder.to_edge(RIGHT, buff=0.5)
        image_text = Text("img-11.jpeg", font_size=16).move_to(image_placeholder)
        image_group = VGroup(image_placeholder, image_text)

        # 5. Bounding Boxes
        # Ground Truth (Using thin lines to represent dashed look if DashedVMobject is unavailable)
        truth_w, truth_h = 1.2, 0.8
        truth_center = target_cell_center + np.array([0.15, 0.1, 0])
        
        truth_box = Rectangle(width=truth_w, height=truth_h, color=RED, stroke_width=2)
        truth_box.move_to(truth_center)
        # Using a low opacity to differentiate from predicted
        truth_box.set_stroke(opacity=0.6)

        # Predicted Box
        pred_w, pred_h = 1.6, 1.2
        pred_center = target_cell_center + np.array([-0.1, -0.15, 0])
        pred_box = Rectangle(width=pred_w, height=pred_h, color=GREEN)
        pred_box.move_to(pred_center)

        # 6. Arrows for Coordinate differences
        arrow_x = Arrow(
            start=[pred_center[0], pred_center[1], 0],
            end=[truth_center[0], pred_center[1], 0],
            buff=0, color=WHITE, stroke_width=2, tip_length=0.1
        )
        arrow_y = Arrow(
            start=[truth_center[0], pred_center[1], 0],
            end=[truth_center[0], truth_center[1], 0],
            buff=0, color=WHITE, stroke_width=2, tip_length=0.1
        )
        
        label_x = MathTex(r"x - \hat{x}", font_size=16).next_to(arrow_x, DOWN, buff=0.05)
        label_y = MathTex(r"y - \hat{y}", font_size=16).next_to(arrow_y, RIGHT, buff=0.05)

        # --- Animation Sequence ---
        self.add(image_group)
        self.play(Create(grid))
        self.play(FadeIn(cell_highlight))
        self.wait(0.5)
        
        self.play(Create(truth_box))
        self.play(Create(pred_box))
        self.play(Create(arrow_x), Create(label_x), Create(arrow_y), Create(label_y))
        self.wait(1)

        self.play(Write(formula))
        self.wait(1)

        # Mock training: Coordinates alignment
        self.play(
            Indicate(formula[1], color=YELLOW),
            pred_box.animate.move_to(truth_center),
            FadeOut(arrow_x), FadeOut(arrow_y),
            FadeOut(label_x), FadeOut(label_y),
            run_time=2
        )
        
        # Mock training: Width/Height alignment
        self.play(
            Indicate(formula[4], color=YELLOW),
            pred_box.animate.stretch_to_fit_width(truth_w).stretch_to_fit_height(truth_h),
            run_time=2
        )
        
        self.wait(2)
        
        # Final cleanup
        self.play(
            FadeOut(image_group),
            FadeOut(grid),
            FadeOut(cell_highlight),
            FadeOut(pred_box),
            FadeOut(truth_box),
            formula.animate.move_to(ORIGIN).scale(1.2)
        )
        self.wait(1)