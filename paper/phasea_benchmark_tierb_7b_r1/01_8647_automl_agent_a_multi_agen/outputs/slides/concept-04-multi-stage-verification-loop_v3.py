from manim import *
import numpy as np

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # 1. Setup Positions
        planning_point = np.array([-5, 0, 0])
        gate_x_coords = [-2, 0, 2]
        deployment_point = np.array([5, 0, 0])
        
        # 2. Create Mobjects
        planning_label = Text("Planning", font_size=24).move_to(planning_point + DOWN * 0.7)
        
        gates = VGroup(*[Line(UP * 1.5, DOWN * 1.5).move_to([x, 0, 0]) for x in gate_x_coords])
        
        gate_labels = VGroup(
            Text("ReqVer", font_size=20).next_to(gates[0], UP),
            Text("ExecVer", font_size=20).next_to(gates[1], UP),
            Text("ImpVer", font_size=20).next_to(gates[2], UP)
        )
        
        deployment_icon = Star(color=GOLD, n_points=5).scale(0.3).move_to(deployment_point)
        deployment_label = Text("Deployment", font_size=20).next_to(deployment_icon, DOWN)
        
        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}",
            font_size=32
        ).to_edge(DOWN, buff=0.5)
        
        plan = Square(side_length=0.4, color=BLUE, fill_opacity=1).move_to(planning_point)

        # 3. Initial Display
        self.add(planning_label, gates, gate_labels, deployment_icon, deployment_label, formula)
        self.play(FadeIn(plan))
        self.wait(0.5)

        # 4. Animation: Failed Attempt (Loop back)
        # Move to first gate and fail
        self.play(plan.animate.move_to([gate_x_coords[0], 0, 0]), run_time=1)
        self.play(plan.animate.set_color(RED))
        
        # Feedback loop arrow (Using Arrow with path_arc instead of CurvedArrow)
        loop_arrow = Arrow(
            start=plan.get_top(), 
            end=planning_point + UP * 0.5, 
            path_arc=-PI/1.2,
            color=RED,
            buff=0.1
        )
        
        self.play(Create(loop_arrow))
        self.play(
            plan.animate.move_to(planning_point).set_color(BLUE),
            run_time=1.5
        )
        self.play(FadeOut(loop_arrow))
        self.wait(0.5)

        # 5. Animation: Successful Pass
        # Pass Gate 1
        self.play(plan.animate.move_to([gate_x_coords[0], 0, 0]))
        self.play(plan.animate.set_color(GREEN))
        
        # Pass Gate 2
        self.play(plan.animate.move_to([gate_x_coords[1], 0, 0]))
        self.play(plan.animate.set_color(GREEN))
        
        # Pass Gate 3
        self.play(plan.animate.move_to([gate_x_coords[2], 0, 0]))
        self.play(plan.animate.set_color(GREEN))
        
        # Reach Deployment
        self.play(plan.animate.move_to(deployment_point))
        self.play(
            Flash(deployment_icon, color=GOLD, line_length=0.3),
            plan.animate.scale(0).set_opacity(0),
            deployment_icon.animate.scale(1.5),
            run_time=1
        )
        
        self.wait(2)