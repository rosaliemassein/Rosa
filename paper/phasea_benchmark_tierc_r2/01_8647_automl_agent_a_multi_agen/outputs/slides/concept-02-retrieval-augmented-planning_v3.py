from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Agent Manager (Central Icon)
        manager_rect = RoundedRectangle(height=1.2, width=2.4, color=BLUE, fill_opacity=0.2)
        manager_text = Text("Agent Manager", font_size=24)
        agent_manager = VGroup(manager_rect, manager_text).move_to(ORIGIN)

        # 2. Knowledge Base (Left Icon - Cloud-like)
        kb_circle1 = Circle(radius=0.4, color=GREY, fill_opacity=0.6).shift(LEFT * 0.3 + UP * 0.2)
        kb_circle2 = Circle(radius=0.5, color=GREY, fill_opacity=0.6).shift(RIGHT * 0.3 + UP * 0.1)
        kb_circle3 = Circle(radius=0.4, color=GREY, fill_opacity=0.6).shift(DOWN * 0.2)
        kb_cloud = VGroup(kb_circle1, kb_circle2, kb_circle3)
        kb_label = Text("Knowledge Base", font_size=22).next_to(kb_cloud, DOWN)
        knowledge_base = VGroup(kb_cloud, kb_label).shift(LEFT * 4.5)

        # 3. Formula (Top)
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(UP, buff=1.0)

        # 4. Three Parallel Plans (Right Icons)
        # Plan A: Transformer Strategy
        plan_a_icon = Star(n=5, color=YELLOW, fill_opacity=0.7).scale(0.3)
        plan_a_text = Text("Plan A: Transformer", font_size=18)
        plan_a = VGroup(plan_a_icon, plan_a_text).arrange(RIGHT, buff=0.2)

        # Plan B: CNN Strategy
        plan_b_icon = Square(color=GREEN, fill_opacity=0.7).scale(0.3)
        plan_b_text = Text("Plan B: CNN", font_size=18)
        plan_b = VGroup(plan_b_icon, plan_b_text).arrange(RIGHT, buff=0.2)

        # Plan C: standard strategy
        plan_c_icon = Triangle(color=ORANGE, fill_opacity=0.7).scale(0.3)
        plan_c_text = Text("Plan C: Baseline", font_size=18)
        plan_c = VGroup(plan_c_icon, plan_c_text).arrange(RIGHT, buff=0.2)

        plans = VGroup(plan_a, plan_b, plan_c).arrange(DOWN, buff=0.8).shift(RIGHT * 4)

        # --- ANIMATIONS ---

        # Show initial components
        self.play(FadeIn(knowledge_base), FadeIn(agent_manager))
        self.wait(0.5)

        # Animate arrows pulling 'Knowledge' into the Manager
        arrow_kb = Arrow(knowledge_base.get_right(), agent_manager.get_left(), color=WHITE, buff=0.1)
        # Using string "ITALIC" for slant to avoid undefined identifier
        knowledge_flow_text = Text("Retrieving Knowledge", font_size=16, slant="ITALIC").next_to(arrow_kb, UP)
        
        self.play(Create(arrow_kb), Write(knowledge_flow_text))
        self.play(Write(formula))
        self.wait(0.5)

        # Branching out into three distinct paths
        # ReplacementTransform simulates the "Manager branching out" concept from the remarks
        branch_arrows = VGroup(*[
            Arrow(agent_manager.get_right(), p.get_left(), color=BLUE, buff=0.1)
            for p in plans
        ])

        self.play(
            Create(branch_arrows),
            ReplacementTransform(agent_manager.copy(), plan_a),
            ReplacementTransform(agent_manager.copy(), plan_b),
            ReplacementTransform(agent_manager.copy(), plan_c),
            run_time=2.5
        )

        self.wait(2)