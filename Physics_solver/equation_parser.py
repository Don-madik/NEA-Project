import re

class EquationParser:
    def __init__(self, equation: str):
        # Normalize: lowercase and replace '^' with '**'
        self.original_equation = equation.strip().replace("^", "**").lower()
        self.equation = self.original_equation  # For validation compatibility
        self.lhs = ""
        self.rhs = ""
        self.variables = []
        self.parse_equation()
    def validate_format(self):
        """
        Validates the equation format:
        - Must contain '='
        - Both sides must not be empty
        - Variables must be valid identifiers
        """
        if '=' not in self.equation:
            raise ValueError("Equation must contain an '=' sign.")

        lhs, rhs = self.equation.split('=', 1)
        lhs, rhs = lhs.strip(), rhs.strip()

        if not lhs or not rhs:
            raise ValueError("Equation must have non-empty left and right sides.")

        # Simple check for invalid characters
        if not re.match(r'^[\w\d\s\+\-\*/\^\=\(\)]+$', self.equation.replace("**", "^")):
            raise ValueError("Equation contains invalid characters.")

        # Extract variables and validate them
        variables = re.findall(r'\b[a-zA-Z_]\w*\b', self.equation)
        if not variables:
            raise ValueError("No valid variables found in the equation.")

        for var in variables:
            if var[0].isdigit():
                raise ValueError(f"Invalid variable name: '{var}' cannot start with a number.")
    def parse_equation(self):
        if "=" not in self.original_equation:
            raise ValueError("Equation must contain '=' symbol")

        self.lhs, self.rhs = map(str.strip, self.original_equation.split("=", 1))

        # Extract variable names using regex (identifiers only)
        matches = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", self.original_equation)

        # Exclude function names like 'sin', 'cos', etc. if needed (you can customize this)
        blacklist = {"sin", "cos", "tan", "log", "ln", "sqrt"}
        self.variables = [var.lower() for var in matches if var.lower() not in blacklist and var.lower() != "e"]

