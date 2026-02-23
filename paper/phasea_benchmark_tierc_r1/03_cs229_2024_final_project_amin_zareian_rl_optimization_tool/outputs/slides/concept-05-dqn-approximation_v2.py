from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Pixel Grid (5x5)
        grid = VGroup(*[
            Square(side_length=0.4, fill_opacity=1, fill_color=WHITE, stroke_color=GRAY, stroke_width=1)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.05).shift(LEFT * 4)
        
        grid_title = Text("Pixel Grid (State s)", font_size=24).next_to(grid, UP)
        self.play(Create(grid), Write(grid_title))
        self.wait(1)

        # 2. Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(UP)
        self.play(Write(formula))

        # 3. Flattening into 1D Vector
        # We'll create a copy and move them into a column
        flat_grid = grid.copy()
        self.play(
            flat_grid.animate.arrange(DOWN, buff=0.02).scale(0.4).move_to(LEFT * 2),
            grid_title.animate.scale(0.7).next_to(flat_grid, UP, buff=0.2),
            run_time=2
        )
        
        # 4. Neural Network Architecture
        # Input Layer (abbreviated for visual clarity but representing 25 inputs)
        input_neurons = VGroup(*[Circle(radius=0.05, color=WHITE) for _ in range(15)]).arrange(DOWN, buff=0.1).next_to(flat_grid, RIGHT, buff=0.5)
        dots_label = Text("...", font_size=20).rotate(90*DEGREES).move_to(input_neurons.get_center())
        
        # Hidden Layer
        hidden_neurons = VGroup(*[Circle(radius=0.15, color=BLUE) for _ in range(4)]).arrange(DOWN, buff=0.4).shift(RIGHT * 0.5)
        
        # Output Layer
        output_neurons = VGroup(*[Circle(radius=0.2, color=GREEN) for _ in range(5)]).arrange(DOWN, buff=0.5).shift(RIGHT * 3)
        output_labels = VGroup(*[
            Text(f"Flip Pixel {i+1}", font_size=18).next_to(output_neurons[i], RIGHT)
            for i in range(5)
        ])

        # Connections (simplified)
        connections_1 = VGroup()
        for i in range(0, 15, 3):
            for h in hidden_neurons:
                connections_1.add(Line(input_neurons[i].get_right(), h.get_left(), stroke_width=0.5, stroke_opacity=0.3))
        
        connections_2 = VGroup()
        for h in hidden_neurons:
            for o in output_neurons:
                connections_2.add(Line(h.get_right(), o.get_left(), stroke_width=1, stroke_opacity=0.5))

        nn_group = VGroup(input_neurons, hidden_neurons, output_neurons, connections_1, connections_2, output_labels)
        self.play(Create(nn_group))
        self.wait(1)

        # 5. Data Flow (Visualizing values entering NN)
        flow_dots = VGroup(*[Dot(radius=0.03, color=YELLOW) for _ in range(5)])
        flow_dots.move_to(flat_grid.get_center())
        
        self.play(
            Succession(
                flow_dots.animate.move_to(input_neurons.get_center()),
                flow_dots.animate.move_to(hidden_neurons.get_center()),
                flow_dots.animate.move_to(output_neurons.get_center()),
            ),
            run_time=2
        )

        # 6. Highlight Highest Output Node
        # Let's say "Flip Pixel 3" has the highest Q-value
        target_index = 2
        highlight_circle = output_neurons[target_index].copy().set_color(YELLOW).scale(1.2)
        
        self.play(
            Indicate(output_neurons[target_index], color=YELLOW),
            output_labels[target_index].animate.set_color(YELLOW).scale(1.2),
            Create(highlight_circle)
        )
        self.wait(1)

        # 7. Corresponding Pixel in Grid Flipping
        # We index 2 in the flattened version, which is the 3rd square in the original grid
        target_pixel = grid[target_index]
        self.play(
            target_pixel.animate.set_fill(RED),
            Flash(target_pixel, color=RED)
        )
        
        # 8. Final Narration/Conclusion
        narration = Text(
            "Deep Q-Network approximates the rewards for each action.",
            font_size=20, color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(narration))
        self.wait(3)

# Note: PinholeCamera is not standard in Manim scenes.
# Standard Camera is used. 
# scene_args removed as Manim CLI or config handles background.