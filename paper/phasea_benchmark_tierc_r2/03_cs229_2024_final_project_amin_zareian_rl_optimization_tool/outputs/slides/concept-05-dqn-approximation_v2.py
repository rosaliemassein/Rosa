from manim import *

class DQN_Approximation(Scene):
    def construct(self):
        # 1. Setup Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(UP)
        self.add(formula)

        # 2. Create the 5x5 pixel grid
        grid = VGroup(*[
            Square(side_length=0.6, stroke_width=2, fill_opacity=0.2, fill_color=BLUE)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.1).shift(LEFT * 4)
        
        grid_labels = VGroup(*[
            Text(str(i), font_size=12).move_to(grid[i])
            for i in range(25)
        ])
        
        self.play(Create(grid), Write(grid_labels))
        self.wait(1)

        # 3. Create the Neural Network components
        # Input Layer (25 nodes)
        input_layer = VGroup(*[
            Circle(radius=0.1, color=YELLOW, fill_opacity=0.8)
            for _ in range(25)
        ]).arrange(DOWN, buff=0.05).set_height(5.5).shift(LEFT * 0.5)

        # Hidden Layer (simplified)
        hidden_layer = VGroup(*[
            Circle(radius=0.15, color=WHITE, fill_opacity=0.3)
            for _ in range(8)
        ]).arrange(DOWN, buff=0.3).move_to(RIGHT * 1.5)

        # Output Layer (25 nodes)
        output_layer = VGroup(*[
            Circle(radius=0.1, color=YELLOW, fill_opacity=0.8)
            for _ in range(25)
        ]).arrange(DOWN, buff=0.05).set_height(5.5).shift(RIGHT * 3.5)

        # Connections (Visual subset to avoid clutter)
        connections = VGroup()
        for i in range(0, 25, 4): # Every 4th input node
            for h in hidden_layer:
                connections.add(Line(input_layer[i].get_right(), h.get_left(), stroke_width=0.5, stroke_opacity=0.2))
        for h in hidden_layer:
            for o in range(0, 25, 4): # Every 4th output node
                connections.add(Line(h.get_right(), output_layer[o].get_left(), stroke_width=0.5, stroke_opacity=0.2))

        # 4. Animate flattening grid into Input Layer
        self.play(
            AnimationGroup(*[
                ReplacementTransform(grid[i].copy(), input_layer[i])
                for i in range(25)
            ], lag_ratio=0.02),
            run_time=2
        )
        self.wait(0.5)

        # 5. Show NN structure
        self.play(
            Create(hidden_layer),
            Create(output_layer),
            Create(connections),
            run_time=2
        )
        self.wait(1)

        # 6. Highlight highest value output node
        # We'll pick pixel 12 (middle) as the "max" output
        max_index = 12
        max_node = output_layer[max_index]
        max_label = Text(f"Flip Pixel {max_index}", font_size=18, color=RED).next_to(max_node, RIGHT)
        
        self.play(
            max_node.animate.set_color(RED).scale(1.5),
            Write(max_label)
        )
        self.play(Indicate(max_node), Indicate(grid[max_index]))
        self.wait(1)

        # 7. Animate pixel flip in the original grid
        self.play(
            grid[max_index].animate.set_fill(RED, opacity=0.8),
            grid_labels[max_index].animate.set_color(WHITE),
            run_time=1
        )
        
        # Finishing sequence
        self.play(Flash(grid[max_index], color=RED, line_length=0.3))
        self.wait(2)