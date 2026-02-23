from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Image and CLIP block
        # ImageMobject for the input
        try:
            image = ImageMobject("img-8.jpeg").scale(0.5).to_edge(UP + LEFT)
        except:
            image = Square(side_length=2, color=BLUE).to_edge(UP + LEFT)
            image.add(Text("Image", font_size=20).move_to(image.get_center()))
            
        clip_block = VGroup(
            Rectangle(width=1.8, height=0.8, color=WHITE),
            Text("CLIP", font_size=24)
        ).next_to(image, RIGHT, buff=0.8)
        
        clip_arrow = Arrow(image.get_right(), clip_block.get_left())

        # 2. Country MLP (3-layer neural network)
        # Defining layers
        layers_config = [4, 3, 2]
        nodes = VGroup()
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup(*[
                Circle(radius=0.1, color=WHITE, fill_opacity=1) 
                for _ in range(num_nodes)
            ]).arrange(DOWN, buff=0.2)
            layer.shift(RIGHT * i * 1.2)
            nodes.add(layer)
        
        nodes.center().shift(DOWN * 0.5)
        
        edges = VGroup()
        for i in range(len(nodes) - 1):
            for n1 in nodes[i]:
                for n2 in nodes[i+1]:
                    edges.add(Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.4))

        mlp_group = VGroup(edges, nodes)
        mlp_label = Text("Country MLP", font_size=20).next_to(mlp_group, UP)
        
        clip_to_mlp_arrow = Arrow(clip_block.get_bottom(), mlp_label.get_top())

        # 3. Map and Centroids
        map_rect = Rectangle(width=3.5, height=2.5, color=GREY).to_edge(DOWN + RIGHT)
        map_label = Text("Local Region Clusters", font_size=18).next_to(map_rect, UP)
        
        # Centroids
        center_map = map_rect.get_center()
        centroid_positions = [
            center_map + np.array([-0.8, 0.5, 0]),
            center_map + np.array([0.6, -0.4, 0]),
            center_map + np.array([-0.3, -0.7, 0]),
            center_map + np.array([0.4, 0.6, 0])
        ]
        centroids = VGroup(*[Dot(pos, color=YELLOW, radius=0.06) for pos in centroid_positions])
        target_centroid = centroids[1]

        # GPS Pin (Triangle + Dot)
        pin_head = Dot(color=RED, radius=0.1)
        pin_point = Triangle(color=RED, fill_opacity=1).scale(0.1).rotate(180 * DEGREES)
        pin = VGroup(pin_point, pin_head).arrange(UP, buff=0).move_to(target_centroid.get_center() + UP * 0.15)

        # 4. Formula and Text
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32).to_edge(UP).shift(RIGHT * 2)
        image_vector = MathTex(r"x^{(i)}", color=BLUE).next_to(image, DOWN)
        final_coord = MathTex(r"(\text{lat}, \text{lon})", color=GREEN).next_to(map_rect, LEFT)

        # ANIMATION SEQUENCE
        self.play(FadeIn(image), Write(image_vector))
        self.play(Create(clip_arrow), FadeIn(clip_block))
        self.wait(0.5)
        
        self.play(Create(clip_to_mlp_arrow))
        self.play(FadeIn(mlp_label), Create(mlp_group))
        self.play(Write(formula))
        
        # Signal flow animation
        for i in range(len(nodes)):
            self.play(nodes[i].animate.set_color(YELLOW), run_time=0.3)
            self.play(nodes[i].animate.set_color(WHITE), run_time=0.1)

        self.play(FadeIn(map_rect), FadeIn(map_label), Create(centroids))
        
        # Flow to centroid
        mlp_to_map_arrow = Arrow(nodes[-1].get_right(), target_centroid.get_center(), color=YELLOW)
        self.play(Create(mlp_to_map_arrow))
        
        # Drop GPS Pin
        self.play(
            pin.animate.move_to(target_centroid.get_center()),
            target_centroid.animate.set_color(RED).scale(1.5),
            run_time=1
        )
        
        # Transition from image vector to coordinates
        # Using ReplacementTransform since TransformMatchingTex failed in original log
        self.play(ReplacementTransform(image_vector.copy(), final_coord))
        
        self.wait(3)