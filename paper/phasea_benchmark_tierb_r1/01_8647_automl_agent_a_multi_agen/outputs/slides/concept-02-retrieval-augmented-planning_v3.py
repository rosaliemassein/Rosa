from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Setup Elements
        # Agent Manager (Central)
        agent_manager_rect = RoundedRectangle(corner_radius=0.2, height=1.5, width=3, color=BLUE)
        agent_manager_text = Text("Agent Manager", font_size=24).move_to(agent_manager_rect.get_center())
        agent_manager = VGroup(agent_manager_rect, agent_manager_text).center()

        # Knowledge Base (Left)
        kb_rect = RoundedRectangle(corner_radius=0.5, height=1.5, width=3, color=GREY_A)
        kb_text = Text("Knowledge Base\n(arXiv, Web)", font_size=20).move_to(kb_rect.get_center())
        knowledge_base = VGroup(kb_rect, kb_text).to_edge(LEFT, buff=1)

        # Formula (Top)
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))", font_size=36).to_edge(UP, buff=0.5)

        # 2. Animations - Retrieval
        self.play(Create(agent_manager), Create(knowledge_base))
        self.play(Write(formula))
        self.wait(0.5)

        # Pulling knowledge into the manager
        arrow_kb_to_mgr = Arrow(knowledge_base.get_right(), agent_manager.get_left(), buff=0.2, color=YELLOW)
        
        # Represent knowledge bits
        dots = VGroup(*[Dot(color=YELLOW).move_to(knowledge_base.get_right()) for _ in range(3)])
        
        self.play(Create(arrow_kb_to_mgr))
        self.play(
            LaggedStart(
                *[d.animate.move_to(agent_manager.get_left()).set_opacity(0) for d in dots],
                lag_ratio=0.3
            ),
            run_time=2
        )

        # 3. Branching into Plans (Right)
        # Create plan icons/labels
        plan_a = VGroup(Square(side_length=1, color=GREEN), Text("Plan A\n(Transformer)", font_size=16)).scale(0.8)
        plan_b = VGroup(Square(side_length=1, color=ORANGE), Text("Plan B\n(CNN)", font_size=16)).scale(0.8)
        plan_c = VGroup(Square(side_length=1, color=PURPLE), Text("Plan C\n(Hybrid)", font_size=16)).scale(0.8)

        plans = VGroup(plan_a, plan_b, plan_c).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)

        # Create branching arrows
        arrow_a = Arrow(agent_manager.get_right(), plan_a.get_left(), buff=0.2)
        arrow_b = Arrow(agent_manager.get_right(), plan_b.get_left(), buff=0.2)
        arrow_c = Arrow(agent_manager.get_right(), plan_c.get_left(), buff=0.2)

        # Animate branching
        self.play(
            Create(arrow_a),
            Create(arrow_b),
            Create(arrow_c),
            ReplacementTransform(agent_manager.copy(), plan_a),
            ReplacementTransform(agent_manager.copy(), plan_b),
            ReplacementTransform(agent_manager.copy(), plan_c),
            run_time=2
        )

        # Final Narration Text
        narration_text = Text(
            "Queries external knowledge to generate parallel plans.",
            font_size=20,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(narration_text))
        self.wait(3)