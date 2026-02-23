from manim import *

class Concept03TheElbowThreshold(Scene):
    def construct(self):
        # Axes setup
        axes = Axes(
            x_range=(0, 1.2, 0.1),
            y_range=(0, 1.2, 0.1),
            x_label="Fraction of Zones Flagged",
            y_label="Recall"
        )

        # Plot the concave curve
        x_vals = [0, 0.25, 0.5, 0.75, 1]
        y_vals = [0, 0.4, 0.85, 0.95, 1]
        plot_curve = axes.plot(x_vals, y_vals, color=RED)

        # ValueTracker for the highlighted point
        tracker = ValueTracker(0.5)
        highlight_point = Dot(axes.c2p(tracker.get_value(), 1), color=YELLOW)

        # Side-panel for building floorplan
        floor_plan = VGroup(
            *[
                Rectangle(width=0.1, height=1.5, color=GOLD).set_opacity(0.3)
                for _ in range(10)  # Adjusting the number of zones
            ]
        ).arrange(RIGHT, buff=0.15).move_to(LEFT)
        floor_plan.set_width(floor_plan.width * 2)

        # Update function to highlight the point and update the floor plan
        def update_point(point, param):
            for i in range(10):  # Adjusting the number of zones
                if i < param * 10:  # Highlighting up to the specified percentage
                    floor_plan[i].set_opacity(1)
                else:
                    floor_plan[i].set_opacity(0.3)

        tracker.add_updater(update_point)
        
        # Setting up the scene
        self.play(Create(axes), Write(plot_curve), Create(highlight_point))
        self.wait(2)
        
        # Narration and explanation
        text = Text("We have to decide on a probability threshold. If we set it too low, we flag way too many zones as dominant, which is inefficient. If we set it too high, we miss critical cooling requests.", color=WHITE)
        self.play(Write(text))
        self.wait(5)

        # Highlighting the 'elbow'
        elbow_point = axes.c2p(tracker.get_value(), plot_curve[0].y)
        circle = Circle(radius=0.1, color=YELLOW).move_to(elbow_point).set_opacity(1)
        self.play(Create(circle))

        # Final explanation
        explanation = Text("By plotting the recall — how many requests we correctly caught — against the fraction of zones flagged, we look for the 'elbow' of the curve. This is the sweet spot where we maximize our catch rate while keeping the number of targeted zones as small as possible.", color=WHITE)
        self.play(Write(explanation))
        self.wait(5)

        # Final frame
        self.play(FadeOut(text), FadeOut(explanation))