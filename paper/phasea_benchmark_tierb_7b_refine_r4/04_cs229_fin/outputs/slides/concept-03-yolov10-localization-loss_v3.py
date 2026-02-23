from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image
        # Using a try-except block to handle potential file issues in restricted environments
        try:
            trash_image = ImageMobject("img-11.jpeg")
        except:
            trash_image = Rectangle(width=8, height=6, fill_opacity=0.1, color=GRAY)
        
        trash_image.scale(0.7).to_edge(UP, buff=0.5)
        self.play(FadeIn(trash_image))

        # 2. 7x7 Grid (Manually constructed to avoid NumberPlane restrictions)
        grid_size = 4.0
        rows, cols = 7, 7
        step = grid_size / rows
        grid = VGroup()
        # Center the grid on the trash image
        grid_center = trash_image.get_center()
        start_pt = grid_center + LEFT * (grid_size / 2) + DOWN * (grid_size / 2)
        
        for i in range(rows + 1):
            grid.add(Line(start_pt + UP * i * step, start_pt + UP * i * step + RIGHT * grid_size))
            grid.add(Line(start_pt + RIGHT * i * step, start_pt + RIGHT * i * step + UP * grid_size))
        
        grid.set_stroke(BLUE, width=1, opacity=0.5)
        self.play(Create(grid))

        # 3. Highlight a specific cell (where a center might lie)
        # Choosing an arbitrary cell (row 4, col 3)
        cell_center = start_pt + RIGHT * (3.5 * step) + UP * (4.5 * step)
        cell_highlight = Rectangle(
            width=step, height=step, 
            color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.2
        ).move_to(cell_center)
        
        self.play(Create(cell_highlight))

        # 4. Bounding Boxes
        # Ground Truth (Red)
        gt_box = Rectangle(width=1.4, height=2.2, color=RED, stroke_width=3).move_to(cell_center + RIGHT*0.2 + UP*0.1)
        # Prediction (Green)
        pred_box = Rectangle(width=1.1, height=1.9, color=GREEN, stroke_width=3).move_to(cell_center + LEFT*0.1 + DOWN*0.2)
        
        self.play(Create(gt_box), Create(pred_box))

        # 5. Arrows for distance (x,y) and dimension (w,h) differences
        arrow_xy = Arrow(pred_box.get_center(), gt_box.get_center(), buff=0, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        arrow_wh = Arrow(pred_box.get_corner(UR), gt_box.get_corner(UR), buff=0, color=ORANGE, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        
        self.play(Create(arrow_xy), Create(arrow_wh))

        # 6. Formula Presentation
        # Splitting formula to highlight terms easily
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", # 0: pre
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)", # 1: xy term
            r" + ", # 2: plus
            r"\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", # 3: pre2
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)" # 4: wh term
        ).scale(0.55).to_edge(DOWN, buff=0.4)
        
        # Add background for contrast
        formula_bg = SurroundingRectangle(formula, color=BLACK, fill_color=BLACK, fill_opacity=0.7, buff=0.1)
        self.add(formula_bg)
        self.play(Write(formula))

        # 7. Mock Training Animation
        # Highlight XY loss
        self.play(Indicate(formula[1], color=BLUE), arrow_xy.animate.set_color(BLUE))
        self.play(
            pred_box.animate.move_to(gt_box.get_center()),
            FadeOut(arrow_xy),
            run_time=1.5
        )
        
        # Highlight WH loss
        self.play(Indicate(formula[4], color=ORANGE), arrow_wh.animate.set_color(ORANGE))
        self.play(
            pred_box.animate.stretch_to_fit_width(gt_box.width).stretch_to_fit_height(gt_box.height),
            FadeOut(arrow_wh),
            run_time=1.5
        )

        # Completion
        self.play(pred_box.animate.set_color(YELLOW))
        self.wait(2)