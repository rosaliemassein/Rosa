import numpy as np
from manim import *

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Input Image representation
        input_image = VGroup(
            Rectangle(height=2, width=3, color=GRAY),
            Text("Input Image", font_size=20)
        ).to_edge(LEFT, buff=0.5)
        
        # 2. CLIP Block
        clip_block = VGroup(
            Rectangle(width=2, height=1.2, color=BLUE),
            Text("CLIP", color=BLUE).scale(0.8)
        ).next_to(input_image, RIGHT, buff=1)
        
        # 3. Country MLP selection
        country_mlp_block = VGroup(
            Rectangle(width=2.5, height=1.2, color=RED),
            Text("Country-Specific\nMLP", color=RED, font_size=24)
        ).next_to(clip_block, RIGHT, buff=1)
        
        # Connections
        arrow1 = Arrow(input_image.get_right(), clip_block.get_left(), buff=0.1)
        arrow2 = Arrow(clip_block.get_right(), country_mlp_block.get_left(), buff=0.1)
        
        self.play(FadeIn(input_image))
        self.play(Create(arrow1), Create(clip_block))
        self.wait(0.5)
        self.play(Create(arrow2), Create(country_mlp_block))
        
        # 4. Scale and move to make room for the MLP details
        top_group = VGroup(input_image, clip_block, country_mlp_block, arrow1, arrow2)
        self.play(top_group.animate.scale(0.7).to_edge(UP))
        
        # 5. Hierarchical MLP (3-layer neural network)
        layers_config = [4, 5, 3]
        mlp_layers = VGroup()
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup(*[Circle(radius=0.15, color=WHITE, fill_opacity=1) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.3)
            layer.shift(i * RIGHT * 2)
            mlp_layers.add(layer)
        
        mlp_layers.move_to(DOWN * 0.5)
        
        connections = VGroup()
        for i in range(len(layers_config) - 1):
            for node_in in mlp_layers[i]:
                for node_out in mlp_layers[i+1]:
                    line = Line(node_in.get_center(), node_out.get_center(), stroke_width=1, stroke_opacity=0.3, color=GRAY)
                    connections.add(line)
                    
        mlp_label = Text("Local Region MLP (ReLU)", font_size=24, color=YELLOW).next_to(mlp_layers, UP)
        
        self.play(Create(mlp_layers), Create(connections), Write(mlp_label))
        
        # 6. Animate signals flowing through the MLP layers
        for i in range(len(layers_config) - 1):
            flashes = []
            for node_in in mlp_layers[i]:
                for node_out in mlp_layers[i+1]:
                    l = Line(node_in.get_center(), node_out.get_center(), color=YELLOW, stroke_width=3)
                    flashes.append(Create(l, run_time=0.4))
            self.play(LaggedStart(*flashes, lag_ratio=0.01))
            self.play(FadeOut(VGroup(*[f.mobject for f in flashes])))

        # 7. Map and Final Prediction
        # Placeholder for Map with centroids
        map_rect = Rectangle(width=4, height=2.5, color=GREEN, fill_opacity=0.2).to_edge(DR)
        map_label = Text("Local Clusters", font_size=20).next_to(map_rect, UP)
        
        # Generate random centroids within the map rectangle
        centroids = VGroup()
        for _ in range(5):
            dot = Dot(color=WHITE).move_to(
                map_rect.get_center() + np.array([
                    np.random.uniform(-1.5, 1.5),
                    np.random.uniform(-0.8, 0.8),
                    0
                ])
            )
            centroids.add(dot)
            
        target_centroid = centroids[2] # Pick one as the prediction
        
        self.play(FadeIn(map_rect), FadeIn(map_label), Create(centroids))
        
        # 8. Final Coordinate Result as a GPS 'pin'
        pin = Triangle(color=RED, fill_opacity=1).scale(0.15).rotate(180*DEGREES)
        pin.move_to(target_centroid.get_center() + UP * 0.3)
        
        # 9. Transition: Image Vector (placeholder) to Coordinates
        img_vec = MathTex(r"\vec{x}^{(i)}").move_to(mlp_layers[0].get_left() + LEFT*0.5)
        final_coords = MathTex(r"(lat, lon)", color=RED).next_to(pin, RIGHT, buff=0.2)
        
        self.play(
            target_centroid.animate.set_color(RED).scale(1.5),
            FadeIn(pin),
            Write(final_coords)
        )
        
        # 10. Formula display
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}").to_edge(DL, buff=1)
        self.play(Write(formula))
        
        self.wait(2)