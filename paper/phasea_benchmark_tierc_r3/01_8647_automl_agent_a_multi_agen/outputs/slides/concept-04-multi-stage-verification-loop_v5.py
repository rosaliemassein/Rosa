from manim import *

class ConceptVerification(Scene):
    def construct(self):
        # 1. Setup Gates and Labels
        gate_positions = [LEFT * 3, ORIGIN, RIGHT * 3]
        gate_names = ["ReqVer", "ExecVer", "ImpVer"]
        
        gates = VGroup()
        for pos, name in zip(gate_positions, gate_names):
            line = Line(UP * 1.5, DOWN * 1.5, color=WHITE)
            line.move_to(pos)
            label = Text(name, font_size=24).next_to(line, UP)
            gates.add(VGroup(line, label))
        
        # 2. Planning and Deployment areas
        planning_box = VGroup(
            Rectangle(height=1.5, width=2.5, color=BLUE),
            Text("Agent Manager\n(Planning)", font_size=20)
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 2)
        
        deployment_icon = VGroup(
            Star(color=YELLOW, fill_opacity=1).scale(0.5),
            Text("Deployment", font_size=20).next_to(Star().scale(0.5), DOWN)
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 2)

        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}",
            font_size=34
        ).to_edge(UP, buff=0.5)

        self.add(gates, planning_box, deployment_icon, formula)

        # 3. The 'Plan' object (Small Square)
        plan = Square(side_length=0.4, color=BLUE, fill_opacity=0.8)
        plan.move_to(planning_box.get_center())

        # 4. Animation: The Failure Loop
        self.play(FadeIn(plan))
        # Move to first gate
        self.play(plan.animate.move_to(gate_positions[0]))
        self.wait(0.3)
        
        # Change color to red to indicate failure
        self.play(plan.animate.set_color(RED))
        
        # Loop back to Planning stage using an Arrow with path_arc (replaces CurvedArrow)
        feedback_arrow = Arrow(
            start=plan.get_top(), 
            end=planning_box.get_top(), 
            path_arc=-1.5, 
            color=RED,
            buff=0.1
        )
        feedback_text = Text("Feedback", font_size=18, color=RED).next_to(feedback_arrow, UP)
        
        self.play(Create(feedback_arrow), Write(feedback_text))
        self.wait(1)
        
        # Return to start and reset for the successful attempt
        self.play(
            plan.animate.move_to(planning_box.get_center()).set_color(BLUE),
            FadeOut(feedback_arrow),
            FadeOut(feedback_text)
        )
        self.wait(0.5)

        # 5. Animation: The Success Loop
        # Iterate through each gate, turning green at each step
        for i in range(3):
            self.play(plan.animate.move_to(gate_positions[i]))
            self.play(plan.animate.set_color(GREEN))
            self.wait(0.2)
        
        # Move to Deployment icon
        self.play(plan.animate.move_to(deployment_icon[0].get_center()))
        self.play(
            plan.animate.scale(1.2).set_opacity(0),
            deployment_icon[0].animate.set_color(GREEN).scale(1.2)
        )
        
        # Show final success message
        success_msg = Text("Reliability Verified", font_size=28, color=GREEN).to_edge(DOWN, buff=0.5)
        self.play(Write(success_msg))
        self.wait(2)