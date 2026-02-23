from manim import *

class ConceptVerificationLoop(Scene):
    def construct(self):
        # Create vertical lines as gates
        req_gate = Line(0, 2 * UP)
        exec_gate = Line(0, 1 * UP)
        imp_gate = Line(0, 0)

        req_gate.set_color(RED)
        exec_gate.set_color(YELLOW)
        imp_gate.set_color(GREEN)

        gates = VGroup(req_gate, exec_gate, imp_gate).arrange_submobjects(buff=0.5)

        # Create the 'Plan' object
        plan = Square(side_length=0.5, color=BLUE)
        plan.move_to(gates[0])

        # Create 'Feedback Loop' text
        feedback_loop = Text("Feedback Loop", font_size=24)
        feedback_loop.next_to(gates, DOWN)

        # Animate the 'Plan' object moving through gates
        self.play(
            Write(feedback_loop),
            Create(plan, run_time=2),

            # Animation of 'Plan' moving through gates
            Transform(plan, gates[1]),
            FadeOut(gates[0], run_time=2),
            Transform(plan, gates[1]),
            FadeOut(gates[0]),
            Transform(plan, gates[2]),
            FadeOut(gates[1]),
        )

        # Animation of 'Plan' moving to the deployment icon
        deployment_icon = Dot(radius=0.2, color=GREEN)
        self.play(
            Transform(plan, deployment_icon),
            Write(feedback_loop.next_to(deployment_icon, DOWN)),
        )

        # Narration
        self.wait(2)
        self.play(
            Write(Text("Finally, we ensure reliability through a three-stage verification gate. First, 'Request Verification' ensures the user's instructions are clear.", font_size=24)),
            Write(Text("Then, 'Execution Verification' filters the most promising plans from the pseudo-results.", font_size=24)),
            Write(Text("Finally, 'Implementation Verification' checks the actual compiled code.", font_size=24)),
            Write(Text("If a solution fails any gate, the feedback is fed back to the Agent Manager, which revises the plans and restarts the loop\u2014ensuring only deployment-ready models. reaches the finish line.", font_size=24))
        )