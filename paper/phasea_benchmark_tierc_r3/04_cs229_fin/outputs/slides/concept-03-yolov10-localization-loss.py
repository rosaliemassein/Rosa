from manim import *

class YOLOv10LocalizationLoss(Scene):
    def construct(self):
        image_ref = "img-11.jpeg"
        self.image = ImageMobject(image_ref)
        self.grid = NumberPlane()
        self.box = SurroundingRectangle(color=RED, stroke_width=2)
        self.truth_box = SurroundingRectangle(color=YELLOW, stroke_width=1.5)

        self.texts = [
            Text(self.goal),
            Text(self.remarks),
            MathTex(r"\lambda_{coord}\sum_{i=0}^{S^{2}}\sum_{j=0}^{B}1_{ij}^{obj}\\left((x_{i}-\\hat{x}_{i})^{2}+(y_{i}-\\hat{y}_{i})^{2}\\right) + \\sum_{i=0}^{S^{2}}\\sum_{j=0}^{B}1_{ij}^{obj}\\left((\sqrt{w_{i}}-\\sqrt{\\hat{w}_{i}})^{2}+(\\sqrt{h_{i}}-\\sqrt{\\hat{h}_{i}})^{2}\\right)"),
        ]
        self.texts[0].next_to(self.image, DOWN)
        self.texts[1].next_to(self.texts[0], DOWN)
        self.texts[2].next_to(self.image, DOWN)

        self.add(self.image, self.grid)
        
        # Place a cell that doesn't contain any trash
        i = 3
        j = 2
        cell = self.grid.get_cell(i, j)
        cell.fill(BLACK)

        # Draw a box centered in this cell
        self.box.move_to(cell.get_center())
        self.add(self.box)
        
        # Draw a truth box slightly offset
        truth_box_center = cell.get_center() + RIGHT*0.2+UP*0.1
        self.truth_box.move_to(truth_box_center)
        self.add(self.truth_box)
        
        # Draw arrows between centers and dimensions
        x_arrow = Arrow(cell.get_center(), truth_box_center, buff=0.1)
        y_arrow = Arrow(cell.get_center(), truth_box_center, buff=0.1, angle=PI/2)
        w_arrow = Arrow(cell.get_center(), truth_box_center, buff=0.1, angle=-PI/2)
        h_arrow = Arrow(cell.get_center(), truth_box_center, buff=0.1, angle=PI)
        self.add(x_arrow, y_arrow, w_arrow, h_arrow)
        
        # Show the formula
        self.texts[2].next_to(self.box, RIGHT)
        
        

        # Mock training animation
        self.play(FadeIn(x_arrow), FadeIn(y_arrow), FadeIn(w_arrow), FadeIn(h_arrow))
        self.wait()