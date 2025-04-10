import re

class EquationParser:
    def __init__(self, equation: str):
        # Keep the original equation with '^' replaced by '**'
        # (We assume the equation field itself should NOT contain scientific notation numbers.)
        self.original_equation = equation.strip().replace("^", "**")
        # For validation and variable extraction, we convert to lowercase.
        self.equation = self.original_equation.lower()  
        self.lhs = ""
        self.rhs = ""
        self.variables = []
        self.parse_equation()

    def validate_format(self):
        """
        Validates the equation format:
          - Contains '='
          - Both left and right sides are not empty.
          - Contains only valid characters.
        """
        if '=' not in self.equation:
            raise ValueError("Equation must contain an '=' sign.")
        lhs, rhs = self.equation.split('=', 1)
        if not lhs.strip() or not rhs.strip():
            raise ValueError("Both sides of the equation must be non-empty.")
        # Updated regex: allow '=', and '.' characters.
        if not re.match(r'^[\w\d\s\+\-\*/\(\)=\.]+$', self.equation):
            raise ValueError("Equation contains invalid characters.")

    def parse_equation(self):
        if "=" not in self.original_equation:
            raise ValueError("Equation must contain '=' symbol")
        self.lhs, self.rhs = map(str.strip, self.original_equation.split("=", 1))
        # Use an updated regex that ignores letters immediately following a digit or '.'
        # This prevents capturing the 'e' in numbers like 3e8.
        pattern = r'(?<![\d\.])[a-zA-Z_][a-zA-Z0-9_]*\b'
        matches = re.findall(pattern, self.original_equation)
        # Blacklist common function names. (You can extend this if needed.)
        blacklist = {"sin", "cos", "tan", "log", "ln", "sqrt"}
        self.variables = [var.lower() for var in matches if var.lower() not in blacklist]
