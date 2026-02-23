from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Formula
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(UP, buff=0.5)
        self.play(Write(formula))

        # 2. Agent Manager (Central)
        am_box = Square(side_length=1.5, color=BLUE).set_fill(BLUE, opacity=0.2)
        am_text = Text("Agent Manager", font_size=20).next_to(am_box, DOWN)
        agent_manager = VGroup(am_box, am_text).move_to(ORIGIN)

        # 3. Knowledge Base (Left)
        cloud = VGroup(
            Circle(radius=0.4).shift(LEFT * 0.3),
            Circle(radius=0.5).shift(UP * 0.2),
            Circle(radius=0.4).shift(RIGHT * 0.3),
            Circle(radius=0.4).shift(DOWN * 0.1)
        ).set_fill(GRAY, opacity=0.3).set_stroke(WHITE, 1)
        kb_text = Text("Knowledge Base", font_size=18).next_to(cloud, DOWN)
        knowledge_base = VGroup(cloud, kb_text).to_edge(LEFT, buff=1)

        # 4. Intro
        self.play(FadeIn(agent_manager), FadeIn(knowledge_base))
        self.wait(0.5)

        # 5. Knowledge Retrieval Animation
        # Pulling knowledge into the manager
        knowledge_flow = Arrow(knowledge_base.get_right(), agent_manager.get_left(), color=YELLOW)
        particle = Dot(color=YELLOW).move_to(knowledge_base.get_center())
        
        self.play(GrowArrow(knowledge_flow))
        self.play(particle.animate.move_to(agent_manager.get_center()), run_time=1)
        self.play(FadeOut(particle), am_box.animate.set_stroke(YELLOW, width=4))
        self.play(am_box.animate.set_stroke(BLUE, width=2))

        # 6. Branching into Parallel Plans (Right)
        # Plan A - Triangle icon
        icon_a = Triangle(color=GOLD).scale(0.3)
        label_a = Text("Plan A: Transformer", font_size=16)
        plan_a = VGroup(icon_a, label_a).arrange(RIGHT, buff=0.2)

        # Plan B - Square icon
        icon_b = Square(color=GREEN).scale(0.3)
        label_b = Text("Plan B: CNN", font_size=16)
        plan_b = VGroup(icon_b, label_b).arrange(RIGHT, buff=0.2)

        # Plan C - Circle icon
        icon_c = Circle(color=RED).scale(0.3)
        label_c = Text("Plan C: Hybrid", font_size=16)
        plan_c = VGroup(icon_c, label_c).arrange(RIGHT, buff=0.2)

        plans = VGroup(plan_a, plan_b, plan_c).arrange(DOWN, buff=1).to_edge(RIGHT, buff=1)

        # Create branching arrows
        branch_arrows = VGroup(*[
            Arrow(agent_manager.get_right(), p.get_left(), buff=0.1)
            for p in plans
        ])

        # Animate Branching
        # Using ReplacementTransform on temporary mobjects to satisfy the "Transforming" concept
        temp_objs = VGroup(*[am_box.copy() for _ in range(3)])
        
        self.play(
            LaggedStart(
                *[Create(arrow) for arrow in branch_arrows],
                *[ReplacementTransform(temp_objs[i], plans[i]) for i in range(3)],
                lag_ratio=0.3,
                run_time=2
            )
        )

        self.wait(3)