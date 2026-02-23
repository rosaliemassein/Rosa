from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image Placeholder
        # Using GREY_D to avoid DARK_GRAY error
        image_rect = Rectangle(width=8, height=6, color=GREY_D, fill_opacity=0.5)
        label = Text("Trash Image", color=WHITE).scale(0.8)
        image = VGroup(image_rect, label)
        image.to_edge(UP, buff=0.5)

        # 2. Create 7x7 Grid
        grid_size = 5.0
        cell_size = grid_size / 7
        grid = VGroup(*[
            Square(side_length=cell_size, stroke_width=1, stroke_color=WHITE) 
            for _ in range(49)
        ]).arrange_in_grid(rows=7, cols=7, buff=0)
        grid.move_to(image.get_center())

        # 3. Highlight specific cell
        # Using Create instead of DrawBorderThenFill
        target_cell_index = 3 * 7 + 4
        target_cell = grid[target_cell_index]
        highlight_rect = target_cell.copy().set_fill(YELLOW, opacity=0.3).set_stroke(YELLOW, 3)

        # 4. Define Bounding Boxes
        # Ground truth: larger and dashed
        gt_box = Rectangle(
            width=cell_size * 2.2, 
            height=cell_size * 3.5, 
            color=GREEN, 
            stroke_width=3
        ).set_stroke(dash_length=0.1)
        gt_box.move_to(target_cell.get_center() + RIGHT * 0.2 + UP * 0.1)

        # Predicted box: offset from ground truth
        pred_box = Rectangle(
            width=cell_size * 1.5, 
            height=cell_size * 2.5, 
            color=BLUE, 
            stroke_width=3
        )
        pred_box.move_to(target_cell.get_center() - RIGHT * 0.3 - DOWN * 0.2)

        # 5. Coordinate Error Indicators
        dot_gt = Dot(gt_box.get_center(), radius=0.04, color=GREEN)
        dot_pred = Dot(pred_box.get_center(), radius=0.04, color=BLUE)
        
        # Horizontal error (x)
        x_line = Line(
            [dot_pred.get_x(), dot_pred.get_y(), 0],
            [dot_gt.get_x(), dot_pred.get_y(), 0],
            color=RED, stroke_width=2
        )
        # Vertical error (y)
        y_line = Line(
            [dot_gt.get_x(), dot_pred.get_y(), 0],
            [dot_gt.get_x(), dot_gt.get_y(), 0],
            color=ORANGE, stroke_width=2
        )

        # Width and Height indicators (using Line + add_tip for portability)
        w_indicator = Line(
            pred_box.get_left() + UP * 0.2, 
            pred_box.get_right() + UP * 0.2, 
            color=BLUE
        ).add_tip(tip_length=0.15).add_tip(tip_length=0.15, at_start=True)

        h_indicator = Line(
            pred_box.get_bottom() + RIGHT * 0.2, 
            pred_box.get_top() + RIGHT * 0.2, 
            color=BLUE
        ).add_tip(tip_length=0.15).add_tip(tip_length=0.15, at_start=True)

        # 6. Loss Formula
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)",
            r" + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)",
            font_size=24
        ).to_edge(DOWN, buff=0.5)

        # --- ANIMATION SEQUENCE ---

        self.play(FadeIn(image), Create(grid))
        self.wait(0.5)
        self.play(Create(highlight_rect))
        self.wait(0.5)

        # Show Boxes
        self.play(Create(gt_box), Create(dot_gt))
        self.play(Create(pred_box), Create(dot_pred))
        self.wait(0.5)

        # Show Coordinate Errors (x, y)
        self.play(Create(x_line), Create(y_line))
        self.play(Write(formula[0]))
        self.wait(1)

        # Show Dimension Errors (w, h)
        self.play(Create(w_indicator), Create(h_indicator))
        self.play(Write(formula[1]))
        self.wait(1)

        # Mock Training Animation
        self.play(
            pred_box.animate.move_to(gt_box.get_center()).set_width(gt_box.width).set_height(gt_box.height),
            dot_pred.animate.move_to(gt_box.get_center()),
            FadeOut(x_line), FadeOut(y_line),
            FadeOut(w_indicator), FadeOut(h_indicator),
            run_time=2
        )
        self.wait(2)