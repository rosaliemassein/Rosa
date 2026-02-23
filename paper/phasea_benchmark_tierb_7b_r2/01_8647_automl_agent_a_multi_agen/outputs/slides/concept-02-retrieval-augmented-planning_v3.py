from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Formula
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(UP)

        # 2. Agent Manager (Central Icon)
        agent_box = RoundedRectangle(corner_radius=0.2, height=1.5, width=2.5, color=BLUE)
        agent_text = Text("Agent Manager", font_size=24).move_to(agent_box.get_center())
        agent_manager = VGroup(agent_box, agent_text).move_to(ORIGIN)

        # 3. Knowledge Base (Left Icon - Custom Cloud shape)
        cloud_circles = VGroup(
            Circle(radius=0.4, color=WHITE, fill_opacity=0.2).shift(LEFT * 0.4),
            Circle(radius=0.5, color=WHITE, fill_opacity=0.2).shift(UP * 0.2),
            Circle(radius=0.4, color=WHITE, fill_opacity=0.2).shift(RIGHT * 0.4),
            Circle(radius=0.3, color=WHITE, fill_opacity=0.2).shift(DOWN * 0.2 + LEFT * 0.2),
            Circle(radius=0.3, color=WHITE, fill_opacity=0.2).shift(DOWN * 0.2 + RIGHT * 0.2)
        )
        kb_text = Text("Knowledge Base", font_size=20).move_to(cloud_circles.get_center())
        knowledge_base = VGroup(cloud_circles, kb_text).shift(LEFT * 4.5)

        # 4. Plan Icons (Right side)
        # Plan A: Transformer Strategy
        plan_a_icon = Square(side_length=0.8, color=YELLOW)
        plan_a_text = Text("Plan A: Transformer", font_size=18).next_to(plan_a_icon, RIGHT)
        plan_a = VGroup(plan_a_icon, plan_a_text)

        # Plan B: CNN Strategy
        plan_b_icon = Circle(radius=0.4, color=GREEN)
        plan_b_text = Text("Plan B: CNN", font_size=18).next_to(plan_b_icon, RIGHT)
        plan_b = VGroup(plan_b_icon, plan_b_text)

        # Plan C: Alternative Strategy
        plan_c_icon = Triangle(color=RED).scale(0.5)
        plan_c_text = Text("Plan C: Custom", font_size=18).next_to(plan_c_icon, RIGHT)
        plan_c = VGroup(plan_c_icon, plan_c_text)

        plans = VGroup(plan_a, plan_b, plan_c).arrange(DOWN, buff=0.8).shift(RIGHT * 4)

        # --- ANIMATION SEQUENCE ---

        # Show central Manager and Left Knowledge Base
        self.play(FadeIn(agent_manager), FadeIn(knowledge_base))
        self.wait(0.5)

        # Arrows pulling knowledge into the Manager
        arrow_kb_to_mgr = Arrow(knowledge_base.get_right(), agent_manager.get_left(), color=WHITE)
        self.play(GrowArrow(arrow_kb_to_mgr))
        
        # Knowledge transfer visualization (Using simple animate.move_to to avoid MoveAlongPath issues)
        bits = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in range(5)])
        for bit in bits:
            bit.move_to(knowledge_base.get_right())

        self.play(
            LaggedStart(*[
                bit.animate.move_to(agent_manager.get_left())
                for bit in bits
            ], lag_ratio=0.2),
            run_time=1.5
        )
        self.play(FadeOut(bits))
        self.wait(0.5)

        # Formula appearance
        self.play(Write(formula))
        self.wait(0.5)

        # Branching out into three paths
        branch_arrows = VGroup(*[
            Arrow(agent_manager.get_right(), p[0].get_left(), buff=0.2)
            for p in plans
        ])

        # Animate arrows and plan icons appearing
        self.play(
            LaggedStart(*[GrowArrow(arr) for arr in branch_arrows], lag_ratio=0.3),
            LaggedStart(*[
                ReplacementTransform(agent_manager.copy(), p[0]) 
                for p in plans
            ], lag_ratio=0.3),
            run_time=2
        )
        
        # Show plan text labels
        plan_labels = VGroup(*[p[1] for p in plans])
        self.play(Write(plan_labels))
        
        # Final highlight
        self.play(Indicate(plans))
        self.wait(2)