from manim import *

class SemanticEmbedding(Scene):
    def construct(self):
        # 1. Create a NumberPlane (2D representation of high-dimensional space)
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        self.play(Create(plane))

        # 2. Floating text labels for semantic concepts
        dl_text = Text("Deep Learning", font_size=24).set_color(BLUE)
        nn_text = Text("Neural Networks", font_size=24).set_color(RED)
        rt_text = Text("Robotics", font_size=24).set_color(GREEN)

        # Positioning labels spread out
        dl_text.move_to(UP * 2 + LEFT * 2)
        nn_text.move_to(UP * 2.5 + RIGHT * 2)
        rt_text.move_to(DOWN * 2 + LEFT * 3)

        self.play(Write(dl_text), Write(nn_text), Write(rt_text))
        self.wait(1)

        # 3. Transform text labels into Dot objects at specific coordinates
        dl_dot = Dot(point=[2, 1, 0], color=BLUE)
        nn_dot = Dot(point=[2.5, 0.8, 0], color=RED)
        rt_dot = Dot(point=[-4, -2, 0], color=GREEN)

        self.play(
            Transform(dl_text, dl_dot),
            Transform(nn_text, nn_dot),
            Transform(rt_text, rt_dot)
        )
        self.wait(1)

        # 4. Dashed line showing distance between similar concepts
        dl_dn_line = DashedLine(dl_dot.get_center(), nn_dot.get_center(), color=YELLOW)
        dist_label = Text("Similar concepts", font_size=16).next_to(dl_dn_line, UP, buff=0.1)
        
        self.play(Create(dl_dn_line), FadeIn(dist_label))
        self.wait(2)
        
        # Cleanup for the next phase
        self.play(FadeOut(dl_text, nn_text, rt_text, dl_dn_line, dist_label))

        # 5. Averaging words to find phrase center
        m_word = Text("Machine", font_size=28).move_to(LEFT * 3 + UP * 1)
        l_word = Text("Learning", font_size=28).move_to(RIGHT * 3 + UP * 1)
        
        m_vec = Dot(point=[-3, -1, 0], color=BLUE)
        l_vec = Dot(point=[3, -1, 0], color=RED)
        
        self.play(Write(m_word), Create(m_vec))
        self.play(Write(l_word), Create(l_vec))
        self.wait(1)

        # Merge them into a single central vector (Average)
        avg_vec = Dot(point=[0, -1, 0], color=PURPLE)
        phrase_label = Text("Machine Learning", font_size=28).move_to(DOWN * 2)

        self.play(
            Transform(m_vec, avg_vec),
            Transform(l_vec, avg_vec),
            Transform(m_word, phrase_label),
            Transform(l_word, phrase_label)
        )
        self.wait(1)

        # 6. Display the formula
        formula = MathTex(r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}", font_size=42)
        formula.to_edge(UP, buff=0.5)
        formula.set_background_stroke(color=BLACK, width=2)
        
        self.play(Write(formula))
        self.wait(3)