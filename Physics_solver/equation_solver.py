import logging
from Physics_solver.unit_store import UnitAwareVariableStore
from pint import UnitRegistry
from pint.errors import DimensionalityError
import re

# Initialize UnitRegistry
ureg = UnitRegistry()

# Define the voltage dimension and unit using Pint.
ureg.define("[voltage] = [mass] * [length]**2 / [time]**3 / [current]")
ureg.define("volt = 1.0 * [voltage]")
# unit_store.py (after `ureg = UnitRegistry()`):
ureg.define("A = ampere")  # so "2A" parses as "2 * ampere"
ureg.define("amps = ampere")
ureg.define("ohm = ohm")   # if needed as an alias
ureg.define("ohms = ohm")
ureg.define("Ω = ohm")
ureg.define("kg = kilogram")
ureg.define("J = joule")
ureg.define("N = newton")
ureg.define("W = watt")
ureg.define("C = coulomb")
# Optional: print definition to verify
print(ureg["volt"])  # Should print something like "volt = [voltage]"

class EquationSolver:
    def __init__(self, parser, variable_store: UnitAwareVariableStore):
        self.parser = parser
        self.store = variable_store
        self.knowns = variable_store.as_dict()  # Known variable magnitudes in SI units.
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
        Replaces variables with their numeric values (with units) using safe regex substitution.
        This prevents partial replacement inside longer unit names.
        """
        for var, (value, unit) in self.store.converted.items():
            replacement = f"({value} * {unit})"
            expression = re.sub(rf'\b{re.escape(var)}\b', replacement, expression)
        return expression

    def evaluate_expression(self, expression: str):
        """
        Evaluates a unit expression and simplifies it.
        """
        try:
            result = ureg.parse_expression(expression).to_base_units()
            simplified = result.to_compact()  # Use compact notation when possible.
            return simplified
        except Exception as e:
            raise ValueError(f"Error evaluating expression with units: {expression} → {str(e)}")

    def solve_equation(self) -> str:
        try:
            # Identify the unknown variable if not already found.
            if not self.unknown:
                self.find_unknown_variable()

            # Substitute known values into the right-hand side of the equation.
            rhs = self.parser.rhs
            substituted = self.substitute_values(rhs)
            result = self.evaluate_expression(substituted)

            # Simplify the result to base units and then compact them.
            simplified = result.to_base_units().to_compact()

            # Force preferred units based on the unknown variable
            preferred_units = {
                "f": "newton",
                "e": "joule",
                "p": "watt",
                "v": "volt",       # For voltage, now defined via [voltage]
                "q": "coulomb",
                "t": "second",
                "m": "kilogram",
                "a": "meter / second ** 2",
                "s": "meter",      # displacement
                "i": "ampere",
                "r": "ohm"
            }

            var = self.unknown.lower()
            forced_unit = preferred_units.get(var)
            if forced_unit:
                try:
                    simplified = result.to(forced_unit)
                except Exception:
                    try:
                        simplified = result.to_reduced_units().to(forced_unit)
                    except Exception:
                        simplified = result  # Fallback if conversion fails

            # Optional backup: check dimension fallback if needed.
            dimensional_fallbacks = {
                "[force]": "newton",
                "[energy]": "joule",
                "[power]": "watt",
                "[voltage]": "volt",
                "[current]": "ampere",
                "[resistance]": "ohm",
                "[mass]": "kilogram"
            }

            try:
                for dim, unit in dimensional_fallbacks.items():
                    if simplified.check(dim):
                        simplified = simplified.to(unit)
                        break
            except DimensionalityError:
                pass

            value = round(simplified.magnitude, 2)
            unit = str(simplified.units)
            return f"{self.unknown} = {value} {unit}"

        except Exception as e:
            logging.error(f"PhysicsAI Error: {e}")
            return f"Error: {str(e)}"
