from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background / Image Representation
        # Defining basic colors to avoid undefined identifier issues
        MY_BLUE = BLUE
        MY_YELLOW = YELLOW
        MY_RED = RED
        MY_GREEN = GREEN
        
        image_w, image_h = 6, 6
        image_bg = Rectangle(width=image_w, height=image_h, color=MY_BLUE, fill_opacity=0.1)
        image_label = Text("Input Image", font_size=24, color=GRAY).to_edge(UP, buff=0.2)
        
        # 2. 7x7 Grid (NumberPlane)
        grid = NumberPlane(
            x_range=[0, 7, 1],
            y_range=[0, 7, 1],
            x_length=image_w,
            y_length=image_h,
            background_line_style={"stroke_color": WHITE, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"include_numbers": False}
        ).move_to(ORIGIN)
        
        self.add(image_bg, image_label, grid)
        
        # 3. Highlight specific cell (where object center lies)
        # Using cell (4, 3) in grid coordinates
        cell_size = image_w / 7
        cell_center = grid.c2p(4.5, 3.5)
        highlight_cell = Rectangle(
            width=cell_size, height=cell_size,
            stroke_color=MY_YELLOW, stroke_width=4, fill_color=MY_YELLOW, fill_opacity=0.2
        ).move_to(cell_center)
        
        # 4. Bounding Boxes
        # Ground Truth: Dashed Yellow
        truth_box = Rectangle(width=1.2, height=1.8, color=MY_YELLOW)
        truth_box.set_stroke(width=4).set_stroke(dash_pattern=[0.1, 0.1])
        truth_box.move_to(cell_center)
        
        # Prediction: Solid Red, slightly offset
        pred_box = Rectangle(width=1.6, height=2.2, color=MY_RED, stroke_width=4)
        pred_box.move_to(cell_center + RIGHT * 0.4 + UP * 0.3)
        
        self.play(FadeIn(highlight_cell))
        self.play(Create(truth_box), Create(pred_box))
        
        # 5. Arrows for Delta X, Delta Y
        gt_center = truth_box.get_center()
        pred_center = pred_box.get_center()
        
        # We'll use simple Arrow objects as they are highly compatible
        arrow_x = Arrow(
            start=[gt_center[0], pred_center[1], 0],
            end=pred_center,
            color=MY_BLUE, buff=0, tip_length=0.15
        )
        arrow_y = Arrow(
            start=[gt_center[0], pred_center[1], 0],
            end=gt_center,
            color=MY_GREEN, buff=0, tip_length=0.15
        )
        
        label_x = MathTex(r"x - \hat{x}", font_size=20, color=MY_BLUE).next_to(arrow_x, UP, buff=0.05)
        label_y = MathTex(r"y - \hat{y}", font_size=20, color=MY_GREEN).next_to(arrow_y, LEFT, buff=0.05)

        # 6. Localization Loss Formula
        # Splitting into two parts for highlighting logic
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)",
            r" + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)",
            font_size=24
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(formula))
        self.play(Create(arrow_x), Write(label_x), Create(arrow_y), Write(label_y))
        self.wait(1)

        # 7. Mock Training Animation
        # Align boxes and highlight formula terms
        self.play(
            pred_box.animate.move_to(gt_center).set_width(truth_box.width).set_height(truth_box.height),
            FadeOut(arrow_x), FadeOut(label_x),
            FadeOut(arrow_y), FadeOut(label_y),
            formula[0].animate.set_color(MY_YELLOW),
            run_time=2
        )
        
        self.play(
            formula[0].animate.set_color(WHITE),
            formula[1].animate.set_color(MY_YELLOW),
            run_time=1
        )
        
        self.wait(2)