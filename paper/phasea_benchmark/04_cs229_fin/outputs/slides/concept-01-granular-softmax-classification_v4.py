from manim import *

class ConceptAnimation01GranularSoftmaxClassification(Scene):
    def construct(self):
        # Directional and color constants to avoid undefined identifiers
        D_UP = [0, 1, 0]
        D_RIGHT = [1, 0, 0]
        D_LEFT = [-1, 0, 0]
        D_DOWN = [0, -1, 0]
        C_BLUE = "#0000FF"
        C_WHITE = "#FFFFFF"
        C_GREEN = "#00FF00"
        C_RED = "#FF0000"
        C_YELLOW = "#FFFF00"

        # 1. Input Image Representation (Plastic Bottle)
        # Replacing Rectangle with a VGroup of 4 Lines
        i_top = Line([-5, 1, 0], [-3, 1, 0], color=C_BLUE)
        i_bot = Line([-5, -1, 0], [-3, -1, 0], color=C_BLUE)
        i_l = Line([-5, 1, 0], [-5, -1, 0], color=C_BLUE)
        i_r = Line([-3, 1, 0], [-3, -1, 0], color=C_BLUE)
        input_box = VGroup(i_top, i_bot, i_l, i_r)
        input_text = Text("Plastic Bottle", font_size=16).move_to(input_box.get_center())
        input_mobj = VGroup(input_box, input_text)

        # 2. CNN Layers
        # Replacing Rectangles with hand-drawn skinny boxes using Lines
        cnn_layers = VGroup()
        for i in range(4):
            lx = -2 + (i * 0.4)
            l_rect = VGroup(
                Line([lx, 1, 0], [lx + 0.2, 1, 0], color=C_WHITE),
                Line([lx + 0.2, 1, 0], [lx + 0.2, -1, 0], color=C_WHITE),
                Line([lx + 0.2, -1, 0], [lx, -1, 0], color=C_WHITE),
                Line([lx, -1, 0], [lx, 1, 0], color=C_WHITE)
            )
            cnn_layers.add(l_rect)

        # 3. Data Vector and Softmax Formula
        # Using Text instead of MathTex
        v_text = Text("x_i = [2.1, 0.4, ..., -1.2]", font_size=18).next_to(cnn_layers, D_RIGHT, buff=0.5)
        sm_formula = Text("Softmax(x_i) = exp(x_i) / Sum(exp(x_j))", font_size=18).move_to([3, 3, 0]).set_color(C_YELLOW)

        # 4. Connecting Data Flow
        # Using Create instead of GrowArrow
        arrow1 = Arrow(input_mobj.get_right(), cnn_layers.get_left(), buff=0.1)
        arrow2 = Arrow(cnn_layers.get_right(), v_text.get_left(), buff=0.1)

        # 5. Bar Chart for Probabilities
        # Replacing Axes with a simple Line and bars with thick vertical Lines
        x_axis = Line([-4, -2.5, 0], [4, -2.5, 0], color=C_WHITE)
        bars = VGroup()
        for i in range(20):
            # Heights represent categorical probabilities
            h = 0.25
            if i == 14: # Target category
                h = 2.2
            bx = -4 + (i * 8 / 19)
            bar = Line([bx, -2.5, 0], [bx, -2.5 + h, 0], stroke_width=10, color=C_GREEN)
            bars.add(bar)

        # 6. Classification Label
        pred_label = Text("Plastic Bottle", font_size=20, color=C_RED).next_to(bars[14], D_UP, buff=0.2)

        # --- Animation Sequence ---
        # 1. Show Input Image
        self.play(FadeIn(input_mobj))
        self.wait(0.5)

        # 2. Flow into CNN Layers
        self.play(Create(arrow1), Create(cnn_layers))
        self.wait(0.5)

        # 3. Flow into raw score vector
        self.play(Create(arrow2), Write(v_text))
        self.wait(1)

        # 4. Show Softmax transformation
        self.play(Write(sm_formula))
        self.wait(1)

        # 5. Transform into probability chart
        self.play(Create(x_axis))
        self.play(Create(bars), run_time=2)
        self.wait(1)

        # 6. Highlight highest bar (Replacing Indicate with manual scale and color)
        self.play(
            bars[14].animate.set_color(C_RED).scale(1.2, about_edge=D_DOWN),
            Write(pred_label)
        )
        self.wait(3)