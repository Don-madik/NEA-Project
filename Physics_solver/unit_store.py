from Physics_solver.unit_parser import UnitParser


class UnitAwareVariableStore:
    def __init__(self, known_inputs: dict):
        self.original = {}
        self.converted = {}
        self.standard_units = {
            'km': ('m', 1000), 'm': ('m', 1), 'cm': ('m', 0.01), 'mm': ('m', 0.001),
            'hr': ('s', 3600), 'min': ('s', 60), 's': ('s', 1), 'ms': ('s', 0.001),
            'g': ('kg', 0.001), 'kg': ('kg', 1), 'mg': ('kg', 0.000001), 'tonne': ('kg', 1000)
        }
        self._process_inputs(known_inputs)

    def _process_inputs(self, known_inputs):
        for var, value in known_inputs.items():
            if isinstance(value, str):
                num, unit = UnitParser.parse(value)
            else:
                num, unit = float(value), ''
            self.original[var] = (num, unit)
            converted_val, si_unit = self.convert_to_si(num, unit)
            self.converted[var] = (converted_val, si_unit)

    def convert_to_si(self, value: float, unit: str) -> tuple[float, str]:
        if unit not in self.standard_units:
            raise ValueError(f"Unsupported unit: '{unit}'")
        si_unit, multiplier = self.standard_units[unit]
        return value * multiplier, si_unit

    def get_original(self, var: str) -> tuple[float, str]:
        return self.original.get(var, (None, None))

    def get_converted(self, var: str) -> tuple[float, str]:
        return self.converted.get(var, (None, None))

    def as_dict(self) -> dict:
        return {var: val[0] for var, val in self.converted.items()}
