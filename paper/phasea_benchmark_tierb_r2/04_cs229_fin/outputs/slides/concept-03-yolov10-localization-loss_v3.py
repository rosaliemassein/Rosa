from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background image placeholder or actual image
        try:
            image = ImageMobject("img-11.jpeg").scale_to_fit_height(6)
            self.add(image)
        except:
            bg_rect = Rectangle(width=10, height=6, color=GRAY, fill_opacity=0.1)
            self.add(bg_rect)

        # 2. 7x7 Grid (Manually constructed as NumberPlane is disallowed)
        grid = VGroup()
        for i in range(8):
            # Vertical lines
            v_line = Line(start=[i-3.5, -3.5, 0], end=[i-3.5, 3.5, 0], stroke_width=1, stroke_opacity=0.4, color=WHITE)
            grid.add(v_line)
            # Horizontal lines
            h_line = Line(start=[-3.5, i-3.5, 0], end=[3.5, i-3.5, 0], stroke_width=1, stroke_opacity=0.4, color=WHITE)
            grid.add(h_line)
        self.play(Create(grid))

        # 3. Highlight specific cell (approximate center for a soda can)
        # Cell centered at (-1, 1)
        target_cell = Rectangle(width=1, height=1, color=YELLOW, stroke_width=5)
        target_cell.move_to([-1, 1, 0])
        self.play(Create(target_cell))

        # 4. Predicted Box (Green) and Ground Truth Box (Red)
        # We use standard Rectangle as DashedVMobject is disallowed
        gt_box = Rectangle(width=1.4, height=2.0, color=RED, stroke_width=4)
        gt_box.move_to([-1, 1, 0])
        gt_box.set_stroke(opacity=0.6)
        
        pred_box = Rectangle(width=1.9, height=2.6, color=GREEN, stroke_width=4)
        pred_box.move_to([-1.3, 1.3, 0])
        
        self.play(Create(gt_box), Create(pred_box))

        # 5. Delta arrows for center (x, y)
        p_center = pred_box.get_center()
        g_center = gt_box.get_center()
        
        # x-offset arrow
        arrow_x = Line(start=p_center, end=[g_center[0], p_center[1], 0], color=BLUE)
        arrow_x.add_tip(tip_length=0.15)
        # y-offset arrow
        arrow_y = Line(start=[g_center[0], p_center[1], 0], end=g_center, color=BLUE)
        arrow_y.add_tip(tip_length=0.15)
        
        # Dimension difference visualizer (w, h)
        w_diff_line = Line(
            start=pred_box.get_corner(DR) + 0.1 * DOWN,
            end=pred_box.get_corner(DR) + 0.1 * DOWN + (gt_box.get_width() - pred_box.get_width()) * RIGHT,
            color=ORANGE
        )
        w_diff_line.add_tip(tip_length=0.1)

        self.play(Create(arrow_x), Create(arrow_y))
        self.play(Create(w_diff_line))
        self.wait(0.5)

        # 6. LaTeX Loss Formula (Self-contained and robust)
        # Using the formula provided in the reference
        formula_str = r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right) + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)"
        loss_formula = MathTex(formula_str).scale(0.5).to_edge(UP, buff=0.3)
        
        # Manual background for the formula text
        formula_bg = Rectangle(
            width=loss_formula.get_width() + 0.4,
            height=loss_formula.get_height() + 0.4,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=0
        ).move_to(loss_formula)
        
        self.play(FadeIn(formula_bg), Write(loss_formula))
        self.wait(1)

        # 7. Mock Training Animation
        # Boxes align and formula highlights
        self.play(
            pred_box.animate.move_to(g_center).set_width(1.4).set_height(2.0),
            FadeOut(arrow_x),
            FadeOut(arrow_y),
            FadeOut(w_diff_line),
            loss_formula.animate.set_color(YELLOW),
            run_time=2.5
        )
        self.wait(2)