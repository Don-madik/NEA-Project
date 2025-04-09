import re

class EquationParser:
    def __init__(self, equation: str):
        # Normalize: lowercase and replace '^' with '**'
        self.original_equation = equation.strip().replace("^", "**").lower()
        self.lhs = ""
        self.rhs = ""
        self.variables = []
        self.parse_equation()

    def parse_equation(self):
        if "=" not in self.original_equation:
            raise ValueError("Equation must contain '=' symbol")

        self.lhs, self.rhs = map(str.strip, self.original_equation.split("=", 1))

        # Extract variable names using regex (identifiers only)
        matches = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", self.original_equation)

        # Exclude function names like 'sin', 'cos', etc. if needed (you can customize this)
        blacklist = {"sin", "cos", "tan", "log", "ln", "sqrt"}
        self.variables = [var.lower() for var in matches if var.lower() not in blacklist and var.lower() != "e"]

