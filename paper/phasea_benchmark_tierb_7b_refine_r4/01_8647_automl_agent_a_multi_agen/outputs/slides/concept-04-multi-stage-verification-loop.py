from manim import *

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # Create the gates and pass/fail indicators
        req_ver_gate = Rectangle(width=2, height=1).move_to(LEFT * 3)
        exec_ver_gate = Rectangle(width=2, height=1).move_to(LEFT * 0)
        imp_ver_gate = Rectangle(width=2, height=1).move_to(RIGHT * 3)

        pass_indicator = Text("Pass", font_size=20).next_to(req_ver_gate, UP)
        fail_indicator = Text("Fail", font_size=20).next_to(req_ver_gate, DOWN)

        # Create the plan
        plan = Square(side_length=0.5).move_to(LEFT * 1)

        # Create the deployment icon
        deployment_icon = Text("Deployment", font_size=30).move_to(RIGHT * 6)

        # Animate the plan moving through the gates
        self.play(FadeIn(req_ver_gate), FadeIn(exec_ver_gate), FadeIn(imp_ver_gate))
        self.play(FadeIn(plan))

        for gate in [req_ver_gate, exec_ver_gate, imp_ver_gate]:
            self.play(plan.animate.shift(RIGHT * 3))
            if gate == req_ver_gate:
                plan.set_color(RED)
                self.play(plan.animate.shift(LEFT * 6))
            elif gate == exec_ver_gate:
                plan.set_color(RED)
                self.play(plan.animate.shift(LEFT * 3))
            else:
                plan.set_color(GREEN)

        self.play(plan.animate.shift(RIGHT * 3))
        self.play(FadeIn(deployment_icon))