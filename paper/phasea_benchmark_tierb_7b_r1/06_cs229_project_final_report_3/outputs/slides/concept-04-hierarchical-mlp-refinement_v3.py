import numpy as np
from manim import *

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup Image and CLIP Block
        try:
            image = ImageMobject("img-8.jpeg").scale(0.6)
        except:
            image = Rectangle(height=2, width=3, color=GRAY).add(Text("Image", font_size=24))
        
        image.to_edge(UP, buff=0.5).to_edge(LEFT, buff=1)
        
        clip_rect = Rectangle(height=1.2, width=2, color=BLUE)
        clip_label = Text("CLIP", font_size=28).move_to(clip_rect.get_center())
        clip_group = VGroup(clip_rect, clip_label).next_to(image, RIGHT, buff=1.5)

        # 2. Setup Country MLP (Hierarchical Structure)
        mlp_title = Text("Country-Specific MLP", font_size=24, color=YELLOW)
        
        # Create a 3-layer MLP visualization
        layers = [3, 4, 2]
        mlp_nodes = VGroup()
        for i, num_nodes in enumerate(layers):
            layer = VGroup(*[Circle(radius=0.15, color=WHITE, fill_opacity=1) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.2)
            layer.shift(RIGHT * i * 1.5)
            mlp_nodes.add(layer)
        
        mlp_nodes.center().shift(DOWN * 0.5)
        mlp_title.next_to(mlp_nodes, UP, buff=0.3)
        
        # Connections
        connections = VGroup()
        for i in range(len(layers) - 1):
            for node1 in mlp_nodes[i]:
                for node2 in mlp_nodes[i+1]:
                    line = Line(node1.get_right(), node2.get_left(), stroke_width=1, stroke_opacity=0.5)
                    connections.add(line)

        mlp_full = VGroup(mlp_title, mlp_nodes, connections)

        # 3. Formula and Map/Centroids
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32).to_edge(RIGHT, buff=1).shift(UP * 2)
        
        # Map representation
        map_rect = Rectangle(height=2.5, width=4, color=GREEN, fill_opacity=0.2).to_edge(DOWN).to_edge(RIGHT)
        map_label = Text("Local Region", font_size=20).next_to(map_rect, UP, buff=0.1)
        
        centroids = VGroup(*[Dot(point=map_rect.get_center() + np.array([x, y, 0]), color=RED) 
                           for x, y in [(0.5, 0.4, 0), (-0.8, -0.2, 0), (1.1, -0.6, 0)]])
        centroid_labels = VGroup(*[Text(f"mu_{i+1}", font_size=14).next_to(centroids[i], DOWN, buff=0.1) for i in range(3)])

        # GPS Pin
        pin = VGroup(
            Line(ORIGIN, UP*0.3, color=YELLOW),
            Dot(color=YELLOW).scale(1.5)
        ).move_to(centroids[1].get_center() + UP*0.15)

        # --- ANIMATION SEQUENCE ---
        
        self.play(FadeIn(image))
        self.play(Create(clip_group))
        
        arrow_to_clip = Arrow(image.get_right(), clip_rect.get_left())
        self.play(GrowArrow(arrow_to_clip))
        self.wait(1)

        # Transition to MLP
        self.play(
            FadeOut(clip_group),
            FadeOut(image),
            FadeOut(arrow_to_clip),
            FadeIn(mlp_full)
        )
        self.play(Write(formula))
        self.wait(1)

        # Signal Flow through MLP
        for i in range(len(layers) - 1):
            # Identifying lines between current layer and next layer
            layer_start_x = mlp_nodes[i][0].get_right()[0]
            layer_end_x = mlp_nodes[i+1][0].get_left()[0]
            
            connecting_lines = VGroup(*[
                line for line in connections 
                if np.isclose(line.get_start()[0], layer_start_x, atol=0.1) 
                and np.isclose(line.get_end()[0], layer_end_x, atol=0.1)
            ])
            
            self.play(
                mlp_nodes[i].animate.set_color(YELLOW),
                connecting_lines.animate.set_stroke(color=YELLOW, opacity=1),
                run_time=0.4
            )
            self.play(
                mlp_nodes[i].animate.set_color(WHITE),
                connecting_lines.animate.set_stroke(color=WHITE, opacity=0.5),
                run_time=0.2
            )
        self.play(mlp_nodes[-1].animate.set_color(YELLOW))

        # Show Map and Prediction
        self.play(Create(map_rect), Write(map_label))
        self.play(Create(centroids), Write(centroid_labels))
        
        # Connect MLP output to specific centroid
        prediction_arrow = Arrow(mlp_nodes[-1].get_right(), centroids[1].get_center(), color=YELLOW)
        self.play(GrowArrow(prediction_arrow))
        
        # Drop GPS Pin
        self.play(pin.animate.shift(DOWN*0.15).set_opacity(1))
        self.play(Indicate(centroids[1]))
        
        # Final Transformation (Transition from image vector idea to coordinates)
        vec_label = MathTex(r"\vec{x}^{(i)}", font_size=42).move_to(mlp_nodes.get_center())
        coord_label = MathTex(r"(\phi, \lambda)", font_size=42).move_to(pin.get_center() + UP * 0.8)
        
        self.play(FadeIn(vec_label))
        self.play(ReplacementTransform(vec_label, coord_label))
        
        self.wait(2)