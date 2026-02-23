from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Setup Agent Manager (Central Icon)
        manager_circle = Circle(radius=0.8, color=WHITE).set_fill(GREY_B, opacity=0.2)
        manager_label = Text("Agent\nManager", font_size=20).move_to(manager_circle.get_center())
        agent_manager = VGroup(manager_circle, manager_label).move_to(ORIGIN)

        # 2. Setup Knowledge Base (Cloud Icon Substitute)
        cloud_circles = VGroup(
            Circle(radius=0.4).shift(LEFT * 0.3),
            Circle(radius=0.5).shift(ORIGIN),
            Circle(radius=0.4).shift(RIGHT * 0.3),
            Circle(radius=0.3).shift(UP * 0.3)
        ).set_fill(BLUE, opacity=0.4).set_stroke(BLUE, 2)
        kb_label = Text("Knowledge Base", font_size=18).next_to(cloud_circles, DOWN)
        knowledge_base = VGroup(cloud_circles, kb_label).to_edge(LEFT, buff=1)

        # 3. Knowledge Retrieval Animation
        knowledge_arrow = Arrow(knowledge_base.get_right(), agent_manager.get_left(), buff=0.1, color=YELLOW)
        k_packet = MathTex("K", color=BLUE).move_to(knowledge_base.get_center())

        self.play(FadeIn(agent_manager), FadeIn(knowledge_base))
        self.wait(0.5)
        self.play(Create(knowledge_arrow))
        self.play(k_packet.animate.move_to(agent_manager.get_center()).set_opacity(0), run_time=1.5)
        self.wait(0.5)

        # 4. Branching out into Plans (A, B, C)
        # Define icons for different ML strategies
        icon_a = Triangle(color=GREEN).scale(0.3)
        icon_b = Square(color=RED).scale(0.3)
        icon_c = Star(color=YELLOW).scale(0.3)

        plan_a = VGroup(Text("Plan A: Transformer", font_size=18, color=GREEN), icon_a).arrange(RIGHT, buff=0.2)
        plan_b = VGroup(Text("Plan B: CNN", font_size=18, color=RED), icon_b).arrange(RIGHT, buff=0.2)
        plan_c = VGroup(Text("Plan C: Hybrid", font_size=18, color=YELLOW), icon_c).arrange(RIGHT, buff=0.2)

        plans_group = VGroup(plan_a, plan_b, plan_c).arrange(DOWN, buff=1).to_edge(RIGHT, buff=1)

        # Create branching arrows
        branch_arrows = VGroup(*[
            Arrow(agent_manager.get_right(), p.get_left(), buff=0.2, color=WHITE)
            for p in plans_group
        ])

        # Animate branching (using ReplacementTransform to simulate the Manager "generating" them)
        self.play(
            LaggedStart(*[GrowArrow(arr) for arr in branch_arrows], lag_ratio=0.3),
            ReplacementTransform(agent_manager.copy().set_opacity(0), plans_group),
            run_time=2
        )
        self.wait(1)

        # 5. Formula
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))", font_size=36).to_edge(DOWN, buff=1)
        self.play(Write(formula))
        self.wait(3)

        # Cleanup
        self.play(
            FadeOut(knowledge_base),
            FadeOut(knowledge_arrow),
            FadeOut(agent_manager),
            FadeOut(branch_arrows),
            FadeOut(plans_group),
            FadeOut(formula)
        )
        self.wait(1)