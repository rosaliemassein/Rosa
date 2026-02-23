from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Header: Image -> CLIP -> Country MLP
        image_box = Rectangle(width=2, height=1.5, color=WHITE).shift(UP * 3 + LEFT * 4)
        image_text = Text("Image", font_size=24).move_to(image_box)
        image_group = VGroup(image_box, image_text)

        clip_box = Rectangle(width=2, height=1, color=BLUE).next_to(image_box, RIGHT, buff=1)
        clip_text = Text("CLIP", font_size=24).move_to(clip_box)
        clip_group = VGroup(clip_box, clip_text)

        country_mlp_box = Rectangle(width=3, height=1, color=GREEN).next_to(clip_box, RIGHT, buff=1)
        country_mlp_text = Text("Country MLP", font_size=24).move_to(country_mlp_box)
        country_mlp_group = VGroup(country_mlp_box, country_mlp_text)

        arrow1 = Arrow(image_box.get_right(), clip_box.get_left(), buff=0.1)
        arrow2 = Arrow(clip_box.get_right(), country_mlp_box.get_left(), buff=0.1)

        # 2. Detailed MLP (3 layers)
        def create_layer(n_nodes, x_pos, color=WHITE):
            layer = VGroup(*[Dot(radius=0.1, color=color) for _ in range(n_nodes)])
            layer.arrange(DOWN, buff=0.3).move_to(RIGHT * x_pos + DOWN * 0.5)
            return layer

        input_layer = create_layer(4, -2, color=BLUE)
        hidden_layer1 = create_layer(6, 0, color=WHITE)
        hidden_layer2 = create_layer(6, 2, color=WHITE)
        output_layer = create_layer(4, 4, color=GREEN)

        layers = VGroup(input_layer, hidden_layer1, hidden_layer2, output_layer)

        connections = VGroup()
        for i in range(len(layers) - 1):
            for node_a in layers[i]:
                for node_b in layers[i+1]:
                    line = Line(node_a.get_center(), node_b.get_center(), stroke_width=1, stroke_opacity=0.3)
                    connections.add(line)

        mlp_label = Text("Local Region MLP", font_size=20).next_to(layers, UP)
        relu_labels = VGroup(
            Text("ReLU", font_size=14, color=YELLOW).next_to(hidden_layer1, DOWN),
            Text("ReLU", font_size=14, color=YELLOW).next_to(hidden_layer2, DOWN)
        )

        # 3. Formula
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=30).to_corner(UR)

        # 4. Map and Centroid
        map_rect = Rectangle(width=5, height=3, color=GRAY_D).to_edge(DOWN).shift(RIGHT * 2)
        map_label = Text("Local Cluster Map", font_size=18).next_to(map_rect, UP, buff=0.1)
        
        centroids = VGroup(*[Dot(map_rect.get_center() + np.array([np.random.uniform(-1.5, 1.5), np.random.uniform(-0.8, 0.8), 0]), color=GRAY) for _ in range(5)])
        target_centroid = centroids[2].copy().set_color(RED).scale(1.5)
        
        pin = Triangle(color=RED, fill_opacity=1).scale(0.15).rotate(PI)
        pin.move_to(target_centroid.get_center() + UP * 0.3)

        # 5. Coordinate Transition
        vector_text = MathTex(r"\vec{x}^{(i)}", font_size=36).move_to(output_layer.get_right() + RIGHT * 0.5)
        coords_text = MathTex(r"(40.71, -74.00)", font_size=36).next_to(pin, RIGHT)

        # Animations
        self.play(Create(image_group), Create(clip_group), Create(arrow1))
        self.play(Create(arrow2), Create(country_mlp_group))
        self.wait(1)

        self.play(FadeIn(layers), FadeIn(connections), Write(mlp_label), FadeIn(relu_labels))
        self.play(Write(formula))

        # Animate signal through MLP using simple flash-like indicators
        for i in range(len(layers) - 1):
            pulse_conns = VGroup(*[Line(n1.get_center(), n2.get_center(), color=YELLOW, stroke_width=2) 
                                   for n1 in layers[i] for n2 in layers[i+1]])
            self.play(FadeIn(pulse_conns, run_time=0.2), FadeOut(pulse_conns, run_time=0.2))

        self.play(Write(vector_text))
        self.wait(1)

        self.play(FadeIn(map_rect), FadeIn(map_label), FadeIn(centroids))
        
        # Point to centroid
        output_arrow = Arrow(vector_text.get_right(), target_centroid.get_center(), color=YELLOW, buff=0.1)
        self.play(Create(output_arrow))
        self.play(target_centroid.animate.set_color(YELLOW).scale(1.2))
        
        # Drop pin
        self.play(pin.animate.shift(DOWN * 0.1), FadeIn(pin))
        
        # Transform vector to coordinate
        self.play(ReplacementTransform(vector_text, coords_text))
        self.wait(2)

        # Final summary text
        summary = Text("Hierarchical Refinement: Country -> Cluster Centroid", font_size=24).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(3)