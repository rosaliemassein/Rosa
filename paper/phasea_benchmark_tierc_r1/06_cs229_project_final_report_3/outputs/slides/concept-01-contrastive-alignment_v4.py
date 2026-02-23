from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Coordinate System
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(RIGHT, buff=1)
        
        axes_label = Text("Shared Embedding Space", font_size=20).next_to(axes, UP)
        origin = axes.coords_to_point(0, 0)

        # 2. Neural Network Encoders
        img_encoder = VGroup(
            Rectangle(height=1.2, width=1.8, color=BLUE),
            Text("Image\nEncoder", font_size=18)
        ).shift(LEFT * 4 + UP * 2)
        
        text_encoder = VGroup(
            Rectangle(height=1.2, width=1.8, color=GREEN),
            Text("Text\nEncoder", font_size=18)
        ).shift(LEFT * 4 + DOWN * 2)

        # 3. Inputs
        # Using placeholder for image as a generic rectangle
        img_placeholder = VGroup(
            Rectangle(height=0.8, width=1.2, color=WHITE, fill_opacity=0.2),
            Text("Street View\n(France)", font_size=12)
        ).next_to(img_encoder, LEFT, buff=0.5)
            
        text_input_france = Text("'A Street View photo in France'", font_size=16, color=YELLOW).next_to(text_encoder, LEFT, buff=0.5)

        # 4. Arrows (Representing Vectors)
        # Using Arrow class as Vector was flagged
        img_vec = Arrow(start=origin, end=axes.coords_to_point(1, 0.4), buff=0, color=BLUE)
        france_vec = Arrow(start=origin, end=axes.coords_to_point(-0.4, 1), buff=0, color=GREEN)
        
        img_label = Text("Image", font_size=16, color=BLUE).next_to(img_vec.get_end(), UR, buff=0.1)
        france_label = Text("France Label", font_size=16, color=GREEN).next_to(france_vec.get_end(), UL, buff=0.1)

        # 5. Value Tracker for Similarity
        sim_tracker = ValueTracker(0.12)
        sim_decimal = DecimalNumber(sim_tracker.get_value(), num_decimal_places=2, color=YELLOW).scale(0.8)
        sim_text = VGroup(
            Text("Cosine Similarity:", font_size=20),
            sim_decimal
        ).arrange(RIGHT).to_edge(DOWN, buff=0.8)
        
        def update_decimal_value(mobject):
            mobject.set_value(sim_tracker.get_value())
            
        sim_decimal.add_updater(update_decimal_value)

        # --- Execution ---

        # Introduction
        self.play(Create(img_encoder), Create(text_encoder), Create(axes), Write(axes_label))
        self.play(FadeIn(img_placeholder), Write(text_input_france))
        self.wait(1)

        # Passing through encoders
        self.play(
            img_placeholder.animate.scale(0.2).move_to(img_encoder.get_center()),
            text_input_france.animate.scale(0.2).move_to(text_encoder.get_center()),
            run_time=1
        )
        self.play(FadeOut(img_placeholder), FadeOut(text_input_france))
        
        # Display Arrows
        self.play(
            Create(img_vec), 
            Create(france_vec),
            Write(img_label),
            Write(france_label)
        )
        self.add(sim_text)
        self.wait(1)

        # Align vectors (Learning process)
        target_point = axes.coords_to_point(0.8, 0.8)
        self.play(
            img_vec.animate.put_start_and_end_on(origin, target_point),
            france_vec.animate.put_start_and_end_on(origin, axes.coords_to_point(0.75, 0.75)),
            img_label.animate.next_to(target_point, UR, buff=0.1),
            france_label.animate.next_to(target_point, DR, buff=0.1),
            sim_tracker.animate.set_value(0.99),
            run_time=2
        )
        self.wait(1)

        # Contrastive Step: Wrong Label
        text_input_japan = Text("'A Street View photo in Japan'", font_size=16, color=RED).next_to(text_encoder, LEFT, buff=0.5)
        self.play(Write(text_input_japan))
        
        japan_vec = Arrow(start=origin, end=axes.coords_to_point(0.7, 0.6), buff=0, color=RED)
        japan_label = Text("Japan Label", font_size=16, color=RED).next_to(japan_vec.get_end(), RIGHT, buff=0.1)

        self.play(text_input_japan.animate.scale(0.1).move_to(text_encoder.get_center()), run_time=1)
        self.play(FadeOut(text_input_japan), Create(japan_vec), Write(japan_label))
        
        # Push Japan away from Image
        away_point = axes.coords_to_point(-0.8, -0.3)
        self.play(
            japan_vec.animate.put_start_and_end_on(origin, away_point),
            japan_label.animate.next_to(away_point, DL, buff=0.1),
            run_time=2
        )
        self.wait(1)

        # Final Formula
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=36)
        formula.to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(axes, axes_label, img_encoder, text_encoder, img_vec, france_vec, japan_vec, img_label, france_label, japan_label, sim_text, formula)))
        self.wait(1)