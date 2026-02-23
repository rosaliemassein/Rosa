import numpy as np
from manim import *

class Concept01SemanticEmbedding(Scene):
    def construct(self):
        # Manually create axes since Axes and NumberPlane are restricted
        x_axis = Line(LEFT * 5, RIGHT * 5, color=GREY_B)
        y_axis = Line(DOWN * 3.5, UP * 3.5, color=GREY_B)
        self.add(x_axis, y_axis)

        # Coordinate positions
        p_dl = np.array([-3, 1.5, 0])
        p_nn = np.array([-2.2, 1.0, 0])
        p_ro = np.array([3, -2, 0])

        # Floating text labels
        t_dl = Tex("Deep Learning").scale(0.7).move_to(p_dl + UP * 0.5)
        t_nn = Tex("Neural Networks").scale(0.7).move_to(p_nn + DOWN * 0.5)
        t_ro = Tex("Robotics").scale(0.7).move_to(p_ro + UP * 0.5)

        # 1. Pop up floating text labels
        self.play(Write(t_dl), Write(t_nn), Write(t_ro))
        self.wait(1)

        # 2. Transform text labels into Dot objects
        dot_dl = Dot(p_dl, color=BLUE)
        dot_nn = Dot(p_nn, color=BLUE)
        dot_ro = Dot(p_ro, color=WHITE)

        self.play(
            Transform(t_dl, dot_dl),
            Transform(t_nn, dot_nn),
            Transform(t_ro, dot_ro)
        )
        self.wait(1)

        # 3. Connection line to show proximity (Replacing DashedLine with basic Line)
        proximity_line = Line(p_dl, p_nn, color=YELLOW)
        self.play(Create(proximity_line))
        self.wait(1)
        self.play(FadeOut(proximity_line))

        # 4. Display the formula
        formula = MathTex(r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}").to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 5. Multi-word phrase vectors
        origin = np.array([0, 0, 0])
        p_machine = np.array([1, -1, 0])
        p_learning = np.array([3, 1, 0])
        p_avg = (p_machine + p_learning) / 2

        # Create vectors using Line + add_tip (often safer than Arrow in restricted environments)
        v_m = Line(origin, p_machine, color=GREEN).add_tip()
        v_m_label = Tex("Machine").scale(0.6).next_to(p_machine, RIGHT)
        
        v_l = Line(origin, p_learning, color=GREEN).add_tip()
        v_l_label = Tex("Learning").scale(0.6).next_to(p_learning, RIGHT)

        self.play(Create(v_m), Write(v_m_label))
        self.play(Create(v_l), Write(v_l_label))
        self.wait(1)

        # 6. Transform and merge into average position vector
        v_avg = Line(origin, p_avg, color=GOLD).add_tip()
        v_avg_label = Tex("Machine Learning").scale(0.7).next_to(p_avg, DOWN)

        self.play(
            Transform(VGroup(v_m, v_l), v_avg),
            Transform(VGroup(v_m_label, v_l_label), v_avg_label),
            FadeOut(t_dl), FadeOut(t_nn), FadeOut(t_ro)
        )
        
        self.wait(2)