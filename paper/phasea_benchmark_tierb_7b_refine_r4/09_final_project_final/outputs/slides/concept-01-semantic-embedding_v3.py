from manim import *

class SemanticEmbedding(Scene):
    def construct(self):
        # 1. Manually create a coordinate system (since Axes/NumberPlane are restricted)
        x_axis = Line(LEFT * 6, RIGHT * 6, color=GREY, stroke_width=1)
        y_axis = Line(DOWN * 4, UP * 4, color=GREY, stroke_width=1)
        self.add(x_axis, y_axis)

        # 2. Text labels for 'Deep Learning', 'Neural Networks', and 'Robotics'
        dl_label = Text("Deep Learning", font_size=24)
        nn_label = Text("Neural Networks", font_size=24)
        r_label = Text("Robotics", font_size=24)

        # Initial grouping of labels
        labels_group = VGroup(dl_label, nn_label, r_label).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.play(FadeIn(labels_group))
        self.wait(1)

        # 3. Define mapping coordinates
        pos_dl = RIGHT * 2 + UP * 1.5
        pos_nn = RIGHT * 2.5 + UP * 1.2
        pos_r = LEFT * 3 + DOWN * 1.5

        dot_dl = Dot(pos_dl, color=BLUE)
        dot_nn = Dot(pos_nn, color=BLUE)
        dot_r = Dot(pos_r, color=RED)

        # 4. Animate transformation from text to dots
        self.play(
            Transform(dl_label, dot_dl),
            Transform(nn_label, dot_nn),
            Transform(r_label, dot_r)
        )
        self.wait(1)

        # 5. Show proximity between similar concepts
        # (Using solid Line instead of DashedLine due to restrictions)
        proximity_line = Line(pos_dl, pos_nn, color=YELLOW, stroke_width=2)
        self.play(Create(proximity_line))
        self.wait(1)

        # 6. Display the mathematical formula
        formula = MathTex(r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}", font_size=36)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 7. Averaging multi-word phrases: 'Machine' and 'Learning'
        m_word = Text("Machine", font_size=24, color=GREEN)
        l_word = Text("Learning", font_size=24, color=GREEN)
        m_word.to_corner(UR)
        l_word.next_to(m_word, DOWN, aligned_edge=RIGHT)

        self.play(FadeIn(m_word), FadeIn(l_word))

        pos_m = LEFT * 2.5 + UP * 1.5
        pos_l = LEFT * 0.5 + UP * 2.0
        pos_avg = (pos_m + pos_l) / 2

        dot_m = Dot(pos_m, color=GREEN)
        dot_l = Dot(pos_l, color=GREEN)
        dot_avg = Dot(pos_avg, color=WHITE)

        vec_m = Arrow(ORIGIN, pos_m, buff=0, color=GREEN, stroke_width=3)
        vec_l = Arrow(ORIGIN, pos_l, buff=0, color=GREEN, stroke_width=3)
        vec_avg = Arrow(ORIGIN, pos_avg, buff=0, color=WHITE, stroke_width=5)

        # Transform keywords into vectors
        self.play(
            Transform(m_word, dot_m),
            Transform(l_word, dot_l),
            Create(vec_m),
            Create(vec_l)
        )
        self.wait(1)

        # 8. Merge vectors into their average (center of gravity)
        self.play(
            Transform(vec_m, vec_avg),
            Transform(vec_l, vec_avg),
            Transform(m_word, dot_avg),
            Transform(l_word, dot_avg),
            FadeOut(proximity_line),
            FadeOut(dl_label),
            FadeOut(nn_label),
            FadeOut(r_label)
        )
        self.wait(2)