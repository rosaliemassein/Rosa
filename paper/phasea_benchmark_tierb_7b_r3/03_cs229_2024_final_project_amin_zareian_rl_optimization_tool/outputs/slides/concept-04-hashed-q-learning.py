from manim import *

class HashedQLearning(Scene):
    def construct(self):
        # Define the grid patterns
        grid1 = Square(tiled=True).scale(0.8)
        grid2 = Square(tiled=True).scale(0.8).rotate(TAU/4)
        grid3 = Square(tiled=True).scale(0.8).rotate(TAU/2)

        # Define the hash function box
        hash_box = Rectangle(height=1.5, width=3).to_edge(UP)
        Text("Hash Function").next_to(hash_box, UP)

        # Define the Q-table
        q_table = VGroup(*[
            MathTex(r"a", r"b", r"c", r"d"),
            MathTex(r"e", r"f", r"g", r"h"),
            MathTex(r"i", r"j", r"k", r"l")
        ]).arrange(DOWN, buff=0.5).next_to(hash_box, RIGHT)

        # Create arrows from grids to hash function
        arrow1 = Arrow(grid1.get_center(), hash_box.get_corner(UR), buff=0.3)
        arrow2 = Arrow(grid2.get_center(), hash_box.get_corner(UR), buff=0.3)
        arrow3 = Arrow(grid3.get_center(), hash_box.get_corner(UR), buff=0.3)

        # Create arrows from hash function to Q-table
        arrow4 = Arrow(hash_box.get_corner(DL), q_table[0].get_center(), buff=0.3)
        arrow5 = Arrow(hash_box.get_corner(DL), q_table[1].get_center(), buff=0.3)
        arrow6 = Arrow(hash_box.get_corner(DL), q_table[2].get_center(), buff=0.3)

        # Show the grids and arrows
        self.play(Create(grid1), Create(grid2), Create(grid3))
        self.wait(0.5)
        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(0.5)
        self.play(Create(arrow4), Create(arrow5), Create(arrow6))
        self.wait(0.5)

        # Highlight the collision
        highlight = SurroundingRectangle(q_table[1], color=RED)
        self.play(Create(highlight), Indicate(arrow2, color=RED))
        self.wait(0.5)
        self.play(FadeOut(highlight))

        # Wait for the animation to finish
        self.wait(2)