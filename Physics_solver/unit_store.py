from pint import UnitRegistry
from pint.errors import UndefinedUnitError
import re

ureg = UnitRegistry()

def normalize_units(value: str) -> str:
    """
    Normalize compact units like '2A' to '2 ampere', '100J' to '100 joule', etc.
    Handles scientific notation and works with upper/lower case.
    """
    value = value.strip()

    # Fix scientific notation stuck to unit, e.g., 3e8m → 3e8 m
    value = re.sub(r'(\de[+-]?\d)([a-zA-Z])', r'\1 \2', value)

    # Normalize attached compact unit symbols (upper or lower case)
    unit_mappings = {
        r'(?<=\d)([aA])\b': ' ampere',
        r'(?<=\d)([jJ])\b': ' joule',
        r'(?<=\d)([nN])\b': ' newton',
        r'(?<=\d)([wW])\b': ' watt',
        r'(?<=\d)([cC])\b': ' coulomb',
        r'(?<=\d)([vV])\b': ' volt',
        r'(?<=\d)(ohms?)\b': ' ohm'
    }

    for pattern, replacement in unit_mappings.items():
        value = re.sub(pattern, replacement, value)

    # Optional replacements for aliases
    value = value.replace("amps", "ampere").replace("amp", "ampere")
    value = value.replace("Ω", "ohm")

    return value.lower()


class UnitAwareVariableStore:
    def __init__(self, raw_inputs: dict[str, str]):
        self.raw = raw_inputs
        self.converted = {}

        for var, value in raw_inputs.items():
            try:
                cleaned = normalize_units(str(value))

                # Fallback: attach unit if value is bare number
                if re.fullmatch(r"\d+(\.\d+)?", cleaned) and var in default_units:
                    cleaned += f" {default_units[var]}"


                qty = ureg(cleaned)
                self.converted[var] = (qty.magnitude, qty.units)
            except UndefinedUnitError as e:
                raise ValueError(f"Unknown unit in variable '{var}' with value '{value}': {e}")
            except Exception as e:
                raise ValueError(f"Error processing variable '{var}' with value '{value}': {e}")

    def get_converted(self, var: str):
        return self.converted.get(var.lower(), (None, None))

    def as_dict(self):
        return {k.lower(): v for k, v in self.raw.items()}

default_units = {
    "f": "newton",
    "e": "joule",
    "p": "watt",
    "v": "volt",
    "q": "coulomb",
    "t": "second",
    "m": "kilogram",
    "a": "meter/second**2",
    "s": "meter",
    "i": "ampere",
    "r": "ohm"
}
