from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Agent Manager and Knowledge Base
        # Agent Manager (Central)
        agent_circle = Circle(radius=0.7, color=YELLOW, fill_opacity=0.2)
        agent_label = Text("Agent\nManager", font_size=20)
        agent_manager = VGroup(agent_circle, agent_label).move_to(ORIGIN)

        # Knowledge Base (Left) - Using Circle and stretch instead of Ellipse
        kb_shape = Circle(radius=1.0, color=BLUE, fill_opacity=0.2).stretch(1.5, 0)
        kb_label = Text("Knowledge\nBase", font_size=20)
        knowledge_base = VGroup(kb_shape, kb_label).shift(LEFT * 4.5)

        # 2. Formula (Bottom)
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(DOWN)

        # Animation: Intro
        self.play(FadeIn(agent_manager), FadeIn(knowledge_base))
        self.wait(1)

        # 3. Knowledge Retrieval Animation
        knowledge_particle = Text("Knowledge", font_size=24, color=BLUE)
        knowledge_particle.move_to(knowledge_base.get_center())
        
        arrow = Arrow(knowledge_base.get_right(), agent_manager.get_left(), buff=0.1, color=BLUE)
        
        self.play(Create(arrow))
        self.play(
            knowledge_particle.animate.move_to(agent_manager.get_center()).scale(0.5), 
            run_time=1.5
        )
        self.play(FadeOut(knowledge_particle))
        self.wait(0.5)

        # 4. Branching out into 3 distinct plans
        # Plan A (Transformer strategy)
        plan_a_box = Rectangle(height=0.8, width=2.2, color=GREEN, fill_opacity=0.1)
        plan_a_text = Text("Plan A: Transformer", font_size=16)
        plan_a = VGroup(plan_a_box, plan_a_text).shift(RIGHT * 4 + UP * 2)

        # Plan B (CNN strategy)
        plan_b_box = Rectangle(height=0.8, width=2.2, color=RED, fill_opacity=0.1)
        plan_b_text = Text("Plan B: CNN", font_size=16)
        plan_b = VGroup(plan_b_box, plan_b_text).shift(RIGHT * 4)

        # Plan C (Standard strategy)
        plan_c_box = Rectangle(height=0.8, width=2.2, color=ORANGE, fill_opacity=0.1)
        plan_c_text = Text("Plan C: Basic", font_size=16)
        plan_c = VGroup(plan_c_box, plan_c_text).shift(RIGHT * 4 + DOWN * 2)

        # Connectors
        line_a = Line(agent_manager.get_right(), plan_a.get_left(), color=WHITE)
        line_b = Line(agent_manager.get_right(), plan_b.get_left(), color=WHITE)
        line_c = Line(agent_manager.get_right(), plan_c.get_left(), color=WHITE)

        # Branching animation
        self.play(
            Create(line_a), Create(line_b), Create(line_c),
            ReplacementTransform(agent_manager.copy(), plan_a),
            ReplacementTransform(agent_manager.copy(), plan_b),
            ReplacementTransform(agent_manager.copy(), plan_c),
            run_time=2
        )
        self.wait(1)

        # 5. Icons for ML strategies
        transformer_icon = Square(side_length=0.3, color=GREEN).next_to(plan_a, RIGHT)
        cnn_icon = Circle(radius=0.15, color=RED).next_to(plan_b, RIGHT)
        standard_icon = Triangle(color=ORANGE).scale(0.15).next_to(plan_c, RIGHT)

        self.play(
            Create(transformer_icon),
            Create(cnn_icon),
            Create(standard_icon)
        )

        # 6. Final Formula reveal
        self.play(Write(formula))
        self.wait(2)