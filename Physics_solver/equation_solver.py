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
        if not self.unknown:
            self.find_unknown_variable()

        rhs = self.parser.rhs
        substituted = self.substitute_values(rhs)
        result = self.evaluate_expression(substituted)

        # Try automatic simplification
        simplified = result.to_compact()

        # 🔁 Force specific units for known physics variables
        try:
            if self.unknown.lower() in ["f", "force"]:
                simplified = result.to("newton")
            elif self.unknown.lower() in ["e", "energy"]:
                simplified = result.to("joule")
            elif self.unknown.lower() in ["p", "power"]:
                simplified = result.to("watt")
            elif self.unknown.lower() in ["v", "voltage"]:
                simplified = result.to("volt")
            elif self.unknown.lower() in ["q", "charge"]:
                simplified = result.to("coulomb")
        except Exception as e:
            pass  # fallback to .to_compact() result if unknown

        value = round(simplified.magnitude, 2)
        unit = str(simplified.units)

        return f"{self.unknown} = {value} {unit}"
