from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create the 5x5 pixel grid
        grid = VGroup(*[
            Square(side_length=0.5, fill_opacity=0.2, stroke_width=2) 
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.1)
        grid.shift(LEFT * 4)
        
        grid_title = Text("5x5 Pixel Grid", font_size=24).next_to(grid, UP)
        
        # Randomly fill some pixels to represent state
        for i in [2, 7, 12, 13, 18]:
            grid[i].set_fill(WHITE, opacity=0.8)

        self.play(Create(grid), Write(grid_title))
        self.wait(1)

        # 2. Flatten the grid into a 1D vector
        flattened_vector = grid.copy()
        self.play(
            flattened_vector.animate.arrange(RIGHT, buff=0.05).scale(0.5).to_edge(UP),
            grid_title.animate.scale(0.7).to_edge(UP).shift(LEFT * 2),
            run_time=2
        )
        
        # 3. Neural Network setup
        # Input Layer
        input_layer = VGroup(*[Circle(radius=0.1, color=BLUE, fill_opacity=0.5) for _ in range(12)]).arrange(DOWN, buff=0.15)
        input_dots = MathTex(r"\vdots").move_to(input_layer.get_center())
        input_layer.shift(RIGHT * 1)
        
        # Hidden Layer
        hidden_layer = VGroup(*[Circle(radius=0.1, color=WHITE, fill_opacity=0.3) for _ in range(8)]).arrange(DOWN, buff=0.2)
        hidden_layer.shift(RIGHT * 3)
        
        # Output Layer
        output_layer = VGroup(*[Circle(radius=0.1, color=GREEN, fill_opacity=0.5) for _ in range(12)]).arrange(DOWN, buff=0.15)
        output_dots = MathTex(r"\vdots").move_to(output_layer.get_center())
        output_layer.shift(RIGHT * 5)
        
        nn_group = VGroup(input_layer, hidden_layer, output_layer)
        nn_title = Text("Deep Q-Network", font_size=24).next_to(nn_group, UP)

        # Connections
        connections = VGroup()
        for i in [0, 3, 6, 9, 11]:
            for j in [0, 3, 7]:
                connections.add(Line(input_layer[i].get_right(), hidden_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.3))
        for i in [0, 3, 7]:
            for j in [0, 3, 6, 9, 11]:
                connections.add(Line(hidden_layer[i].get_right(), output_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.3))

        self.play(
            Create(input_layer),
            Create(hidden_layer),
            Create(output_layer),
            Create(connections),
            Write(nn_title),
            Write(input_dots),
            Write(output_dots)
        )
        
        # 4. Show values flowing
        flow_lines = VGroup(*[
            Line(flattened_vector[i].get_bottom(), input_layer[i % 12].get_top(), stroke_width=1, color=BLUE)
            for i in range(0, 25, 2)
        ])
        self.play(Create(flow_lines), run_time=1)
        self.play(FadeOut(flow_lines))

        # 5. Highlight the output node with the highest value
        target_index = 6
        target_node = output_layer[target_index]
        highlight_box = SurroundingRectangle(target_node, color=YELLOW, buff=0.1)
        q_label = MathTex(r"Q(s, a; \theta)", font_size=24).next_to(target_node, RIGHT)

        self.play(
            target_node.animate.set_fill(YELLOW, opacity=1).scale(1.5),
            Create(highlight_box),
            Write(q_label)
        )
        self.wait(1)

        # 6. Flip corresponding pixel in the original grid
        grid_pixel_to_flip = grid[12]
        self.play(
            Indicate(grid_pixel_to_flip),
            grid_pixel_to_flip.animate.set_fill(YELLOW, opacity=1),
            target_node.animate.scale(1/1.5)
        )

        # 7. Final Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(formula))
        self.wait(2)

        # Final Transition
        narration = Text("Transition from tabular RL to Deep RL.", font_size=30).to_edge(DOWN)
        self.play(ReplacementTransform(formula, narration))
        self.wait(2)