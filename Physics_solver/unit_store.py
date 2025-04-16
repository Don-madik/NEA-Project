# unit_store.py
import pint
import re
# Create a Pint unit registry.
ureg = pint.UnitRegistry()

class UnitAwareVariableStore:
    def __init__(self, known_inputs: dict):
        self.original = {}
        self.converted = {}
        self._process_inputs(known_inputs)

    def _process_inputs(self, known_inputs):
        """
        Processes each known input by parsing with Pint.
        Each value is converted to its SI base form.
        """
        for var, value in known_inputs.items():
            try:
                var = var.lower()  # Normalize variable names to lowercase.
                # Insert a space between a digit and the unit 'A' if it's not part of scientific notation.
                value = re.sub(r"(?<![eE])(\d)(A)\b", r"\1 \2", value)
                # Insert a space between a digit and 'ohm' (case insensitive) if not part of scientific notation.
                value = re.sub(r"(?<![eE])(\d)(ohm)\b", r"\1 \2", value, flags=re.IGNORECASE)
                # Parse the string (e.g. "100 N", "9.8 m/s^2") using Pint.
                q = ureg(value)
                self.original[var] = q
                # Convert to SI base units (e.g., newton, kilogram, meter, second, etc.).
                q_si = q.to_base_units()
                # Save as a tuple (magnitude, unit) for clarity.
                self.converted[var] = (q_si.magnitude, str(q_si.units))
            except Exception as e:
                raise ValueError(f"Error processing variable '{var}' with value '{value}': {e}")


    def get_original(self, var: str):
        """Returns the original Pint quantity for a variable."""
        return self.original.get(var, None)

    def get_converted(self, var: str):
        """Returns a tuple (magnitude, SI unit) for the given variable."""
        return self.converted.get(var, (None, None))
    
    def as_dict(self) -> dict:
        """
        Returns a dictionary mapping variable names to their SI magnitudes.
        This can be used by your equation solver.
        """
        return {var: val[0] for var, val in self.converted.items()}
