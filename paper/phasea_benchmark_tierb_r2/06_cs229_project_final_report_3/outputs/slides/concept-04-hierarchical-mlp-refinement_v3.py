import numpy as np
from manim import *

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Flowchart Elements
        # Image Placeholder
        image_box = Rectangle(height=2, width=2.5, color=WHITE).shift(UP * 2.5 + LEFT * 4)
        image_label = Text("Input Image", font_size=24).move_to(image_box)
        self.play(Create(image_box), Write(image_label))

        # CLIP Block
        clip_box = Rectangle(height=1, width=2, color=BLUE).next_to(image_box, RIGHT, buff=1)
        clip_text = Text("CLIP", font_size=24).move_to(clip_box)
        arrow1 = Arrow(image_box.get_right(), clip_box.get_left())
        self.play(GrowArrow(arrow1), Create(clip_box), Write(clip_text))

        # Country MLP Block
        mlp_block_rect = Rectangle(height=1, width=2.5, color=GREEN).next_to(clip_box, RIGHT, buff=1)
        mlp_block_text = Text("Country MLP", font_size=24).move_to(mlp_block_rect)
        arrow2 = Arrow(clip_box.get_right(), mlp_block_rect.get_left())
        self.play(GrowArrow(arrow2), Create(mlp_block_rect), Write(mlp_block_text))

        # 2. MLP Neural Network Representation
        layers_config = [3, 4, 2]
        neurons = VGroup()
        layer_groups = []
        
        for i, num_neurons in enumerate(layers_config):
            layer = VGroup(*[Circle(radius=0.15, color=WHITE, fill_opacity=1) for _ in range(num_neurons)])
            layer.arrange(DOWN, buff=0.3)
            layer.shift(RIGHT * i * 1.5 + DOWN * 1)
            layer_groups.append(layer)
            neurons.add(layer)
        
        neurons.center().shift(DOWN * 1)
        
        connections = VGroup()
        for i in range(len(layer_groups) - 1):
            for n1 in layer_groups[i]:
                for n2 in layer_groups[i+1]:
                    line = Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.4)
                    connections.add(line)
        
        self.play(Create(connections), Create(neurons))
        
        # Label layers
        l1_label = Text("Layer 1 (ReLU)", font_size=18).next_to(layer_groups[0], UP)
        l2_label = Text("Layer 2 (ReLU)", font_size=18).next_to(layer_groups[1], UP)
        l3_label = Text("Layer 3", font_size=18).next_to(layer_groups[2], UP)
        self.play(Write(l1_label), Write(l2_label), Write(l3_label))

        # 3. Formula
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32).to_edge(DOWN, buff=0.5)
        self.play(Write(formula))

        # 4. Signal Flow Animation
        for _ in range(2):
            pulses = VGroup()
            for neuron in layer_groups[0]:
                pulse = Dot(neuron.get_center(), color=YELLOW, radius=0.08)
                pulses.add(pulse)
            
            # Use indices to avoid zip/enumerate logic issues in simple animations
            self.play(
                pulses[0].animate.move_to(layer_groups[1][0].get_center()),
                pulses[1].animate.move_to(layer_groups[1][1].get_center()),
                pulses[2].animate.move_to(layer_groups[1][2].get_center()),
                run_time=0.6
            )
            self.play(
                pulses[0].animate.move_to(layer_groups[2][0].get_center()),
                pulses[1].animate.move_to(layer_groups[2][1].get_center()),
                pulses[2].animate.move_to(layer_groups[2][0].get_center()),
                run_time=0.6
            )
            self.play(FadeOut(pulses))

        # 5. Map and GPS Pin
        map_box = Rectangle(height=3, width=4, color=GRAY).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        map_text = Text("Local Cluster Map", font_size=20).next_to(map_box, UP)
        
        # Centroids
        coords = [(0.5, 0.4, 0), (-0.8, -0.2, 0), (0.2, -0.7, 0), (-0.3, 0.6, 0)]
        centroids = VGroup(*[Dot(map_box.get_center() + np.array(c), color=BLUE) for c in coords])
        
        self.play(Create(map_box), Write(map_text), Create(centroids))
        
        # Final prediction
        target_centroid = centroids[0]
        prediction_arrow = Arrow(layer_groups[-1].get_right(), target_centroid.get_left(), color=YELLOW)
        self.play(GrowArrow(prediction_arrow))
        
        # GPS Pin Drop
        pin = Dot(target_centroid.get_center(), color=RED).scale(1.5)
        self.play(FadeIn(pin))
        
        # 6. Final Coordinate Transformation
        image_vec_label = MathTex(r"\vec{x}_{img}", color=BLUE).next_to(image_box, UP)
        coord_label = MathTex(r"(lat, lon)", color=RED).next_to(pin, RIGHT, buff=0.2)
        
        self.play(Write(image_vec_label))
        self.wait(1)
        self.play(ReplacementTransform(image_vec_label.copy(), coord_label))

        self.wait(2)