from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Formula at the top
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))")
        formula.to_edge(UP, buff=0.5)
        
        # 2. Narration text at the bottom
        narration_text = Text(
            "Retrieval-Augmented Planning (RAP) queries external knowledge\nto explore diverse parallel strategies.",
            font_size=20,
            line_spacing=1.5
        ).to_edge(DOWN, buff=0.5)

        # 3. Create Icons
        # Agent Manager (Central)
        agent_manager = VGroup(
            Circle(radius=0.7, color=BLUE, fill_opacity=0.3),
            Text("Agent Manager", font_size=18)
        ).move_to(ORIGIN)

        # Knowledge Base (Left) - A simple cloud-like collection of circles
        c1 = Circle(radius=0.4).shift(LEFT * 0.3)
        c2 = Circle(radius=0.5).shift(UP * 0.2)
        c3 = Circle(radius=0.4).shift(RIGHT * 0.3)
        cloud = VGroup(c1, c2, c3).set_fill(GREY_B, opacity=0.8).set_stroke(WHITE, 2)
        
        kb_group = VGroup(
            cloud,
            Text("Knowledge Base", font_size=16, color=WHITE).next_to(cloud, DOWN, buff=0.1)
        ).shift(LEFT * 4.5)

        # Plan Icons (Right)
        plan_a = VGroup(
            Square(side_length=0.8, color=RED, fill_opacity=0.5),
            Text("Plan A: Transformer", font_size=14).next_to(Square(side_length=0.8), DOWN)
        ).shift(RIGHT * 4.5 + UP * 2)

        plan_b = VGroup(
            Triangle(color=GREEN, fill_opacity=0.5).scale(0.6),
            Text("Plan B: CNN", font_size=14).next_to(Triangle().scale(0.6), DOWN)
        ).shift(RIGHT * 4.5)

        plan_c = VGroup(
            Circle(radius=0.4, color=GOLD, fill_opacity=0.5),
            Text("Plan C: Custom", font_size=14).next_to(Circle(radius=0.4), DOWN)
        ).shift(RIGHT * 4.5 + DOWN * 2)

        # 4. Animation Sequence
        self.play(Write(formula), Write(narration_text))
        self.play(FadeIn(agent_manager), FadeIn(kb_group))
        self.wait(1)

        # Knowledge Retrieval animation (Particles moving from KB to Manager)
        retrieval_arrow = Arrow(kb_group.get_right(), agent_manager.get_left(), color=YELLOW, buff=0.1)
        knowledge_label = Text("External Knowledge", font_size=14, color=YELLOW).next_to(retrieval_arrow, UP)
        
        self.play(GrowArrow(retrieval_arrow), FadeIn(knowledge_label))
        
        # Creating particles for retrieval
        particles = VGroup(*[Dot(color=YELLOW, radius=0.06) for _ in range(5)])
        for p in particles:
            p.move_to(kb_group.get_right())

        self.play(
            LaggedStart(
                *[p.animate.move_to(agent_manager.get_left()) for p in particles],
                lag_ratio=0.2,
                run_time=1.5
            )
        )
        
        self.play(FadeOut(particles), FadeOut(retrieval_arrow), FadeOut(knowledge_label))
        self.play(agent_manager[0].animate.set_fill(YELLOW, opacity=0.4)) 
        self.wait(0.5)

        # Branching into Multiple Plans
        path_a = Line(agent_manager.get_right(), plan_a.get_left(), color=WHITE, stroke_width=2)
        path_b = Line(agent_manager.get_right(), plan_b.get_left(), color=WHITE, stroke_width=2)
        path_c = Line(agent_manager.get_right(), plan_c.get_left(), color=WHITE, stroke_width=2)

        # Using copies of the manager to transform into the three plans
        mgr_copy_a = agent_manager.copy()
        mgr_copy_b = agent_manager.copy()
        mgr_copy_c = agent_manager.copy()

        self.play(
            Create(path_a),
            Create(path_b),
            Create(path_c)
        )

        self.play(
            ReplacementTransform(mgr_copy_a, plan_a),
            ReplacementTransform(mgr_copy_b, plan_b),
            ReplacementTransform(mgr_copy_c, plan_c),
            run_time=2
        )
        
        # Defining a custom rate function to replace there_and_back
        def custom_back_and_forth(t):
            if t < 0.5:
                return t * 2
            else:
                return 2 - (t * 2)

        self.play(
            plan_a.animate.scale(1.15),
            plan_b.animate.scale(1.15),
            plan_c.animate.scale(1.15),
            rate_func=custom_back_and_forth,
            run_time=2
        )
        
        self.wait(2)