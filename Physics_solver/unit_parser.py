import re

class UnitParser:
    @staticmethod
    def parse(value_with_unit: str) -> tuple[float, str]:
        value_with_unit = value_with_unit.strip()
        match = re.match(r"([0-9.+-eE]+)\s*([a-zA-Z*/^·0-9]+)", value_with_unit)
        if not match:
            raise ValueError(f"Invalid value+unit format: '{value_with_unit}'")
        value = float(match.group(1))
        unit = match.group(2).strip()
        return value, unit
