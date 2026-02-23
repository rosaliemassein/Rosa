from manim import *

class YOLOLocalizationLoss(Scene):
    def construct(self):
        # Load and display the image
        trash_image = ImageMobject("img-11.jpeg")
        self.add(trash_image)

        # Create a 7x7 grid (NumberPlane)
        grid = NumberPlane(x_range=(-2, 2), y_range=(-2, 2), step=0.5)
        grid = grid.scale(1.5).move_to(trash_image.get_center()).rotate(-PI/6)

        self.add(grid)

        # Highlight specific cell
        center_cell = Circle(radius=0.2, color=YELLOW)
        center_cell.move_to(grid.corners[1])
        self.add(center_cell)

        # Draw surrounding rectangle (predicted box) and offset dashed rectangle (ground truth)
        predicted_box = SurroundingRectangle(grid.corners[1], buff=0.2, color=BLUE)
        ground_truth_box = SurroundingRectangle(grid.corners[1], buff=0.2, color=RED, stroke_dasharray=(2, 4))
        ground_truth_box.move_to(grid.corners[1] + RIGHT * 0.5 + DOWN * 0.3)
        self.play(Create(predicted_box), Create(ground_truth_box))

        # Draw arrows showing the distance between centers and dimensions
        x_arrow = Arrow(grid.corners[1], grid.corners[1] + RIGHT * 0.5, buff=0.1)
        y_arrow = Arrow(grid.corners[1], grid.corners[1] + DOWN * 0.3, buff=0.1)
        w_arrow = Arrow(grid.corners[1], grid.corners[1] + RIGHT * 0.5, buff=0.1).rotate(-PI/4)
        h_arrow = Arrow(grid.corners[1], grid.corners[1] + DOWN * 0.3, buff=0.1).rotate(-PI/4)
        self.play(Create(x_arrow), Create(y_arrow), Create(w_arrow), Create(h_arrow))

        # Show the LaTeX formula
        loss_formula = MathTex(self.formula).scale(0.75)
        loss_formula.move_to(grid.get_center() + UP * 1.5)
        self.play(Create(loss_formula))

        # Animate aligning boxes during mock training
        for i in range(5):
            self.play(FadeOut(x_arrow), FadeOut(y_arrow), FadeOut(w_arrow), FadeOut(h_arrow))
            new_x = RIGHT * 0.2
            new_y = DOWN * 0.1
            new_w_h = RIGHT * 0.3 + DOWN * 0.2
            x_arrow = Arrow(grid.corners[1], grid.corners[1] + new_x, buff=0.1)
            y_arrow = Arrow(grid.corners[1], grid.corners[1] + new_y, buff=0.1)
            w_arrow = Arrow(grid.corners[1], grid.corners[1] + new_w_h, buff=0.1).rotate(-PI/4)
            h_arrow = Arrow(grid.corners[1], grid.corners[1] + new_w_h, buff=0.1).rotate(-PI/4)
            self.play(Create(x_arrow), Create(y_arrow), Create(w_arrow), Create(h_arrow))
            self.wait(0.25)

        # Highlight coordinate terms in the loss formula
        coord_terms = Text("coordinate terms", color=YELLOW).scale(0.75)
        coord_terms.move_to(grid.get_center() + UP * 0.1)
        self.play(Create(coord_terms))

        # Show the explanation
        narration = Text("To find these objects in a pile, YOLOv10 divides the image into a grid. If the center of a piece of trash falls into a cell, that cell is responsible for predicting a bounding box. The model's loss function specifically penalizes errors in the box coordinates and the square roots of the width and height. By using square roots, the model ensures that a small error in a tiny object is penalized more heavily than the same error in a large object, which is crucial for finding small scraps of paper amidst larger debris.", color=WHITE).scale(0.6)
        narration.next_to(coord_terms, DOWN * 1)
        self.play(Create(narration))

        # Wait for completion
        self.wait()