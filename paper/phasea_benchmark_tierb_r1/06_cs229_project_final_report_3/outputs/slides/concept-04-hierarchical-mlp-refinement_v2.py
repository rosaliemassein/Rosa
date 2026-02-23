from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup Image and Flowchart
        # Using a Square as placeholder for the Image if path is invalid
        image_box = Square(side_length=2, color=WHITE).to_edge(UP).shift(LEFT * 3)
        image_label = Text("Image", font_size=24).next_to(image_box, UP)
        image_group = VGroup(image_box, image_label)

        clip_block = VGroup(
            Rectangle(height=1, width=2, color=BLUE),
            Text("CLIP", font_size=24)
        ).next_to(image_box, RIGHT, buff=1)
        
        mlp_block = VGroup(
            Rectangle(height=1, width=3, color=GREEN),
            Text("Country MLP", font_size=24)
        ).next_to(clip_block, RIGHT, buff=1)

        arrow1 = Arrow(image_box.get_right(), clip_block.get_left())
        arrow2 = Arrow(clip_block.get_right(), mlp_block.get_left())

        # 2. Multi-Layer Perceptron (MLP) - 3 Layers
        layer_counts = [4, 6, 3]
        layers = VGroup()
        for count in layer_counts:
            layer = VGroup(*[Circle(radius=0.1, color=WHITE, fill_opacity=1) for _ in range(count)])
            layer.arrange(DOWN, buff=0.2)
            layers.add(layer)
        layers.arrange(RIGHT, buff=1.5).next_to(mlp_block, DOWN, buff=1)

        # Connect MLP layers
        connections = VGroup()
        for i in range(len(layers) - 1):
            for node_a in layers[i]:
                for node_b in layers[i+1]:
                    connections.add(Line(node_a.get_center(), node_b.get_center(), stroke_width=1, stroke_opacity=0.2))

        # Labels for layers
        in_label = Text("Input Vector", font_size=20).next_to(layers[0], DOWN)
        out_label = Text("Output (Centroids)", font_size=20).next_to(layers[-1], DOWN)

        # 3. Map and Centroids
        map_rect = Rectangle(height=3, width=5, color=GREY_B).to_corner(DR)
        map_text = Text("Map (Local Region)", font_size=20).move_to(map_rect.get_top() + DOWN * 0.3)
        
        centroids = VGroup(*[Dot(color=RED) for _ in range(5)])
        # Position centroids within map
        centroid_positions = [
            [0.5, 0.5, 0], [-1, 0.8, 0], [1.2, -0.5, 0], [-0.8, -0.6, 0], [0, -0.2, 0]
        ]
        for dot, pos in zip(centroids, centroid_positions):
            dot.move_to(map_rect.get_center() + pos)

        # Final coordinate (lat, lon)
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32).to_edge(LEFT).shift(DOWN * 1)
        lat_lon = MathTex(r"(\hat{lat}, \hat{lon})", color=YELLOW).to_edge(LEFT).shift(DOWN * 2)
        pin = Dot(color=BLUE, radius=0.15).set_stroke(WHITE, 2)

        # --- Animations ---

        # Phase 1: Pipeline flow
        self.play(FadeIn(image_group))
        self.play(GrowArrow(arrow1), Create(clip_block))
        self.play(GrowArrow(arrow2), Create(mlp_block))
        self.wait(0.5)

        # Phase 2: MLP Refinement
        self.play(Create(layers), Create(connections), Write(in_label), Write(out_label))
        
        # Animate signals flowing through layers
        for _ in range(2):
            self.play(connections.animate.set_stroke(color=YELLOW, opacity=0.8), run_time=0.4)
            self.play(connections.animate.set_stroke(color=WHITE, opacity=0.2), run_time=0.4)
        
        # Phase 3: Centroid selection
        self.play(FadeIn(map_rect), FadeIn(map_text), Create(centroids))
        self.play(Write(formula))
        
        # Highlight specific centroid (prediction)
        chosen_centroid = centroids[2]
        self.play(Indicate(chosen_centroid, color=YELLOW, scale_factor=2))
        
        # Pin dropping
        pin.move_to(chosen_centroid.get_center() + UP * 0.5)
        self.play(pin.animate.move_to(chosen_centroid.get_center()), run_time=0.8, rate_func=bounce)
        
        # Transition to coordinates
        self.play(ReplacementTransform(out_label.copy(), lat_lon))
        
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(image_group), FadeOut(clip_block), FadeOut(mlp_block),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(layers), FadeOut(connections),
            FadeOut(map_rect), FadeOut(map_text), FadeOut(centroids),
            FadeOut(formula), FadeOut(lat_lon), FadeOut(pin), FadeOut(in_label), FadeOut(out_label)
        )
        self.wait(1)

def bounce(t):
    # Custom bounce effect for the pin drop
    return t * t * (3.0 - 2.0 * t) if t < 0.5 else 1.0 - (1.0 - t) * (1.0 - t) * 4.0