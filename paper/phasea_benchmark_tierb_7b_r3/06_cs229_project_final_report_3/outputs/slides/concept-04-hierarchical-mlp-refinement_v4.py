from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup Image and CLIP Block
        image_placeholder = RoundedRectangle(corner_radius=0.1, height=2, width=3, color=WHITE)
        image_label = Text("Image Input", font_size=24).move_to(image_placeholder.get_center())
        image_group = VGroup(image_placeholder, image_label).to_edge(UP).shift(LEFT * 4)

        clip_box = Rectangle(width=2, height=1, color=BLUE)
        clip_label = Text("CLIP", font_size=30).move_to(clip_box.get_center())
        clip_group = VGroup(clip_box, clip_label).next_to(image_group, RIGHT, buff=1.5)

        arrow_to_clip = Arrow(image_group.get_right(), clip_group.get_left(), buff=0.1)

        # 2. Setup Country MLP
        mlp_title = Text("Country MLP", font_size=24, color=YELLOW).next_to(clip_group, DOWN, buff=0.5)
        
        # Creating a 3-layer MLP
        layers = [3, 4, 3]
        mlp_nodes = VGroup()
        for i, num_nodes in enumerate(layers):
            layer = VGroup(*[Circle(radius=0.15, color=WHITE, fill_opacity=1) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.2)
            layer.shift(RIGHT * i * 1.5)
            mlp_nodes.add(layer)
        
        mlp_nodes.move_to(DOWN * 0.5 + LEFT * 1.5)
        
        connections = VGroup()
        for i in range(len(layers) - 1):
            for node1 in mlp_nodes[i]:
                for node2 in mlp_nodes[i+1]:
                    line = Line(node1.get_center(), node2.get_center(), stroke_width=1, stroke_opacity=0.5)
                    connections.add(line)

        mlp_group = VGroup(connections, mlp_nodes)
        arrow_to_mlp = Arrow(clip_group.get_bottom(), mlp_title.get_top(), buff=0.1)

        # 3. Setup Map and Centroids
        map_rect = Rectangle(width=4, height=3, color=GREEN, fill_opacity=0.2).to_edge(DR, buff=0.5)
        map_label = Text("Local Region", font_size=20).next_to(map_rect, UP, buff=0.1)
        
        # Sample centroid positions relative to map center
        raw_coords = [[-1, 0.5], [0.8, -0.6], [0.2, 0.7], [-0.5, -0.8]]
        centroids = VGroup(*[Dot(map_rect.get_center() + np.array([c[0], c[1], 0]), color=GRAY) 
                           for c in raw_coords])
        
        target_pos = map_rect.get_center() + np.array([0.5, 0.2, 0])
        target_centroid = Dot(target_pos, color=RED)
        
        gps_pin = VGroup(
            Triangle(color=RED, fill_opacity=1).scale(0.1).rotate(PI),
            Dot(radius=0.05, color=WHITE)
        ).move_to(target_pos + UP * 0.2)

        # 4. Formula
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=30).to_edge(DL, buff=0.5)

        # 5. Coordinate Labels
        image_vector_tex = MathTex(r"\text{Image Vector}").next_to(mlp_nodes[0], LEFT, buff=0.3).scale(0.7)
        final_coord_tex = MathTex(r"(lat, lon)").next_to(gps_pin, RIGHT, buff=0.2).scale(0.8)

        # --- Execution ---

        # Phase 1: CLIP Logic
        self.play(FadeIn(image_group))
        self.play(Create(arrow_to_clip), Create(clip_group))
        self.wait(0.5)

        # Phase 2: MLP Transition
        self.play(Create(arrow_to_mlp), Write(mlp_title))
        self.play(Create(mlp_nodes), Create(connections), Write(image_vector_tex))
        self.wait(0.5)

        # Phase 3: Neural signals
        for i in range(len(layers) - 1):
            passing_lines = VGroup()
            for n1 in mlp_nodes[i]:
                for n2 in mlp_nodes[i+1]:
                    passing_lines.add(Line(n1.get_center(), n2.get_center(), color=YELLOW, stroke_width=2))
            self.play(Create(passing_lines), run_time=0.4)
            self.play(FadeOut(passing_lines), run_time=0.4)

        # Phase 4: Output to Map
        self.play(Create(map_rect), Write(map_label), Create(centroids))
        self.play(Write(formula))
        
        arrow_to_map = Arrow(mlp_nodes[2].get_right(), target_centroid.get_center(), buff=0.1, color=YELLOW)
        self.play(Create(arrow_to_map))
        self.play(target_centroid.animate.scale(1.5).set_color(ORANGE))
        
        # Phase 5: Result
        self.play(FadeIn(gps_pin, shift=DOWN))
        self.play(ReplacementTransform(image_vector_tex.copy(), final_coord_tex))
        
        self.wait(2)