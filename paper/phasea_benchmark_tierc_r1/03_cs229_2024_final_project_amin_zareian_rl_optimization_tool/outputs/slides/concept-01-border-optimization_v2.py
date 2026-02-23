from manim import *

class Concept01BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 VGroup of Square objects
        squares = VGroup(*[
            Square(side_length=0.8, fill_color=c) for c in [RED, BLUE]
        ])
        
        # Place the squares on a grid
        squares.arrange_in_grid(rows=2, cols=2)

        # Set the positions of each square
        squares[0].move_to(LEFT *2.5)
        squares[1].next_to(squares[0], RIGHT, buff=0)
        squares[2].move_to(DOWN)
        squares[3].next_to(squares[2], UP, buff=0)

        # Draw thick green lines between adjacent pixels of different colors
        borders = VGroup(
            DashedLine(squares[0][0], squares[1][0]),
            DashedLine(squares[1][0], squares[2][0]),
            DashedLine(squares[2][0], squares[3][0]),
            DashedLine(squares[3][0], squares[0][0]),
            DashedLine(squares[1][1], squares[2][1]),
            DashedLine(squares[2][1], squares[3][1]),
            DashedLine(squares[3][1], squares[0][1]),
        )
        borders.set_stroke(BLUE, 2)

        # Animate the squares flipping colors one by one to a checkerboard pattern
        flip_count = 0
        for s in squares:
            if flip_count % 2 == 0:
                s.set_fill(RED)
            else:
                s.set_fill(BLUE)

            # Update the borders dynamically
            for border in borders:
                if (border.get_start() in squares[0] and border.get_end() in squares[1]) or \
                   (border.get_start() in squares[1] and border.get_end() in squares[2]) or \
                   (border.get_start() in squares[2] and border.get_end() in squares[3]) or\
                   (border.get_start() in squares[3] and border.get_end() in squares[0]) or\
                   (border.get_start() in squares[1] and border.get_end() in squares[2]) or\
                   (border.get_start() in squares[2] and border.get_end() in squares[3]) or\
                   (border.get_start() in squares[3] and border.get_end() in squares[0]):
                    border.set_stroke(BLUE, 2)
                else:
                    border.set_stroke(GREEN, 2)

            # Update the counter
            flip_count += 1

        # Display the results
        self.play(Create(squares), FadeIn(borders))
        self.wait()

        # Display the formula
        formula = Text(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").scale(0.7)
        formula.to_corner(DR, buff=1)
        self.play(Write(formula))

        # Draw the counter
        counter = DecimalNumber(flip_count, num_decimal_places=0).scale(1.5)
        counter.move_to(RIGHT*3, UP*2)
        self.play(Create(counter))