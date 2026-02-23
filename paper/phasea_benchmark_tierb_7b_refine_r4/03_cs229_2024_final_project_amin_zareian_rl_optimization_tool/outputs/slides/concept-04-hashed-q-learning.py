from manim import *

class HashedQLearning(Scene):
    def construct(self):
        # Define the grids
        grid1 = VGroup(*[Square().scale(0.5).shift(RIGHT * i + DOWN * j) for i in range(2) for j in range(2)])
        grid2 = VGroup(*[Square().scale(0.5).shift(RIGHT * i + DOWN * j) for i in range(2, 4) for j in range(2)])
        grid3 = VGroup(*[Square().scale(0.5).shift(RIGHT * i + DOWN * j) for i in range(2, 4) for j in range(2, 4)])
        
        # Highlight the grids
        grid1.set_color(BLUE)
        grid2.set_color(GREEN)
        grid3.set_color(RED)
        
        # Hash Function box
        hash_box = Rectangle(height=1, width=2).to_edge(UP)
        hash_text = MathTex(r"\text{Hash Function}").next_to(hash_box, direction=DOWN)
        
        # Q-Table
        q_table = VGroup(*[Text(str(i)).scale(0.5).shift(RIGHT * 1.5 + DOWN * j) for i in range(3) for j in range(2)]).shift(DOWN * 1.5)
        
        # Draw arrows from grids to Hash Function
        arrow1 = Arrow(grid1[0].get_bottom(), hash_box.get_top()).shift(LEFT * 0.5)
        arrow2 = Arrow(grid2[0].get_bottom(), hash_box.get_top()).shift(LEFT * 1.5)
        arrow3 = Arrow(grid3[0].get_bottom(), hash_box.get_top()).shift(LEFT * 2.5)
        
        # Draw arrows from Hash Function to Q-Table
        q_table_row1 = VGroup(*[Text(str(i)).scale(0.5).shift(RIGHT * 1.5 + DOWN * j) for i in range(2) for j in range(1)]).shift(DOWN * 1.5)
        q_table_row2 = VGroup(*[Text(str(i)).scale(0.5).shift(RIGHT * 1.5 + DOWN * j) for i in range(2, 3) for j in range(1)]).shift(DOWN * 0.5)
        q_table_row3 = VGroup(*[Text(str(i)).scale(0.5).shift(RIGHT * 1.5 + DOWN * j) for i in range(2, 3) for j in range(1)]).shift(DOWN * 2.5)
        
        arrow4 = Arrow(hash_box.get_bottom(), q_table_row1.get_top()).shift(RIGHT * 0.5)
        arrow5 = Arrow(hash_box.get_bottom(), q_table_row2.get_top()).shift(RIGHT * 1.5)
        arrow6 = Arrow(hash_box.get_bottom(), q_table_row3.get_top()).shift(RIGHT * 2.5)
        
        # Indicate collision
        collision = Flash(grid1, color=RED, run_time=0.5)
        
        # Animation
        self.play(Create(grid1), Create(grid2), Create(grid3))
        self.wait(0.5)
        self.play(Create(hash_box), Write(hash_text))
        self.wait(0.5)
        self.play(Create(q_table))
        self.wait(0.5)
        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(0.5)
        self.play(Create(arrow4), Create(arrow5), Create(arrow6))
        self.wait(0.5)
        self.play(collision, LaggedStart(FadeIn(grid2), FadeOut(grid1)), run_time=0.5)
        self.wait(0.5)