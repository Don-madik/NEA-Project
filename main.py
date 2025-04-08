import re
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

# Import our backend solver via PhysicsAI.
from backend import PhysicsAI

# ---------------------------
# Preprocessing Function
# ---------------------------
def preprocess_equation(equation: str) -> str:
    """
    Converts a user-friendly equation string into valid Python syntax:
      - Replace '^' with '**' for exponentiation.
      - Remove whitespace.
      - Insert '*' for implicit multiplications (e.g., "mc" becomes "m*c").
    """
    # Replace caret with exponentiation.
    equation = equation.replace("^", "**")
    # Remove all whitespace.
    equation = re.sub(r"\s+", "", equation)
    # Insert multiplication between digit and letter (e.g., "2m" -> "2*m").
    equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)
    # Insert multiplication between letters (e.g., "mc" -> "m*c").
    equation = re.sub(r"([a-zA-Z])([a-zA-Z])", r"\1*\2", equation)
    return equation

# ---------------------------
# Integrated KivyMD Application
# ---------------------------
class IntegratedPhysicsSolverApp(MDApp):
    def build(self):
        self.title = "Integrated Physics Equation Solver (with Pint in unit_store)"
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        
        # Create a card for grouping UI elements.
        card = MDCard(orientation="vertical", padding=20, spacing=20)
        
        # Equation input field (user-friendly).
        self.equation_input = MDTextField(
            hint_text="Enter equation (e.g., F = m c^2 or F = m c)",
            size_hint=(1, None),
            height=40
        )
        card.add_widget(self.equation_input)
        
        # Button: Generate Fields.
        gen_fields_button = MDRaisedButton(
            text="Generate Fields",
            size_hint=(1, None),
            height=40,
            on_release=self.generate_fields
        )
        card.add_widget(gen_fields_button)
        
        # ScrollView for dynamic variable input fields.
        self.scroll = MDScrollView(size_hint=(1, None), height=200)
        self.fields_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        self.fields_box.bind(minimum_height=self.fields_box.setter("height"))
        self.scroll.add_widget(self.fields_box)
        card.add_widget(self.scroll)
        
        # Button: Solve Equation.
        solve_button = MDRaisedButton(
            text="Solve Equation",
            size_hint=(1, None),
            height=40,
            on_release=self.solve_equation_ui
        )
        card.add_widget(solve_button)
        
        # Label to display result or error messages.
        self.result_label = MDLabel(
            text="Result will appear here",
            size_hint=(1, None),
            height=40
        )
        card.add_widget(self.result_label)
        
        main_layout.add_widget(card)
        return main_layout

    def generate_fields(self, instance):
        """
        Preprocess the raw equation, extract variable names,
        and dynamically generate input fields.
        The user should enter known values with units (e.g., '100 N')
        and leave exactly one field blank as the unknown.
        """
        raw_eq = self.equation_input.text.strip()
        if not raw_eq or "=" not in raw_eq:
            self.result_label.text = "Please enter a valid equation with '='."
            return
        
        # Preprocess the equation to valid Python syntax.
        processed_eq = preprocess_equation(raw_eq)
        self.processed_equation = processed_eq  # Save for later use.
        
        # Clear previously generated fields.
        self.fields_box.clear_widgets()
        
        # Extract variables from the processed equation.
        self.variables = list(set(re.findall(r'\b[a-zA-Z]\b', processed_eq)))
        
        # Create a dynamic text field for each variable.
        for var in self.variables:
            tf = MDTextField(
                hint_text=f"Enter value for {var} (include units, e.g., '100 N'; leave blank if unknown)",
                size_hint=(1, None),
                height=40
            )
            # Attach the variable name.
            tf.variable_name = var
            self.fields_box.add_widget(tf)
        
        self.result_label.text = "Fields generated. Enter known values with units, leaving one blank for unknown."

    def solve_equation_ui(self, instance):
        """
        Reads the values from the generated fields.
        Known values (as strings with units) are passed to the backend.
        The updated UnitAwareVariableStore (using Pint) within the backend will handle conversion.
        """
        if not hasattr(self, "processed_equation"):
            self.result_label.text = "Please generate fields first."
            return

        knowns = {}
        unknown_count = 0
        
        # Gather known values from each field.
        for child in self.fields_box.children:
            var = child.variable_name
            val = child.text.strip()
            if val == "":
                unknown_count += 1
            else:
                # Do not preprocess these values—they should be passed as-is (e.g., "100 N").
                knowns[var] = val
        
        if unknown_count != 1:
            self.result_label.text = "Exactly one variable must be left blank for the unknown."
            return
        
        try:
            physics_ai = PhysicsAI()
            # The PhysicsAI class should internally use UnitAwareVariableStore from unit_store.py.
            result = physics_ai.solve_equation(self.processed_equation, knowns)
            self.result_label.text = f"{result}"
        except Exception as e:
            self.result_label.text = "Error: " + str(e)

if __name__ == "__main__":
    IntegratedPhysicsSolverApp().run()
