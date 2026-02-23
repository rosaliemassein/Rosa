from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 grid of squares
        squares = VGroup(*[Square(color=BLUE) for _ in range(16)])
        squares.arrange_in_grid(rows=4, columns=4)
        squares.scale(1.2)

        # Color the left half red and right half blue
        for i in range(4):
            for j in range(2):
                squares[i*4 + 2*j].set_color(RED)

        # Draw green lines between adjacent pixels of different colors
        borders = VGroup()
        for i in range(4):
            for j in range(4):
                if squares[i*4 + j].get_color() != squares[i*4 + (j+1) % 4].get_color():
                    borders += Line(squares[i*4 + j].get_center(), squares[i*4 + (j+1) % 4].get_center()).set_stroke(GREEN, 2)
                if squares[i*4 + j].get_color() != squares[(i+1) % 4 * 4 + j].get_color():
                    borders += Line(squares[i*4 + j].get_center(), squares[(i+1) % 4 * 4 + j].get_center()).set_stroke(GREEN, 2)

        # Add the initial state to the screen
        self.add(borders, squares)
        self.wait(1)

        # Function to flip a color and update the border
        def flip_color_and_update(i, j):
            squares[i*4 + j].set_fill(RED if squares[i*4 + j].get_color() == BLUE else BLUE)
            new_borders = VGroup()
            for x in range(4):
                for y in range(4):
                    if squares[x*4 + y].get_color() != squares[x*4 + (y+1) % 4].get_color():
                        new_borders += Line(squares[x*4 + y].get_center(), squares[x*4 + (y+1) % 4].get_center()).set_stroke(GREEN, 2)
                    if squares[x*4 + y].get_color() != squares[(x+1) % 4 * 4 + y].get_center():
                        new_borders += Line(squares[x*4 + y].get_center(), squares[(x+1) % 4 * 4 + y].get_center()).set_stroke(GREEN, 2)
            self.play(Transform(borders, new_borders), Transform(squares[i*4 + j], squares[i*4 + j].copy()))
            self.wait(0.25)

        # Animate the squares flipping to a checkerboard pattern
        for i in range(4):
            for j in range(2, 4):
                flip_color_and_update(i, j)

        # Counter for red-blue adjacencies
        counter = MathTex(r"B = 0").set_color(WHITE).to_corner(UL)
        self.play(FadeIn(counter))
        for i in range(4):
            for j in range(2, 4):
                if squares[i*4 + j].get_color() != squares[i*4 + (j-1)].get_color():
                    counter[0] += 1
                if squares[i*4 + j].get_color() != squares[(i-1)*4 + j].get_center():
                    counter[0] += 1
                self.play(Indicate(counter))

        self.wait(2)