from manim import *
import numpy as np

class SemanticEmbedding(Scene):
    def construct(self):
        # 1. Setup 2D Environment
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-6, 6, 1],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.add(plane)

        # 2. Text labels for 'Deep Learning', 'Neural Networks', and 'Robotics'
        dl_label = Text("Deep Learning", color=RED).scale(0.6).move_to([3, 2.5, 0])
        nn_label = Text("Neural Networks", color=GREEN).scale(0.6).move_to([4, 1, 0])
        robotics_label = Text("Robotics", color=YELLOW).scale(0.6).move_to([-4, -2.5, 0])

        self.play(
            FadeIn(dl_label),
            FadeIn(nn_label),
            FadeIn(robotics_label)
        )
        self.wait(1)

        # 3. Transform labels into Dots at specific coordinates
        dl_pos = np.array([2.5, 2.0, 0])
        nn_pos = np.array([3.2, 1.4, 0])
        robot_pos = np.array([-4.5, -2.0, 0])

        dl_dot = Dot(dl_pos, color=RED)
        nn_dot = Dot(nn_pos, color=GREEN)
        robot_dot = Dot(robot_pos, color=YELLOW)

        self.play(
            Transform(dl_label, dl_dot),
            Transform(nn_label, nn_dot),
            Transform(robotics_label, robot_dot),
            run_time=2
        )
        self.wait(1)

        # 4. Dashed line to show proximity (distance)
        dist_line = DashedLine(dl_pos, nn_pos, color=WHITE)
        self.play(Create(dist_line))
        self.wait(1)

        # 5. Average vector logic for "Machine Learning"
        # Word 'Machine' and its vector
        m_word = Text("Machine", color=BLUE).scale(0.6).move_to([-5, 3, 0])
        m_vec_pos = np.array([-4, 1.5, 0])
        m_arrow = Arrow(ORIGIN, m_vec_pos, buff=0, color=BLUE, stroke_width=3)
        
        # Word 'Learning' and its vector
        l_word = Text("Learning", color=ORANGE).scale(0.6).move_to([-1, 3, 0])
        l_vec_pos = np.array([-2, 2.5, 0])
        l_arrow = Arrow(ORIGIN, l_vec_pos, buff=0, color=ORANGE, stroke_width=3)

        self.play(Write(m_word), Write(l_word))
        self.play(Create(m_arrow), Create(l_arrow))
        self.wait(1)

        # Merge them into a single central vector representing the average
        avg_pos = (m_vec_pos + l_vec_pos) / 2
        avg_arrow = Arrow(ORIGIN, avg_pos, buff=0, color=WHITE, stroke_width=5)
        avg_text = Text("Machine Learning", color=WHITE).scale(0.6).next_to(avg_pos, RIGHT)

        self.play(
            ReplacementTransform(VGroup(m_arrow, l_arrow), avg_arrow),
            ReplacementTransform(VGroup(m_word, l_word), avg_text),
            run_time=2
        )
        self.wait(1)

        # 6. Display the formula
        # Define the formula string directly
        formula_str = r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}"
        formula_tex = MathTex(formula_str, color=WHITE).scale(0.9)
        formula_tex.to_edge(UP).set_background_stroke(color=BLACK, width=4)
        
        self.play(Write(formula_tex))
        self.wait(2)

        # Move formula away for final frame
        self.play(formula_tex.animate.to_edge(DOWN).scale(0.7))
        self.wait(2)