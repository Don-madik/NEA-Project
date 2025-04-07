from Physics_solver.unit_store import UnitAwareVariableStore

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

    def get_unknown_unit(self) -> str:
        if not self.unknown:
            raise Exception("Unknown variable not determined yet.")
        return self.unknown_unit

    def substitute_values(self, expression: str) -> str:
        for var, value in self.knowns.items():
            expression = expression.replace(var, str(value))
        return expression

    def evaluate_expression(self, expression: str) -> float:
        try:
            result = eval(expression)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expression} → {str(e)}")
        return result

    def solve_equation(self) -> str:
        if not self.unknown:
            self.find_unknown_variable()

        rhs = self.parser.rhs
        substituted = self.substitute_values(rhs)
        result = self.evaluate_expression(substituted)
        result = round(result, 2)
        unit = self.get_unknown_unit()
        return f"{self.unknown} = {result} {unit}"
