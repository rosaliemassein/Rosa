from manim import *

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # 1. Setup Gates and Labels
        gate_positions = [-2, 0, 2]
        gate_labels = ["ReqVer", "ExecVer", "ImpVer"]
        
        planning_label = Text("Planning", font_size=24).move_to([-5, 1.5, 0])
        deployment_label = Text("Deployment", font_size=24, color=YELLOW).move_to([5, 1.5, 0])
        
        gates = VGroup()
        for x, label in zip(gate_positions, gate_labels):
            line = Line(UP * 1.0, DOWN * 1.0, color=WHITE).shift(RIGHT * x)
            txt = Text(label, font_size=24).next_to(line, UP)
            gates.add(VGroup(line, txt))

        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}", 
            font_size=30
        ).to_edge(DOWN)

        self.add(planning_label, gates, deployment_label, formula)

        # 2. Create the Plan Object
        plan = Square(side_length=0.5, color=BLUE, fill_opacity=0.8).move_to([-5, 0, 0])
        self.add(plan)

        # 3. Animate the first attempt (Failure at ImpVer)
        # Pass ReqVer
        self.play(plan.animate.move_to([-2, 0, 0]))
        # Pass ExecVer
        self.play(plan.animate.move_to([0, 0, 0]))
        # Reach ImpVer and Fail
        self.play(plan.animate.move_to([2, 0, 0]))
        self.play(plan.animate.set_color(RED))
        
        # Feedback loop arrow - Using Arrow with path_arc to replace CurvedArrow
        fail_arrow = Arrow(
            start=plan.get_top(), 
            end=planning_label.get_bottom(), 
            path_arc=-PI/1.5, 
            color=RED
        )
        
        self.play(Create(fail_arrow))
        
        # Loop back to Planning
        self.play(
            plan.animate.move_to([-5, 0, 0]).set_color(BLUE),
            FadeOut(fail_arrow)
        )
        self.wait(0.5)

        # 4. Animate the second attempt (Successful deployment)
        # Move through all gates
        for pos in gate_positions:
            self.play(plan.animate.move_to([pos, 0, 0]), run_time=0.6)
            
        # Successfully passes ImpVer
        self.play(plan.animate.set_color(GREEN))
        
        # Reach Deployment
        deployment_icon = Square(side_length=0.6, color=YELLOW).move_to([5, 0, 0])
        self.play(plan.animate.move_to(deployment_icon.get_center()))
        self.play(Transform(plan, deployment_icon))
        
        self.wait(2)