from manim import *

class Concept02RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Icons and Layout
        # Central Agent Manager
        manager_circle = Circle(radius=0.7, color=GOLD, fill_opacity=0.2, fill_color=GOLD)
        manager_label = Text("Agent Manager", font_size=20).next_to(manager_circle, DOWN)
        manager = VGroup(manager_circle, manager_label).move_to(ORIGIN)

        # Knowledge Base to its left (using a cloud-like shape)
        kb_blobs = VGroup(
            Circle(radius=0.5).shift(LEFT * 0.3),
            Circle(radius=0.6).shift(RIGHT * 0.3),
            Circle(radius=0.4).shift(UP * 0.4)
        ).set_color(BLUE).set_fill(BLUE, opacity=0.4)
        kb_label = Text("Knowledge\nBase", font_size=20).move_to(kb_blobs.get_center())
        knowledge_base = VGroup(kb_blobs, kb_label).shift(LEFT * 4 + UP * 1)

        # 2. Initial Display
        self.play(FadeIn(manager), FadeIn(knowledge_base))
        self.wait(1)

        # 3. Knowledge Retrieval Animation
        # Line from KB to Manager
        connector_line = Line(knowledge_base.get_right(), manager.get_left(), color=YELLOW, stroke_width=2)
        knowledge_dot = Dot(color=YELLOW).move_to(knowledge_base.get_center())
        
        self.play(Create(connector_line))
        self.play(knowledge_dot.animate.move_to(manager.get_center()), run_time=1.2)
        self.play(FadeOut(knowledge_dot), FadeOut(connector_line))

        # 4. Branching out into parallel plans
        # Plan A
        p1_shape = Square(side_length=0.7, color=BLUE)
        p1_text = Text("Plan A: Transformer", font_size=18).next_to(p1_shape, RIGHT)
        plan_a = VGroup(p1_shape, p1_text).move_to(RIGHT * 3.5 + UP * 1.8)
        
        # Plan B
        p2_shape = Triangle(color=GREEN).scale(0.4)
        p2_text = Text("Plan B: CNN", font_size=18).next_to(p2_shape, RIGHT)
        plan_b = VGroup(p2_shape, p2_text).move_to(RIGHT * 3.5)
        
        # Plan C
        p3_shape = Circle(radius=0.35, color=RED)
        p3_text = Text("Plan C: Hybrid", font_size=18).next_to(p3_shape, RIGHT)
        plan_c = VGroup(p3_shape, p3_text).move_to(RIGHT * 3.5 + DOWN * 1.8)
        
        line_a = Line(manager.get_right(), plan_a.get_left(), color=GRAY, stroke_width=2)
        line_b = Line(manager.get_right(), plan_b.get_left(), color=GRAY, stroke_width=2)
        line_c = Line(manager.get_right(), plan_c.get_left(), color=GRAY, stroke_width=2)

        self.play(
            Create(line_a), Create(line_b), Create(line_c),
            FadeIn(plan_a), FadeIn(plan_b), FadeIn(plan_c),
            run_time=2
        )

        # 5. Narration Text (Sequential updates)
        narrations = [
            "To find the best path, we use Retrieval-Augmented Planning (RAP).",
            "It queries external knowledge like arXiv or web searches.",
            "This generates multiple diverse plans in parallel."
        ]
        
        current_text = Text(narrations[0], font_size=24).to_edge(UP)
        self.play(Write(current_text))
        self.wait(2)
        
        for next_line in narrations[1:]:
            new_text = Text(next_line, font_size=24).to_edge(UP)
            self.play(ReplacementTransform(current_text, new_text))
            current_text = new_text
            self.wait(2)

        # 6. Formula animation
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))")
        formula.scale(1.1)
        formula.to_edge(DOWN, buff=0.8)
        self.play(Write(formula))
        self.wait(1.5)

        # 7. Image reference (Safe Check)
        try:
            image_ref = ImageMobject("img-2.jpeg")
            image_ref.scale(0.4).to_corner(DR, buff=0.5)
            self.play(FadeIn(image_ref))
        except:
            pass
            
        self.wait(3)