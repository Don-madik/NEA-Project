import logging
from Physics_solver.unit_store import UnitAwareVariableStore
from pint import UnitRegistry
import re
ureg = UnitRegistry()

class EquationSolver:
    def __init__(self, parser, variable_store: UnitAwareVariableStore):
        self.parser = parser
        self.store = variable_store
        self.knowns = variable_store.as_dict()
        self.unknown = None
        self.unknowns = []
        self.unknown_unit = None

    def get_known_variables(self) -> list[str]:
        return [var for var in self.parser.variables if var in self.knowns]

    def get_missing_variables(self) -> list[str]:
        return [var for var in self.parser.variables if var not in self.knowns]

    def find_unknown_variable(self) -> str:
        missing = self.get_missing_variables()
        if len(missing) == 0:
            raise ValueError("No unknown variable found. All variables have known values.")
        elif len(missing) == 1:
            self.unknown = missing[0]
            self.unknown_unit = self.store.get_converted(self.unknown)[1]
            return self.unknown
        else:
            self.unknowns = missing
            raise ValueError(f"Multiple unknown variables found: {missing}. Cannot solve yet.")

    def substitute_values(self, expression: str) -> str:
        """
        Replaces variables with values (with units) using safe regex substitution.
        Prevents partial replacements inside unit names like 'meter'.
        """
        for var, (value, unit) in self.store.converted.items():
            replacement = f"({value} * {unit})"
            # Only replace whole variable words
            expression = re.sub(rf'\b{re.escape(var)}\b', replacement, expression)
        return expression



    def evaluate_expression(self, expression: str):
        """
        Evaluates a unit expression and simplifies to standard units like N or J.
        """
        try:
            result = ureg.parse_expression(expression).to_base_units()
            simplified = result.to_compact()  # ← best for unit names like N, J, etc.
            return simplified
        except Exception as e:
            raise ValueError(f"Error evaluating expression with units: {expression} → {str(e)}")



    def solve_equation(self) -> str:
        try:
            if not self.unknown:
                self.find_unknown_variable()

            rhs = self.parser.rhs
            substituted = self.substitute_values(rhs)
            result = self.evaluate_expression(substituted)

            # Simplify unit to base/compact first
            simplified = result.to_base_units().to_compact()

            # Step 1: Force unit based on variable name
            preferred_units = {
                "f": "newton",
                "e": "joule",
                "p": "watt",
                "v": "volt",
                "q": "coulomb",
                "t": "second",
                "m": "kilogram",
                "a": "meter / second ** 2",
                "s": "meter",     # displacement
                "i": "ampere",
                "r": "ohm"
            }

            try:
                var = self.unknown.lower()
                if var in preferred_units:
                    simplified = simplified.to(preferred_units[var])
            except Exception:
                pass  # fallback to compact unit

            # Step 2: (optional) Fallback match on unit expression
            unit_fallback_map = {
                "kilogram * meter / second ** 2": "newton",
                "kilogram * meter ** 2 / second ** 2": "joule",
                "kilogram * meter ** 2 / second ** 3": "watt"
            }
            unit_str = str(simplified.units)

            if unit_str in unit_fallback_map:
                try:
                    simplified = simplified.to(unit_fallback_map[unit_str])
                except Exception:
                    pass  # fallback silently

            value = round(simplified.magnitude, 2)
            unit = str(simplified.units)
            return f"{self.unknown} = {value} {unit}"

        except Exception as e:
            logging.error(f"PhysicsAI Error: {e}")
            return f"Error: {str(e)}"
