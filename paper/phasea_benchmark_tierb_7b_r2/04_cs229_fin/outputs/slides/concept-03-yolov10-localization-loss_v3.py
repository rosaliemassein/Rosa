from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        # 1. Background Image
        # Using a fallback rectangle if the image file is missing
        try:
            image = ImageMobject("img-11.jpeg")
            image.height = 7
        except:
            image = Rectangle(width=10, height=7, fill_color="#333333", fill_opacity=1)
        self.add(image)

        # 2. 7x7 Grid (Manual construction to avoid NumberPlane and DashedLine)
        grid = VGroup()
        grid_size = 6.0
        step = grid_size / 7.0
        for i in range(8):
            # Horizontal lines
            h_line = Line(
                start=[-grid_size/2, -grid_size/2 + i*step, 0],
                end=[grid_size/2, -grid_size/2 + i*step, 0],
                stroke_width=1, color=WHITE, stroke_opacity=0.4
            )
            # Vertical lines
            v_line = Line(
                start=[-grid_size/2 + i*step, -grid_size/2, 0],
                end=[-grid_size/2 + i*step, grid_size/2, 0],
                stroke_width=1, color=WHITE, stroke_opacity=0.4
            )
            grid.add(h_line, v_line)
        self.play(Create(grid))

        # 3. Highlight specific cell
        # Picking cell at grid index (4, 3) from bottom-left
        cell_x = -grid_size/2 + (4 + 0.5) * step
        cell_y = -grid_size/2 + (3 + 0.5) * step
        highlight = Square(side_length=step).move_to([cell_x, cell_y, 0])
        highlight.set_fill(YELLOW, opacity=0.3).set_stroke(YELLOW, 3)
        self.play(FadeIn(highlight))

        # 4. Bounding Boxes
        # Ground Truth (Using standard Rectangle since DashedVMobject is problematic)
        gt_color = BLUE
        gt_rect = Rectangle(width=1.4, height=1.0, color=gt_color, stroke_width=2)
        gt_rect.move_to([cell_x + 0.1, cell_y - 0.2, 0])
        
        # Predicted Box
        pred_color = RED
        pred_rect = Rectangle(width=2.2, height=1.6, color=pred_color, stroke_width=4)
        pred_rect.move_to([cell_x + 0.5, cell_y + 0.3, 0])
        
        self.play(Create(gt_rect), Create(pred_rect))

        # 5. Arrows for differences
        # Coordinate diffs (center x, y)
        arr_x = Arrow(
            start=pred_rect.get_center(), 
            end=[gt_rect.get_center()[0], pred_rect.get_center()[1], 0], 
            buff=0, color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.15
        )
        arr_y = Arrow(
            start=[gt_rect.get_center()[0], pred_rect.get_center()[1], 0], 
            end=gt_rect.get_center(), 
            buff=0, color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.15
        )
        
        # Dimension diffs (width, height)
        arr_w = Arrow(
            start=pred_rect.get_right(), 
            end=[gt_rect.get_right()[0], pred_rect.get_right()[1], 0], 
            buff=0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.15
        )
        arr_h = Arrow(
            start=pred_rect.get_top(), 
            end=[pred_rect.get_top()[0], gt_rect.get_top()[1], 0], 
            buff=0, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.15
        )

        self.play(Create(arr_x), Create(arr_y))
        self.play(Create(arr_w), Create(arr_h))

        # 6. LaTeX Loss Formula
        formula_str = r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right) + \sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)"
        formula = MathTex(formula_str, font_size=20)
        # Position at the bottom
        formula.move_to([0, -3.3, 0])
        
        # Add a dark background for the formula
        label_bg = Rectangle(width=13, height=0.8, fill_color=BLACK, fill_opacity=0.8, stroke_width=0).move_to(formula)
        self.add(label_bg)
        self.play(Write(formula))

        # 7. Mock Training Animation
        # Highlight coordinate terms
        highlight_rect = SurroundingRectangle(formula, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect))

        self.play(
            pred_rect.animate.move_to(gt_rect.get_center()).set_width(1.4).set_height(1.0),
            FadeOut(arr_x), FadeOut(arr_y), FadeOut(arr_w), FadeOut(arr_h),
            run_time=2
        )
        
        self.wait(2)