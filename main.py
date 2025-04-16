import re
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

from backend import PhysicsAI
from Physics_solver.NLP_processing import NLPProcessor  # ✅ Import your NLP module

def preprocess_equation(equation: str) -> str:
    equation = equation.replace("^", "**")
    equation = re.sub(r"\s+", "", equation)
    equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)
    equation = re.sub(r"([a-zA-Z])([a-zA-Z])", r"\1*\2", equation)
    return equation

class IntegratedPhysicsSolverApp(MDApp):
    def build(self):
        self.title = "Integrated Physics Solver (with NLP)"
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        card = MDCard(orientation="vertical", padding=20, spacing=20)

        # NLP input
        self.nlp_input = MDTextField(
            hint_text="Or enter a sentence (e.g., 'Find the force when mass is 5kg and acceleration is 3m/s^2')",
            size_hint=(1, None),
            height=80
        )
        card.add_widget(self.nlp_input)

        # NLP Button
        parse_nlp_button = MDRaisedButton(
            text="Parse NLP Sentence",
            size_hint=(1, None),
            height=40,
            on_release=self.parse_nlp
        )
        card.add_widget(parse_nlp_button)

        # Equation input
        self.equation_input = MDTextField(
            hint_text="Enter equation (e.g., F = m c^2 or F = m c)",
            size_hint=(1, None),
            height=40
        )
        card.add_widget(self.equation_input)

        # Generate Fields
        gen_fields_button = MDRaisedButton(
            text="Generate Fields",
            size_hint=(1, None),
            height=40,
            on_release=self.generate_fields
        )
        card.add_widget(gen_fields_button)

        # Variable Input Fields
        self.scroll = MDScrollView(size_hint=(1, None), height=200)
        self.fields_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        self.fields_box.bind(minimum_height=self.fields_box.setter("height"))
        self.scroll.add_widget(self.fields_box)
        card.add_widget(self.scroll)

        # Solve
        solve_button = MDRaisedButton(
            text="Solve Equation",
            size_hint=(1, None),
            height=40,
            on_release=self.solve_equation_ui
        )
        card.add_widget(solve_button)

        # Result label
        self.result_label = MDLabel(
            text="Result will appear here",
            size_hint=(1, None),
            height=40
        )
        card.add_widget(self.result_label)

        main_layout.add_widget(card)
        return main_layout

    def parse_nlp(self, instance):
        sentence = self.nlp_input.text.strip()
        if not sentence:
            self.result_label.text = "Please enter a sentence first."
            return

        nlp = NLPProcessor()
        equation, values = nlp.parse(sentence)

        if not equation:
            self.result_label.text = "Could not detect equation. Try another sentence."
            return

        # Auto-fill equation field
        self.equation_input.text = equation

        # Generate input fields for variables
        self.generate_fields(None)

        # Auto-fill known values from NLP
        for child in self.fields_box.children:
            if hasattr(child, "variable_name"):
                var = child.variable_name.lower()
                if var in values:
                    child.text = values[var]

        self.result_label.text = "NLP parsed successfully. Equation & values updated."

    def generate_fields(self, instance):
        raw_eq = self.equation_input.text.strip()
        if not raw_eq or "=" not in raw_eq:
            self.result_label.text = "Please enter a valid equation with '='."
            return

        processed_eq = preprocess_equation(raw_eq)
        self.processed_equation = processed_eq
        self.fields_box.clear_widgets()
        self.variables = list(set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', processed_eq)))

        for var in self.variables:
            tf = MDTextField(
                hint_text=f"Enter value for {var} (include units)",
                size_hint=(1, None),
                height=40
            )
            tf.variable_name = var
            self.fields_box.add_widget(tf)

        self.result_label.text = "Fields generated. Enter known values, leave one blank."

    def solve_equation_ui(self, instance):
        if not hasattr(self, "processed_equation"):
            self.result_label.text = "Please generate fields first."
            return

        knowns = {}
        for child in self.fields_box.children:
            var = child.variable_name
            val = child.text.strip()
            if val:
                knowns[var.lower()] = val

        missing = [v for v in self.variables if v.lower() not in knowns]
        if len(missing) != 1:
            self.result_label.text = f"Exactly one variable must be left blank. Found {len(missing)} missing."
            return

        try:
            result = PhysicsAI().solve_equation(self.processed_equation, knowns)
            self.result_label.text = result
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

if __name__ == "__main__":
    IntegratedPhysicsSolverApp().run()
