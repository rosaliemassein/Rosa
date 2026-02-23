from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # 1. Formula display
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(UP)
        self.play(Write(formula))

        # 2. Create a 5x5 pixel grid
        # Using squares to represent pixels clearly
        grid = VGroup(*[
            Square(side_length=0.4, fill_opacity=1, fill_color=WHITE, stroke_width=1)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.1)
        grid.shift(LEFT * 3)
        self.play(Create(grid))
        self.wait(1)

        # 3. Animate 'flattening' into a 1D vector
        # We'll create a flattened version to the right
        flattened_vector = VGroup(*[
            Square(side_length=0.2, fill_opacity=1, fill_color=WHITE, stroke_width=0.5)
            for _ in range(25)
        ]).arrange(DOWN, buff=0.05).scale(0.8).shift(LEFT * 0.5)

        self.play(
            ReplacementTransform(grid.copy(), flattened_vector),
            grid.animate.scale(0.5).to_edge(UP).to_edge(LEFT)
        )
        self.wait()

        # 4. Neural Network Representation
        # Input Layer (matching the flattened vector)
        input_layer = VGroup(*[Dot(radius=0.05) for _ in range(25)]).arrange(DOWN, buff=0.05).next_to(flattened_vector, RIGHT, buff=0.5)
        
        # Hidden Layer
        hidden_layer = VGroup(*[Dot(radius=0.08) for _ in range(8)]).arrange(DOWN, buff=0.2).next_to(input_layer, RIGHT, buff=1.5)
        
        # Output Layer (matching action space, let's say 25 actions for 25 pixels)
        output_layer = VGroup(*[Dot(radius=0.08, color=BLUE) for _ in range(25)]).arrange(DOWN, buff=0.05).next_to(hidden_layer, RIGHT, buff=1.5)
        
        nn_group = VGroup(input_layer, hidden_layer, output_layer)
        
        # Connections
        connections1 = VGroup()
        for i in range(0, 25, 3): # Sparsely visualize connections for performance/clarity
            for h in hidden_layer:
                connections1.add(Line(input_layer[i].get_center(), h.get_center(), stroke_width=0.5, stroke_opacity=0.3))
        
        connections2 = VGroup()
        for h in hidden_layer:
            for o in range(0, 25, 3):
                connections2.add(Line(h.get_center(), output_layer[o].get_center(), stroke_width=0.5, stroke_opacity=0.3))

        self.play(
            Create(input_layer),
            Create(hidden_layer),
            Create(output_layer),
            run_time=2
        )
        self.play(Create(connections1), Create(connections2), run_time=1)

        # 5. Data flowing from vector to input
        flow_animations = []
        for i in range(25):
            flow_animations.append(flattened_vector[i].animate.move_to(input_layer[i]))
        
        self.play(*flow_animations)
        self.wait(0.5)

        # 6. Highlight highest output node
        max_index = 12 # Middle pixel
        highlight_circle = Circle(radius=0.15, color=YELLOW).move_to(output_layer[max_index])
        
        self.play(
            Indicate(output_layer[max_index], color=RED, scale_factor=2),
            Create(highlight_circle)
        )
        
        # Label the node
        label = Text(f"Flip Pixel {max_index}", font_size=16).next_to(output_layer[max_index], RIGHT)
        self.play(Write(label))
        self.wait(1)

        # 7. Show pixel flipping in the original grid
        # The grid was moved to top left earlier
        target_pixel = grid[max_index]
        self.play(
            target_pixel.animate.set_fill(RED),
            Flash(target_pixel, color=RED)
        )
        
        self.wait(2)

        # Final Cleanup
        self.play(
            FadeOut(nn_group), 
            FadeOut(connections1), 
            FadeOut(connections2), 
            FadeOut(flattened_vector), 
            FadeOut(label), 
            FadeOut(highlight_circle)
        )
        self.play(grid.animate.scale(2).center())
        self.wait(1)