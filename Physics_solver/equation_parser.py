import re

class EquationParser:
    def __init__(self, equation: str):
        self.equation = equation
        self.lhs = ""
        self.rhs = ""
        self.variables = []

    def validate_format(self) -> bool:
        if '=' not in self.equation:
            raise ValueError("Equation must contain an '=' sign.")
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^=(). ")
        for char in self.equation:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character detected in equation: '{char}'")
        return True

    def parse(self) -> tuple[str, str]:
        lhs, rhs = self.equation.split('=')
        self.lhs = lhs.strip()
        self.rhs = rhs.strip()
        return self.lhs, self.rhs

    def extract_variables(self) -> list[str]:
        tokens = re.findall(r'\b[a-zA-Z]\b', self.equation)
        self.variables = list(set(tokens))
        return self.variables
