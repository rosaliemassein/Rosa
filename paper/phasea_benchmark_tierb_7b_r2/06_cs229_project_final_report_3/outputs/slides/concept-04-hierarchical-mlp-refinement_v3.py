from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Image and CLIP Block
        # Placeholder for image if file is missing
        try:
            image_mob = ImageMobject("img-8.jpeg").scale(1.5).to_edge(UP, buff=0.5)
        except:
            image_mob = VGroup(
                Rectangle(height=2, width=3, color=BLUE),
                Text("Input Image", font_size=24)
            ).to_edge(UP, buff=0.5)

        clip_block = VGroup(
            Rectangle(width=2, height=0.8, color=WHITE),
            Text("CLIP", font_size=24)
        ).next_to(image_mob, DOWN, buff=0.4)

        arrow_to_clip = Arrow(image_mob.get_bottom(), clip_block.get_top(), buff=0.1)

        self.play(FadeIn(image_mob))
        self.play(Create(arrow_to_clip), Create(clip_block))

        # 2. MLP Structure (Hierarchical Refinement)
        mlp_label = Text("Country-Specific MLP", font_size=20).next_to(clip_block, DOWN, buff=0.5)
        
        layers_config = [3, 4, 2]
        mlp_layers = VGroup()
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup(*[Circle(radius=0.12, color=BLUE, fill_opacity=0.6) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.15)
            layer.shift(RIGHT * i * 1.2)
            mlp_layers.add(layer)
        
        mlp_layers.center().shift(DOWN * 1.5 + LEFT * 2)
        mlp_label.next_to(mlp_layers, UP, buff=0.2)

        connections = VGroup()
        for i in range(len(layers_config) - 1):
            for node_start in mlp_layers[i]:
                for node_end in mlp_layers[i+1]:
                    line = Line(node_start.get_right(), node_end.get_left(), stroke_width=1, stroke_opacity=0.4)
                    connections.add(line)

        arrow_to_mlp = Arrow(clip_block.get_bottom(), mlp_label.get_top(), buff=0.1)

        self.play(
            Create(arrow_to_mlp),
            Write(mlp_label),
            Create(mlp_layers),
            Create(connections)
        )

        # 3. Animate signals through MLP
        signals = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in range(3)])
        for i, dot in enumerate(signals):
            dot.move_to(mlp_layers[0][i].get_center())

        self.play(FadeIn(signals))
        for i in range(len(layers_config) - 1):
            self.play(
                *[signals[j].animate.move_to(mlp_layers[i+1][j % layers_config[i+1]].get_center()) 
                  for j in range(len(signals))],
                run_time=0.8
            )
        self.play(FadeOut(signals))

        # 4. Map and Centroid Prediction
        map_box = Rectangle(width=3.5, height=2.2, color=GREEN, fill_opacity=0.1).to_edge(RIGHT, buff=0.8).shift(DOWN * 1.5)
        map_text = Text("Regional Map", font_size=16).next_to(map_box, UP, buff=0.1)
        
        # Centroids
        points = [(0.4, 0.3), (-0.6, -0.2), (1.0, -0.5), (-0.1, 0.15)]
        centroids = VGroup(*[Dot(map_box.get_center() + np.array([x, y, 0]), color=RED, radius=0.05) 
                           for x, y in points])
        
        target_centroid = centroids[3]
        arrow_to_map = Arrow(mlp_layers.get_right(), map_box.get_left(), buff=0.2)

        self.play(Create(map_box), Write(map_text), Create(centroids))
        self.play(Create(arrow_to_map))
        self.play(target_centroid.animate.scale(2).set_color(YELLOW))

        # 5. Coordinate Logic (Formula and Pin)
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=28).to_corner(UL)
        self.play(Write(formula))

        # Vector to Coordinate Transformation
        image_vector_tex = MathTex(r"\vec{x}_{img}", font_size=34).next_to(mlp_layers, LEFT, buff=0.4)
        coord_tex = MathTex(r"(lat, lon)", font_size=34).next_to(map_box, DOWN, buff=0.3)
        
        pin = VGroup(
            Line(ORIGIN, UP * 0.4, color=WHITE, stroke_width=2),
            Dot(UP * 0.4, color=RED, radius=0.08)
        ).move_to(target_centroid.get_center(), aligned_edge=DOWN)

        self.play(Write(image_vector_tex))
        self.play(
            ReplacementTransform(image_vector_tex.copy(), coord_tex),
            FadeIn(pin, shift=DOWN)
        )

        self.wait(2)