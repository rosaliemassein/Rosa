from manim import *

class ConceptAnimationYolo(Scene):
    def construct(self):
        # 1. Background Image or Placeholder
        try:
            image = ImageMobject("img-11.jpeg").scale_to_fit_height(6)
        except:
            image = Rectangle(width=8, height=6, color=GRAY, fill_opacity=0.5)
            image.add(Text("img-11.jpeg").scale(0.5))
        self.add(image)

        # 2. Grid Setup (7x7 representing the YOLO grid)
        grid = NumberPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )
        grid.scale_to_fit_height(6)
        self.play(Create(grid))

        # 3. Highlight specific cell
        # Using cell (1, 1) in coordinate space
        target_cell_center = grid.c2p(1, 1)
        cell_highlight = Square(side_length=grid.get_x_unit_size(), color=YELLOW, fill_opacity=0.3)
        cell_highlight.move_to(target_cell_center)
        self.play(Create(cell_highlight))

        # 4. Ground Truth and Predicted Boxes
        # Ground Truth: dashed green
        gt_center = grid.c2p(1.2, 0.8)
        gt_box = Rectangle(width=1.8, height=2.2, color=GREEN).move_to(gt_center)
        gt_box.set_stroke(dash_pattern=[5, 5])
        
        # Prediction: solid red
        pred_center = grid.c2p(0.7, 1.3)
        pred_box = Rectangle(width=2.5, height=1.5, color=RED).move_to(pred_center)

        self.play(Create(gt_box), Create(pred_box))
        self.wait(0.5)

        # 5. Animate coordinate differences (x, y)
        dot_gt = Dot(gt_center, color=GREEN, radius=0.05)
        dot_pred = Dot(pred_center, color=RED, radius=0.05)
        
        # Difference indicators
        arrow_x = Arrow(
            start=[pred_center[0], pred_center[1], 0], 
            end=[gt_center[0], pred_center[1], 0], 
            color=BLUE, buff=0, stroke_width=3
        )
        arrow_y = Arrow(
            start=[gt_center[0], pred_center[1], 0], 
            end=[gt_center[0], gt_center[1], 0], 
            color=PURPLE, buff=0, stroke_width=3
        )
        
        lbl_x = MathTex(r"\Delta x", color=BLUE).scale(0.5).next_to(arrow_x, DOWN, buff=0.1)
        lbl_y = MathTex(r"\Delta y", color=PURPLE).scale(0.5).next_to(arrow_y, RIGHT, buff=0.1)

        self.play(FadeIn(dot_gt), FadeIn(dot_pred))
        self.play(GrowArrow(arrow_x), Write(lbl_x))
        self.play(GrowArrow(arrow_y), Write(lbl_y))

        # 6. Loss Formula
        # Splitting the formula for highlighting
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}",
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)",
            r" + ",
            r"\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}",
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)"
        ).scale(0.6).to_edge(DOWN, buff=0.2)
        formula.set_background_stroke(color=BLACK, width=4)
        
        self.play(Write(formula))
        self.wait(1)

        # 7. Mock "Training" Animation
        # Highlight x,y coordinates term
        h_rect_xy = SurroundingRectangle(formula[1], color=YELLOW)
        self.play(Create(h_rect_xy))
        
        # Align centers
        self.play(
            pred_box.animate.move_to(gt_center),
            dot_pred.animate.move_to(gt_center),
            FadeOut(arrow_x), FadeOut(arrow_y), FadeOut(lbl_x), FadeOut(lbl_y),
            run_time=1.2
        )
        self.play(FadeOut(h_rect_xy))

        # Highlight width/height square root term
        h_rect_wh = SurroundingRectangle(formula[4], color=YELLOW)
        self.play(Create(h_rect_wh))
        
        # Align dimensions
        self.play(
            pred_box.animate.stretch_to_fit_width(gt_box.width).stretch_to_fit_height(gt_box.height),
            run_time=1.2
        )
        self.play(FadeOut(h_rect_wh))
        
        self.wait(3)