from manim import *

class ConceptEmbedding(Scene):
    def construct(self):
        # 1. Coordinate Indicators (Mimicking a coordinate plane since NumberPlane is disallowed)
        x_axis = Line(LEFT * 5, RIGHT * 5, color=GREY_B)
        y_axis = Line(DOWN * 3, UP * 3, color=GREY_B)
        self.add(x_axis, y_axis)

        # 2. Text Labels for Concepts
        # Positioning them to illustrate proximity in semantic space
        dl_label = Text("Deep Learning").scale(0.5).move_to([2, 2, 0])
        nn_label = Text("Neural Networks").scale(0.5).move_to([2.5, 1.3, 0])
        ro_label = Text("Robotics").scale(0.5).move_to([-3, -1.5, 0])

        self.play(Write(dl_label), Write(nn_label), Write(ro_label))
        self.wait(1)

        # 3. Transform Text Labels into Dot Objects
        dl_dot = Dot([2, 2, 0], color=BLUE)
        nn_dot = Dot([2.5, 1.3, 0], color=BLUE)
        ro_dot = Dot([-3, -1.5, 0], color=RED)

        self.play(
            Transform(dl_label, dl_dot),
            Transform(nn_label, nn_dot),
            Transform(ro_label, ro_dot)
        )
        self.wait(1)

        # 4. Show distance (Using Line as DashedLine is disallowed)
        # Deep Learning and Neural Networks are close
        dist_near = Line(dl_dot.get_center(), nn_dot.get_center(), color=YELLOW)
        # Robotics is far from Deep Learning
        dist_far = Line(dl_dot.get_center(), ro_dot.get_center(), color=WHITE)

        self.play(Create(dist_near))
        self.play(Create(dist_far))
        self.wait(1)

        # 5. Display Formula and Clear Scene
        self.play(
            FadeOut(dl_label), FadeOut(nn_label), FadeOut(ro_label),
            FadeOut(dist_near), FadeOut(dist_far),
            FadeOut(x_axis), FadeOut(y_axis)
        )

        formula = MathTex(r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}")
        self.play(Write(formula))
        self.play(formula.animate.to_edge(UP))
        self.wait(1)

        # 6. Averaging logic: Machine + Learning = Machine Learning
        # Define vector positions
        v_machine_pos = [-2.5, -0.5, 0]
        v_learning_pos = [1.5, 1.5, 0]
        # Calculate average position: ([-2.5+1.5]/2, [-0.5+1.5]/2) = (-0.5, 0.5)
        v_avg_pos = [-0.5, 0.5, 0]

        # Use Arrow as Vector is disallowed
        arrow_m = Arrow(ORIGIN, v_machine_pos, buff=0, color=GREEN)
        lab_m = Text("Machine").scale(0.5).next_to(v_machine_pos, DOWN)

        arrow_l = Arrow(ORIGIN, v_learning_pos, buff=0, color=ORANGE)
        lab_l = Text("Learning").scale(0.5).next_to(v_learning_pos, UP)

        self.play(Create(arrow_m), Write(lab_m))
        self.play(Create(arrow_l), Write(lab_l))
        self.wait(1)

        # Merge vectors and words into the average central vector
        arrow_avg = Arrow(ORIGIN, v_avg_pos, buff=0, color=YELLOW)
        lab_avg = Text("Machine Learning").scale(0.6).next_to(v_avg_pos, RIGHT)

        self.play(
            Transform(arrow_m, arrow_avg),
            Transform(arrow_l, arrow_avg),
            Transform(lab_m, lab_avg),
            Transform(lab_l, lab_avg)
        )
        self.wait(2)