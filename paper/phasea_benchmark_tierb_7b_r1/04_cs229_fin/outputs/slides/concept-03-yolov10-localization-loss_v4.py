from manim import *

class YOLOv10LossFunction(Scene):
    def construct(self):
        # 1. Background Image
        # Using ImageMobject to display the trash items
        image = ImageMobject("img-11.jpeg")
        image.scale_to_fit_height(8)
        self.add(image)

        # 2. Manual 7x7 Grid (Replacing NumberPlane)
        grid = VGroup()
        cell_size = 0.8
        grid_width = cell_size * 7
        start_point = - (grid_width / 2)
        
        for i in range(8):
            # Vertical lines
            v_line = Line(
                start=[start_point + i * cell_size, grid_width / 2, 0],
                end=[start_point + i * cell_size, -grid_width / 2, 0],
                stroke_width=2, color=BLUE, stroke_opacity=0.6
            )
            # Horizontal lines
            h_line = Line(
                start=[-(grid_width / 2), start_point + i * cell_size, 0],
                end=[grid_width / 2, start_point + i * cell_size, 0],
                stroke_width=2, color=BLUE, stroke_opacity=0.6
            )
            grid.add(v_line, h_line)
        
        self.play(Create(grid))

        # 3. Highlight a specific cell (where a soda can center lies)
        # Choosing cell at index (4, 4) in the grid logic
        cell_center = [start_point + 4.5 * cell_size, start_point + 4.5 * cell_size, 0]
        highlight_cell = Rectangle(
            width=cell_size, height=cell_size, 
            color=YELLOW, fill_opacity=0.3, stroke_width=4
        ).move_to(cell_center)
        self.play(FadeIn(highlight_cell))

        # 4. Predicted and Ground Truth Boxes
        # Ground Truth (GT): Red
        gt_box = Rectangle(
            width=1.2, height=1.8, 
            color=RED, stroke_width=4
        ).move_to(cell_center + RIGHT * 0.1 + DOWN * 0.1)
        
        # Predicted: Green
        pred_box = Rectangle(
            width=2.0, height=1.0, 
            color=GREEN, stroke_width=4
        ).move_to(cell_center + LEFT * 0.4 + UP * 0.3)
        
        self.play(Create(gt_box), Create(pred_box))
        self.wait(0.5)

        # 5. Arrows for differences (x, y, w, h)
        # Arrows for position delta
        arrow_x = Arrow(
            start=pred_box.get_center(),
            end=[gt_box.get_center()[0], pred_box.get_center()[1], 0],
            color=WHITE, buff=0, tip_length=0.15
        )
        arrow_y = Arrow(
            start=[gt_box.get_center()[0], pred_box.get_center()[1], 0],
            end=gt_box.get_center(),
            color=WHITE, buff=0, tip_length=0.15
        )
        
        # Arrows for dimension delta
        arrow_w = Arrow(
            start=pred_box.get_right(),
            end=[gt_box.get_right()[0], pred_box.get_right()[1], 0],
            color=YELLOW, buff=0, tip_length=0.15
        )
        arrow_h = Arrow(
            start=pred_box.get_top(),
            end=[pred_box.get_top()[0], gt_box.get_top()[1], 0],
            color=YELLOW, buff=0, tip_length=0.15
        )

        self.play(Create(arrow_x), Create(arrow_y))
        self.wait(0.5)
        self.play(Create(arrow_w), Create(arrow_h))
        self.wait(1)
        self.play(FadeOut(arrow_x), FadeOut(arrow_y), FadeOut(arrow_w), FadeOut(arrow_h))

        # 6. Loss Formula
        # Using a background rect manually since BackgroundRectangle is restricted
        formula = MathTex(
            r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((x_{i}-\hat{x}_{i})^{2}+(y_{i}-\hat{y}_{i})^{2}\right)", 
            r" + ", 
            r"\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}", 
            r"\left((\sqrt{w_{i}}-\sqrt{\hat{w}_{i}})^{2}+(\sqrt{h_{i}}-\sqrt{\hat{h}_{i}})^{2}\right)",
            font_size=28
        ).to_edge(DOWN, buff=0.5)
        
        formula_bg = Rectangle(
            width=formula.width + 0.4, height=formula.height + 0.4,
            fill_color=BLACK, fill_opacity=0.85, stroke_width=0
        ).move_to(formula.get_center())
        
        self.play(FadeIn(formula_bg), Write(formula))
        self.wait(1)

        # 7. Mock Training Animation
        # Part 1: Position correction (Coordinate term)
        self.play(
            formula[1].animate.set_color(YELLOW),
            pred_box.animate.move_to(gt_box.get_center()),
            run_time=2
        )
        self.wait(0.5)

        # Part 2: Size correction (Dimensions term)
        self.play(
            formula[1].animate.set_color(WHITE),
            formula[4].animate.set_color(YELLOW),
            pred_box.animate.stretch_to_fit_width(gt_box.width).stretch_to_fit_height(gt_box.height),
            run_time=2
        )
        self.wait(0.5)
        
        self.play(formula[4].animate.set_color(WHITE))
        self.wait(2)

        # Final Cleanup
        self.play(FadeOut(VGroup(grid, highlight_cell, gt_box, pred_box, formula_bg, formula, image)))
        self.wait(1)