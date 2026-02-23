from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # Create icons
        agent_manager = Text("Agent Manager").to_edge(UP)
        knowledge_base = Text("Knowledge Base (Cloud)").next_to(agent_manager, LEFT).shift(LEFT)
        plan_a = Text("Plan A (Transformer)").next_to(agent_manager, RIGHT).shift(RIGHT)
        plan_b = Text("Plan B (CNN)").next_to(agent_manager, RIGHT).shift(RIGHT * 2)
        plan_c = Text("Plan C (LSTM)").next_to(agent_manager, RIGHT).shift(RIGHT * 3)

        # Connect Knowledge Base to Agent Manager
        arrow_kb_to_manager = Arrow(start=knowledge_base.get_bottom(), end=agent_manager.get_top())
        self.play(FadeIn(knowledge_base), FadeIn(agent_manager))
        self.play(Create(arrow_kb_to_manager))

        # Branch out into multiple plans
        self.wait()
        plans = VGroup(plan_a, plan_b, plan_c)
        plans.arrange(RIGHT, buff=2).next_to(agent_manager, DOWN)
        self.play(Create(plans))

        # Explain how plans are generated using RAP
        rap_text = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(RIGHT).shift(DOWN)
        self.play(Create(rap_text), Write(rap_text))