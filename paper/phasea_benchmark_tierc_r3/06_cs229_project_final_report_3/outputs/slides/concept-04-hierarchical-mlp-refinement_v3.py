from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup the UI/Flowchart Elements
        # Image
        try:
            image = ImageMobject("img-8.jpeg").scale(1.2)
        except:
            image = Rectangle(height=2, width=3, color=GRAY).add(Text("Image", font_size=20))
        image.to_edge(UP).to_edge(LEFT, buff=1)

        # Vector Label
        image_vector = MathTex(r"\vec{x}", font_size=36).next_to(image, DOWN)

        # CLIP Block
        clip_box = VGroup(
            Rectangle(height=0.8, width=1.5, color=YELLOW),
            Text("CLIP", font_size=24, color=YELLOW)
        ).next_to(image, RIGHT, buff=1.2)

        # Country MLP Block
        country_mlp = VGroup(
            Rectangle(height=0.8, width=2.5, color=GREEN),
            Text("Country MLP", font_size=24, color=GREEN)
        ).next_to(clip_box, DOWN, buff=1.2)

        # Multi-Layer Perceptron (Refinement Stage)
        def create_mlp():
            layers = [3, 4, 3]
            nodes = VGroup()
            for i, count in enumerate(layers):
                layer_nodes = VGroup(*[Dot(radius=0.08, color=BLUE) for _ in range(count)])
                layer_nodes.arrange(DOWN, buff=0.2)
                layer_nodes.shift(RIGHT * i * 0.7)
                nodes.add(layer_nodes)
            
            edges = VGroup()
            for i in range(len(nodes) - 1):
                for n1 in nodes[i]:
                    for n2 in nodes[i+1]:
                        edges.add(Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.3, color=WHITE))
            return VGroup(edges, nodes)

        refinement_mlp = create_mlp().next_to(country_mlp, RIGHT, buff=1.2)
        mlp_label = Text("Refinement MLP", font_size=20, color=BLUE).next_to(refinement_mlp, UP, buff=0.2)

        # Map and GPS Output
        map_rect = Rectangle(height=2.5, width=3.5, color=WHITE).to_edge(DOWN).to_edge(RIGHT, buff=1)
        map_label = Text("Local Region Map", font_size=20).next_to(map_rect, UP)
        
        # K-means centroids on map
        centroids = VGroup(*[
            Dot(map_rect.get_center() + np.array([x, y, 0]), radius=0.06, color=GRAY_A)
            for x, y in [[-0.8, 0.4], [0.6, 0.7], [-0.4, -0.6], [0.9, -0.3], [0, 0]]
        ])
        target_centroid = centroids[4]
        
        # GPS Pin
        pin = VGroup(
            Line(ORIGIN, UP*0.4, color=RED, stroke_width=4),
            Dot(UP*0.4, color=RED, radius=0.12)
        ).move_to(target_centroid.get_center(), aligned_edge=DOWN)

        # Final coordinate label
        coord_result = MathTex(r"(\text{lat}, \text{lon})", font_size=36, color=RED).next_to(map_rect, LEFT, buff=0.5)

        # Formula
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32).to_edge(DOWN).to_edge(LEFT, buff=1)

        # 2. Animation Pipeline
        self.play(FadeIn(image), Write(image_vector))
        self.wait(0.5)

        # CLIP Processing
        arrow1 = Arrow(image.get_right(), clip_box.get_left(), buff=0.1)
        self.play(GrowArrow(arrow1), Create(clip_box))
        
        # To Country MLP
        arrow2 = Arrow(clip_box.get_bottom(), country_mlp.get_top(), buff=0.1)
        self.play(GrowArrow(arrow2), Create(country_mlp))
        
        # To Refinement MLP
        arrow3 = Arrow(country_mlp.get_right(), refinement_mlp.get_left(), buff=0.1)
        self.play(GrowArrow(arrow3), Create(refinement_mlp), Write(mlp_label))
        
        # Animate signal through MLP
        for layer in refinement_mlp[1]:
            self.play(layer.animate.set_color(YELLOW), run_time=0.15)
            self.play(layer.animate.set_color(BLUE), run_time=0.15)

        # Final prediction on map
        self.play(Create(map_rect), Create(centroids), Write(map_label))
        arrow4 = Arrow(refinement_mlp.get_right(), target_centroid.get_center(), buff=0.1)
        self.play(GrowArrow(arrow4))
        
        self.play(FadeIn(pin, shift=DOWN))
        self.play(Write(formula))

        # Coordinate transition
        # Using ReplacementTransform for stability between vector and coordinate text
        self.play(ReplacementTransform(image_vector.copy(), coord_result))
        
        self.wait(3)