import re
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView

# --- Simple Equation Parsing and Solving Functions ---

def extract_variables(equation: str) -> list:
    """
    Extracts single-letter variables from an equation.
    For example, from "F = m * a" returns ['F', 'm', 'a'].
    """
    return list(set(re.findall(r'\b[a-zA-Z]\b', equation)))

def solve_equation(equation: str, knowns: dict) -> tuple:
    """
    Solves an equation for the unknown variable.
    Expects an equation of the form "X = expression" where X is the unknown variable.
    The knowns dictionary should have keys for the known variables.
    
    Returns a tuple (unknown_variable, computed_value).
    Raises ValueError if the conditions are not met.
    """
    # Split into LHS and RHS
    try:
        lhs, rhs = equation.split("=")
    except ValueError:
        raise ValueError("Equation must contain exactly one '=' sign.")
    lhs = lhs.strip()
    rhs = rhs.strip()
    variables = set(re.findall(r'\b[a-zA-Z]\b', equation))
    
    # Determine which variable is unknown: it must be the one missing from knowns
    unknowns = [v for v in variables if v not in knowns]
    if len(unknowns) != 1:
        raise ValueError("Exactly one variable must be unknown (left blank) to solve for.")
    unknown = unknowns[0]
    
    # Build an expression from RHS by replacing known variable names with their values.
    expr = rhs
    for var, value in knowns.items():
        # Ensure to replace only whole-word occurrences.
        expr = re.sub(r'\b' + var + r'\b', str(value), expr)
        
    try:
        computed_value = eval(expr)
    except Exception as e:
        raise ValueError("Error evaluating the expression: " + str(e))
    return unknown, computed_value

# --- KivyMD Application ---

class PhysicsSolverApp(MDApp):
    def build(self):
        self.title = "Physics Equation Solver"
        main_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Card to group our interface elements
        card = MDCard(orientation='vertical', padding=20, spacing=20)
        
        # Text field to input the equation
        self.equation_input = MDTextField(
            hint_text="Enter equation (e.g., F = m * a)",
            size_hint=(1, None),
            height=40
        )
        card.add_widget(self.equation_input)
        
        # Button to generate dynamic input fields for variables
        gen_fields_button = MDRaisedButton(
            text="Generate Fields",
            size_hint=(1, None),
            height=40,
            on_release=self.generate_fields
        )
        card.add_widget(gen_fields_button)
        
        # ScrollView to hold the dynamic variable input fields
        self.scroll = MDScrollView(size_hint=(1, None), height=200)
        self.fields_box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        # Bind the minimum_height so the container expands with its children
        self.fields_box.bind(minimum_height=self.fields_box.setter('height'))
        self.scroll.add_widget(self.fields_box)
        card.add_widget(self.scroll)
        
        # Button to solve the equation
        solve_button = MDRaisedButton(
            text="Solve Equation",
            size_hint=(1, None),
            height=40,
            on_release=self.solve_equation_ui
        )
        card.add_widget(solve_button)
        
        # Label to display the result or error messages
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
        Generates dynamic text fields for each variable in the entered equation.
        Instructs the user to fill in known values and leave exactly one field blank.
        """
        eq = self.equation_input.text.strip()
        if not eq or "=" not in eq:
            self.result_label.text = "Please enter a valid equation containing '='."
            return
        
        # Clear any previously generated fields
        self.fields_box.clear_widgets()
        # Extract variables from the equation
        self.variables = extract_variables(eq)
        for var in self.variables:
            tf = MDTextField(
                hint_text=f"Enter value for {var} (leave blank if unknown)",
                size_hint=(1, None),
                height=40
            )
            # Store the variable name with the field for later retrieval
            tf.variable_name = var
            self.fields_box.add_widget(tf)
        self.result_label.text = ("Fields generated. "
                                  "Fill in values (as numbers) for known variables and leave one blank.")

    def solve_equation_ui(self, instance):
        """
        Reads the values from the dynamic fields, validates input, and calls solve_equation.
        Displays the result or any error messages.
        """
        eq = self.equation_input.text.strip()
        if not eq or "=" not in eq:
            self.result_label.text = "Please enter a valid equation containing '='."
            return
        
        # Gather known variable values
        knowns = {}
        unknown_count = 0
        for child in self.fields_box.children:
            # Each child is an MDTextField with an attached variable name
            var = child.variable_name
            val = child.text.strip()
            if val == "":
                unknown_count += 1
            else:
                try:
                    # Convert the input to a float
                    knowns[var] = float(val)
                except Exception:
                    self.result_label.text = f"Invalid numeric value for '{var}': {val}"
                    return
        
        if unknown_count != 1:
            self.result_label.text = "Exactly one variable must be left blank to solve for."
            return
        
        try:
            unknown, result = solve_equation(eq, knowns)
            self.result_label.text = f"Solved: {unknown} = {result}"
        except Exception as e:
            self.result_label.text = "Error: " + str(e)

if __name__ == "__main__":
    PhysicsSolverApp().run()
