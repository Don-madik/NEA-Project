import re

class NLPProcessor:
    def __init__(self):
        # Map natural language terms to variable names
        self.keyword_to_var = {
            "mass": "m",
            "acceleration": "a",
            "force": "f",
            "velocity": "v",
            "speed": "v",
            "displacement": "s",
            "time": "t",
            "energy": "e",
            "power": "p",
            "voltage": "v",
            "current": "i",
            "resistance": "r"
        }

        # Known equation templates
        self.templates = {
            frozenset(["force", "mass", "acceleration"]): "f = m * a",
            frozenset(["energy", "mass", "speed"]): "e = m * v ** 2",  # e = mc²
            frozenset(["voltage", "current", "resistance"]): "v = i * r",
            frozenset(["power", "energy", "time"]): "p = e / t"
        }

    def parse(self, sentence: str):
        sentence = sentence.lower()
        values = {}

        # Extract values like "mass is 10kg", "speed is 3e8m/s"
        for keyword, var in self.keyword_to_var.items():
            match = re.search(rf"{keyword}\s*(?:is|=)?\s*([\d\.eE+-]+(?:[a-zA-Z/^\d]*))", sentence)
            if match:
                values[var] = match.group(1).strip()

        # Detect keywords to match an equation
        detected_keywords = set(k for k in self.keyword_to_var if k in sentence)

        for keyset, equation in self.templates.items():
            if keyset.issubset(detected_keywords):
                return equation, values

        return None, values
