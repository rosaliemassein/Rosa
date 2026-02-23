from manim import *

class YOLOCoordinateLoss(Scene):
    def construct(self):
        # 1. Background Image/Placeholder
        try:
            image = ImageMobject("img-11.jpeg").scale(1.5)
        except:
            image = Rectangle(width=10, height=6, fill_opacity=0.1, color=GRAY)
        self.add(image)

        # 2. 7x7 Grid (Manually constructed as NumberPlane is disallowed)
        grid = VGroup()
        for i in range(8):
            # Horizontal lines from x=-3.5 to 3.5
            grid.add(Line(start=[-3.5, -3.5 + i, 0], end=[3.5, -3.5 + i, 0], stroke_width=1, stroke_opacity=0.5))
            # Vertical lines from y=-3.5 to 3.5
            grid.add(Line(start=[-3.5 + i, -3.5, 0], end=[-3.5 + i, 3.5, 0], stroke_width=1, stroke_opacity=0.5))
        self.play(Create(grid))

        # 3. Highlight specific cell
        cell_pos = [0.5, 0.5, 0] 
        highlight = Square(side_length=1).move_to(cell_pos).set_fill(YELLOW, opacity=0.3)
        self.play(FadeIn(highlight))

        # 4. Ground Truth and Predicted Boxes
        # Using simple Rectangle because DashedVMobject is disallowed in this environment
        gt_box = Rectangle(width=2.5, height=3.5, color=RED).move_to([0.7, 0.6, 0])
        pred_box = Rectangle(width=3.2, height=2.4, color=BLUE).move_to([0.0, 0.1, 0])
        
        self.play(Create(gt_box), Create(pred_box))

        # 5. Distance between centers (x, y intuition)
        arrow = Arrow(start=pred_box.get_center(), end=gt_box.get_center(), buff=0, color=WHITE)
        self.play(Create(arrow))

        # 6. LaTeX Formula for Loss
        # Reference: \lambda_{coord}\sum_{i=0}^{S^2}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_i-\hat{x}_i)^2+(y_i-\hat{y}_i)^2\right) + \sum_{i=0}^{S^2}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_i}-\sqrt{\hat{w}_i})^2+(\sqrt{h_i}-\sqrt{\hat{h}_i})^2\right)
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^2}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_i-\hat{x}_i)^2+(y_i-\hat{y}_i)^2\right)",
            r" + \sum_{i=0}^{S^2}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_i}-\sqrt{\hat{w}_i})^2+(\sqrt{h_i}-\sqrt{\hat{h}_i})^2\right)",
            font_size=32
        ).to_edge(DOWN).set_background_stroke(color=BLACK, width=4)

        self.play(Write(formula))
        self.wait(1)

        # 7. Mock Training Animation
        # We morph the predicted box into the ground truth's shape and position
        # while highlighting the respective parts of the formula.
        self.play(
            pred_box.animate.become(gt_box.copy().set_color(BLUE)),
            arrow.animate.scale(0.01),
            formula[0].animate.set_color(YELLOW),
            run_time=2
        )
        self.play(formula[1].animate.set_color(GREEN))
        
        self.wait(2)