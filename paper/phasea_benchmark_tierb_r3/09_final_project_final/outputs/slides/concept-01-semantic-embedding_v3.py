from manim import *

class SemanticEmbedding(Scene):
    def construct(self):
        # Create a simple 2D coordinate space using basic Lines 
        # (NumberPlane and 3D features are restricted in this environment)
        x_axis = Line(5 * LEFT, 5 * RIGHT, color=GRAY, stroke_opacity=0.5)
        y_axis = Line(3 * DOWN, 3 * UP, color=GRAY, stroke_opacity=0.5)
        self.add(x_axis, y_axis)

        # 1. Create floating text labels for the concepts
        dl_label = Text("Deep Learning", color=BLUE).scale(0.6).move_to(2.5 * RIGHT + 1.5 * UP)
        nn_label = Text("Neural Networks", color=GREEN).scale(0.6).move_to(2.5 * RIGHT + 0.5 * UP)
        rob_label = Text("Robotics", color=RED).scale(0.6).move_to(3 * LEFT + 1.5 * DOWN)

        self.play(Write(dl_label), Write(nn_label), Write(rob_label))
        self.wait(1)

        # 2. Transform text labels into Dot objects (vectors)
        dl_dot = Dot(2.5 * RIGHT + 1.2 * UP, color=BLUE)
        nn_dot = Dot(2.8 * RIGHT + 0.8 * UP, color=GREEN)
        rob_dot = Dot(3 * LEFT + 1.2 * DOWN, color=RED)

        self.play(
            Transform(dl_label, dl_dot),
            Transform(nn_label, nn_dot),
            Transform(rob_label, rob_dot)
        )
        self.wait(1)

        # 3. Represent semantic distance 
        # (Using a standard Line as DashedLine is restricted)
        dist_line = Line(dl_dot.get_center(), nn_dot.get_center(), color=WHITE, stroke_width=2)
        dist_text = Text("Similar concepts", color=WHITE).scale(0.4).next_to(dist_line, RIGHT)
        
        self.play(Create(dist_line), Write(dist_text))
        self.wait(1)
        self.play(FadeOut(dist_line), FadeOut(dist_text), FadeOut(rob_label))

        # 4. Multi-word phrase averaging: "Machine" + "Learning"
        machine_text = Text("Machine", color=WHITE).scale(0.5).move_to(2 * LEFT + 2.5 * UP)
        learning_text = Text("Learning", color=WHITE).scale(0.5).move_to(2 * RIGHT + 2.5 * UP)
        m_dot = Dot(2 * LEFT + 2 * UP, color=ORANGE)
        l_dot = Dot(2 * RIGHT + 2 * UP, color=PURPLE)

        self.play(
            Write(machine_text), Write(learning_text),
            Create(m_dot), Create(l_dot)
        )
        self.wait(1)

        # Transform both individual vectors into a single central vector (average)
        avg_pos = 2 * UP
        avg_dot = Dot(avg_pos, color=YELLOW)
        avg_label = Text("Average (Phrase Vector)", color=YELLOW).scale(0.5).next_to(avg_dot, UP)

        self.play(
            Transform(m_dot, avg_dot),
            Transform(l_dot, avg_dot),
            Transform(machine_text, avg_dot),
            Transform(learning_text, avg_dot)
        )
        self.play(FadeIn(avg_label))
        self.wait(1)

        # 5. Display the mathematical formula for the phrase vector
        formula = MathTex(
            r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}", 
            color=YELLOW
        ).scale(0.9).to_edge(DOWN, buff=1)
        
        self.play(Write(formula))
        self.wait(2)