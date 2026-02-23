from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup Image and CLIP block
        try:
            image = ImageMobject("img-8.jpeg").scale(0.6)
        except:
            # Fallback if image doesn't exist
            image = Rectangle(height=2, width=3, color=GRAY).add(Text("Image", font_size=20))
        
        image.to_edge(LEFT, buff=1).shift(UP * 1.5)
        
        clip_label = MathTex(r"\text{CLIP}").next_to(image, RIGHT, buff=1)
        mlp_label = MathTex(r"\text{Country MLP}").move_to(clip_label.get_center())
        
        self.play(FadeIn(image), Write(clip_label))
        self.wait(1)
        
        # Transition CLIP to MLP label (ReplacementTransform instead of TransformMatchingTex)
        self.play(
            ReplacementTransform(clip_label, mlp_label),
            image.animate.scale(0.5).to_corner(UL)
        )
        self.play(mlp_label.animate.to_edge(UP, buff=0.5))

        # 2. Multi-Layer Perceptron (MLP)
        # Using 3 layers: 4 nodes, 5 nodes, 3 nodes
        layer_sizes = [4, 5, 3]
        layers = VGroup()
        for i, size in enumerate(layer_sizes):
            layer = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.2) for _ in range(size)])
            layer.arrange(DOWN, buff=0.25)
            layer.move_to(i * 1.8 * RIGHT + LEFT * 3)
            layers.add(layer)
        
        connections = VGroup()
        for i in range(len(layer_sizes) - 1):
            for n1 in layers[i]:
                for n2 in layers[i+1]:
                    line = Line(n1.get_right(), n2.get_left(), stroke_width=1, stroke_opacity=0.3)
                    connections.add(line)
        
        mlp_group = VGroup(connections, layers).shift(DOWN * 0.5)
        self.play(Create(mlp_group))

        # Animate signals flowing
        for i in range(len(layer_sizes) - 1):
            self.play(
                *[Flash(node, color=YELLOW, flash_radius=0.2, run_time=0.4) for node in layers[i]],
                lag_ratio=0.1
            )
        
        # 3. Map and Prediction
        map_area = RoundedRectangle(corner_radius=0.1, height=3.5, width=4.5, color=GRAY_A)
        map_area.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        map_title = Text("Local Clusters", font_size=20).next_to(map_area, UP)
        
        # Random centroids for the nation
        centroids = VGroup(*[
            Dot(map_area.get_center() + np.array([x, y, 0]), color=RED) 
            for x, y in [(0.7, 0.5), (-1.2, -0.4), (0.3, -1.0), (-0.5, 0.9)]
        ])
        target_centroid = centroids[1]
        
        self.play(Create(map_area), Write(map_title), Create(centroids))
        
        # MLP output pointing to centroid
        prediction_arrow = Arrow(layers[-1].get_right(), target_centroid.get_center(), color=YELLOW)
        self.play(GrowArrow(prediction_arrow))
        
        # GPS Pin Drop
        pin = VGroup(
            Dot(target_centroid.get_center(), color=YELLOW, radius=0.08),
            Triangle(color=YELLOW, fill_opacity=1).scale(0.12).rotate(180*DEGREES).move_to(target_centroid.get_center() + UP*0.15)
        )
        self.play(FadeIn(pin, shift=DOWN))

        # 4. Formula and Text Transition
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}").to_corner(UR, buff=0.5)
        self.play(Write(formula))
        
        # Transition from vector to coordinate
        vector_tex = MathTex(r"\vec{x}^{(i)}").next_to(layers[0], LEFT, buff=0.5)
        coord_tex = MathTex(r"(\text{lat, lon})").next_to(pin, UP, buff=0.3)
        
        self.play(Write(vector_tex))
        self.wait(1)
        # Using ReplacementTransform as a safe alternative to TransformMatchingTex
        self.play(ReplacementTransform(vector_tex, coord_tex))
        
        self.wait(2)