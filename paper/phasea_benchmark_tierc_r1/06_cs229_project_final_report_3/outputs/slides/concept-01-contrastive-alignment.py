from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # Create the text and image
        voice_text = Text("To figure out where a photo was taken, we first need to align visual features with geographic concepts.")
        text_label = Text("Goal: Align images with country-specific text descriptions in a shared embedding space.")
        explanation_text = Text("Create two neural network blocks labeled 'Image Encoder' and 'Text Encoder'. Show a Street View image entering the Image Encoder and the text 'A Street View photo in France' entering the Text Encoder. Represent the output as two vectors (arrows) in a 2D coordinate system. Animate the two vectors rotating to point in the same direction. Then, show a 'wrong' text label like 'A Street View photo in Japan' and show its vector being pushed away from the image vector. Use a ValueTracker to show the similarity score increasing as they align.")
        formula_text = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})")
        image = ImageMobject("img-7.jpeg").scale(0.4)

        # Arrange text
        text_group = VGroup(text_label, explanation_text, formula_text).arrange(DOWN)

        # Create and arrange the vectors
        vector1 = Arrow(ORIGIN, RIGHT).next_to(text_label, DOWN)
        vector2 = Arrow(ORIGIN, LEFT).next_to(formula_text, DOWN)

        # Animate vectors aligning
        self.play(Write(text_label))
        self.wait()
        self.add(vector1)
        vector1_text = Text("Image Embedding").next_to(vector1, RIGHT)
        self.add(vector1_text)

        self.play(Transform(vector1_text, vector1.animate.next_to(ORIGIN, RIGHT)))
        self.wait()
        self.add(vector2)
        vector2_text = Text("Text Embedding").next_to(vector2, LEFT)
        self.add(vector2_text)

        self.wait()
        vector1.animate.rotate(PI / 4)
        vector2.animate.rotate(-PI / 4)
        self.wait()
        self.add(vector1_text, vector2_text)

        # Animation of 'wrong' text
        wrong_text = Text("A Street View photo in Japan")
        self.wait()
        self.add(wrong_text)
        wrong_vector = Arrow(ORIGIN, LEFT).next_to(wrong_text, DOWN)

        self.wait()
        wrong_vector.animate.scale(0.5).set_color(RED)
        self.wait()

        # ValueTracker for similarity score
        value_tracker = ValueTracker(0)
        update_vector1_text = always_redraw(lambda: vector1_text.set_value(f"Similarity: {value_tracker.get_value():.2f}"))
        self.add(update_vector1_text)

        # Run a loop to animate similarity score
        for i in range(-8, 9):
            value_tracker.set_value(i / 10)
            self.wait(0.1)

        # Final text
        final_text = Text("This contrastive approach teaches the model that architectural styles, vegetation, and road signs are all linked to specific country names.")
        self.wait()
        self.add(final_text)