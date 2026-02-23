from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create the central node for the Agent Manager
        mgr_circle = Circle(radius=0.7, color=RED)
        mgr_symbol = MathTex(r"\mathcal{A}_{mgr}", color=RED)
        manager = VGroup(mgr_circle, mgr_symbol)
        mgr_label = Text("Agent Manager", font_size=24).next_to(manager, UP)

        # 2. Define data for the four specialized agents
        # Format: (Label, Math Symbol, Color, Position)
        agent_data = [
            ("Prompt Agent", r"\mathcal{A}_p", GREEN, UP * 2 + LEFT * 4),
            ("Data Agent", r"\mathcal{A}_d", BLUE, UP * 2 + RIGHT * 4),
            ("Model Agent", r"\mathcal{A}_m", YELLOW, DOWN * 2 + LEFT * 4),
            ("Operation Agent", r"\mathcal{A}_o", ORANGE, DOWN * 2 + RIGHT * 4),
        ]

        agents = VGroup()
        arrows = VGroup()

        for name, symbol, color, pos in agent_data:
            # Create sub-node (Circle + Math Symbol)
            a_circ = Circle(radius=0.6, color=color)
            a_sym = MathTex(symbol, color=color)
            a_node = VGroup(a_circ, a_sym).move_to(pos)
            
            # Create text label for the sub-node
            a_label = Text(name, font_size=20).next_to(a_node, DOWN)
            
            # Group them and add to the main collection
            full_agent = VGroup(a_node, a_label)
            agents.add(full_agent)
            
            # Create arrow from the Manager to the specialized agent
            # buff=0.7 ensures the arrow doesn't overlap the circles
            arr = Arrow(manager.get_center(), a_node.get_center(), buff=0.7, color=GRAY_A)
            arrows.add(arr)

        # 3. Reference Formula at the bottom
        formula = MathTex(
            r"\mathcal{A}_{mgr} \to \{\mathcal{A}_p, \mathcal{A}_d, \mathcal{A}_m, \mathcal{A}_o\}",
            font_size=36
        ).to_edge(DOWN, buff=0.7)

        # 4. User Instruction pulse elements
        user_dot = Dot(LEFT * 6, color=WHITE)
        user_text = Text("User", font_size=20).next_to(user_dot, LEFT)
        user_to_mgr = Arrow(user_dot.get_center(), manager.get_center(), buff=0.1, color=WHITE)

        # --- ANIMATION SEQUENCE ---

        # Phase 1: Build the hierarchy
        self.play(Create(manager), Write(mgr_label))
        self.wait(0.5)

        self.play(
            AnimationGroup(
                *[GrowFromCenter(a) for a in agents],
                *[Create(arr) for arr in arrows],
                lag_ratio=0.2
            )
        )
        self.play(Write(formula))
        self.wait(1)

        # Phase 2: User Instruction Pulse
        self.play(FadeIn(user_dot), Write(user_text))
        self.play(Create(user_to_mgr))
        
        pulse_u = Dot(user_dot.get_center(), color=YELLOW).scale(1.5)
        self.play(pulse_u.animate.move_to(manager.get_center()), run_time=1)
        self.play(FadeOut(pulse_u, scale=2))

        # Phase 3: Task Pulses from Manager to Agents
        # Create dots at the center of the manager
        task_pulses = VGroup(*[
            Dot(manager.get_center(), color=WHITE).scale(0.8) 
            for _ in range(len(agents))
        ])
        
        # Animate each pulse to its respective specialized agent circle
        self.play(
            *[
                task_pulses[i].animate.move_to(agents[i][0].get_center())
                for i in range(len(agents))
            ],
            run_time=1.5
        )
        self.play(FadeOut(task_pulses))

        # Phase 4: Narration and Conclusion
        narration = Text(
            "Imagine an AI project as a construction site.", 
            font_size=24,
            slant=ITALIC
        ).to_edge(UP, buff=0.3)
        
        self.play(FadeIn(narration))
        self.wait(3)