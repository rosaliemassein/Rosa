from manim import *
import numpy as np

class HierarchicalMLPRefinement(Scene):
    def construct(self):
        # 1. Setup World Map and Centroids
        # Attempt to load the image, fallback to a rectangle if it fails
        try:
            world_map = ImageMobject("img-8.jpeg")
        except:
            world_map = Rectangle(width=6, height=4, color=GRAY).add(Text("Map", font_size=20))
            
        world_map.scale(0.6).to_edge(RIGHT, buff=0.5)
        
        # Create centroids on the map
        centroid_positions = [
            [-1, 0.5, 0], [0.5, -0.3, 0], [0.2, 0.8, 0], [-0.4, -0.7, 0], [0.8, 0.4, 0]
        ]
        city_centroids = VGroup(*[
            Dot(color=RED, radius=0.1).move_to(world_map.get_center() + np.array(pos))
            for pos in centroid_positions
        ])

        # 2. Pipeline Components (Flow Chart)
        image_label = Text("Image", font_size=24)
        clip_block = VGroup(
            RoundedRectangle(height=0.7, width=1.8, color=BLUE),
            Text("CLIP", font_size=24)
        )
        country_mlp_block = VGroup(
            RoundedRectangle(height=0.7, width=2.2, color=GREEN),
            Text("Country MLP", font_size=22)
        )

        # 3. MLP Structure (3 layers)
        layer_sizes = [4, 5, 3]
        mlp_layers = VGroup()
        for size in layer_sizes:
            layer = VGroup(*[Dot(radius=0.08, color=RED) for _ in range(size)])
            layer.arrange(DOWN, buff=0.15)
            mlp_layers.add(layer)
        mlp_layers.arrange(RIGHT, buff=0.7)
        
        # MLP Connections
        connections = VGroup()
        for i in range(len(mlp_layers)-1):
            for dot_in in mlp_layers[i]:
                for dot_out in mlp_layers[i+1]:
                    connections.add(Line(
                        dot_in.get_center(), 
                        dot_out.get_center(), 
                        stroke_width=0.5, 
                        stroke_opacity=0.3,
                        color=WHITE
                    ))
        
        mlp_full = VGroup(connections, mlp_layers)

        # 4. Assemble the Pipeline on the Left
        pipeline = VGroup(image_label, clip_block, country_mlp_block, mlp_full)
        pipeline.arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.5)

        # 5. Formula and Coordinate Label
        formula = MathTex(r"c^{(i)}:=\arg\min_{j}\|x^{(i)}-\mu_{j}\|^{2}", font_size=32)
        formula.to_edge(DOWN, buff=0.4)
        
        coord_tex = MathTex(r"(lat, lon)", font_size=24, color=YELLOW)
        coord_tex.next_to(mlp_layers, RIGHT, buff=0.3)

        # --- Animation Sequence ---
        
        # Show Map and Start Pipeline
        self.play(FadeIn(world_map), Create(city_centroids))
        self.play(Write(image_label))
        self.wait(0.5)

        # Pass through CLIP
        image_embedding = Circle(radius=0.2, color=YELLOW).next_to(image_label, DOWN, buff=0.2)
        self.play(Create(clip_block), FadeIn(image_embedding))
        self.play(image_embedding.animate.move_to(clip_block.get_center()))
        self.wait(0.2)
        
        # Move to Country MLP
        self.play(Create(country_mlp_block))
        self.play(image_embedding.animate.move_to(country_mlp_block.get_center()))
        
        # Transition to MLP (The local refinement stage)
        self.play(
            ReplacementTransform(image_embedding, mlp_layers[0]),
            Create(mlp_full)
        )
        
        # Animate signal flow through the MLP using Indicate
        self.play(Indicate(connections, color=YELLOW, scale_factor=1.02))
        self.play(Indicate(mlp_layers, color=YELLOW))

        # MLP Output points to coordinate/centroid
        self.play(Write(coord_tex))
        self.wait(0.5)

        # Transform coordinate into a GPS pin on the map
        target_centroid = city_centroids[1]
        pin = Dot(color=GREEN, radius=0.15).move_to(target_centroid.get_center())
        pin_pulse = Circle(radius=0.3, color=GREEN).move_to(target_centroid.get_center())
        
        self.play(ReplacementTransform(coord_tex, pin))
        self.play(FadeIn(pin_pulse, scale=0.1))
        self.play(pin_pulse.animate.set_stroke(opacity=0).scale(1.5), run_time=1)
        
        # Show Formula
        self.play(Write(formula))
        self.wait(2)

        # Final narration text
        final_text = Text(
            "Global country to local region refinement",
            font_size=20,
            color=WHITE
        ).next_to(formula, UP, buff=0.2)
        
        self.play(Write(final_text))
        self.wait(3)

        # Cleanup
        self.play(
            FadeOut(pipeline),
            FadeOut(world_map),
            FadeOut(city_centroids),
            FadeOut(pin),
            FadeOut(pin_pulse),
            FadeOut(formula),
            FadeOut(final_text)
        )