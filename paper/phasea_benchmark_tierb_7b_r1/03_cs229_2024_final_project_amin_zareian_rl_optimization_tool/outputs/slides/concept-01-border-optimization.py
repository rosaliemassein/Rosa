from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 grid of squares
        squares = VGroup(*[Square(side_length=1) for _ in range(16)])
        squares.arrange(RIGHT, 4).arrange(DOWN)

        # Color the left half red and the right half blue
        for i in range(4):
            squares[4*i:4*(i+1)].set_fill(color=RED)
        for i in range(4):
            squares[4*(i+4):4*(i+5)].set_fill(color=BLUE)

        # Draw green border lines
        border_lines = VGroup()
        for i in range(4):
            for j in range(3):
                if squares[i*4+j].get_color() != squares[i*4+j+1].get_color():
                    border_lines.add(Line(squares[i*4+j].get_center(), squares[i*4+j+1].get_center()).set_stroke(GREEN, 2))
                if squares[j*4+i].get_color() != squares[(j+1)*4+i].get_color():
                    border_lines.add(Line(squares[j*4+i].get_center(), squares[(j+1)*4+i].get_center()).set_stroke(GREEN, 2))

        # Add squares and border lines to the scene
        self.play(FadeIn(squares))
        self.wait(1)
        self.play(Create(border_lines))

        # Animate the squares flipping colors to a checkerboard pattern
        for i in range(4):
            for j in range(4):
                if (i+j) % 2 == 1:
                    squares[i*4+j].set_fill(color=BLUE)
                else:
                    squares[i*4+j].set_fill(color=RED)
        self.wait(1)

        # Animation group to update border lines
        border_update = AnimationGroup()
        for i in range(4):
            for j in range(3):
                if squares[i*4+j].get_color() != squares[i*4+j+1].get_color():
                    border_update += Transform(border_lines[2*i+2*j], Line(squares[i*4+j].get_center(), squares[i*4+j+1].get_center()).set_stroke(GREEN, 2))
                if squares[j*4+i].get_color() != squares[(j+1)*4+i].get_color():
                    border_update += Transform(border_lines[2*i*2+8*j], Line(squares[j*4+i].get_center(), squares[(j+1)*4+i].get_center()).set_stroke(GREEN, 2))

        self.play(border_update)

        # Add checkerboard pattern to the scene
        self.wait(1)
        self.play(Create(squares))

        # Show the counter in the corner
        counter = MathTex(r"B = 8").set_color(BLACK).to_edge(RIGHT, buff=1)
        self.play(Create(counter))