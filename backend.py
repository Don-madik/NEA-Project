import logging
import numpy as np

from Physics_solver.unit_store import UnitAwareVariableStore
from Physics_solver.equation_parser import EquationParser
from Physics_solver.equation_solver import EquationSolver
from Physics_solver.NLP_processing import NLPProcessor  # <-- External NLP module

# Setup logging
logging.basicConfig(
    filename='backend.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PhysicsAI:
    def __init__(self):
        self.nlp = NLPProcessor()
        self.weights = np.random.rand(5)

    def solve_equation(self, equation: str, knowns: dict) -> str:
        """
        Solve the equation using the EquationSolver pipeline.
        """
        try:
            parser = EquationParser(equation)
            parser.validate_format()

            store = UnitAwareVariableStore(knowns)
            solver = EquationSolver(parser, store)
            result = solver.solve_equation()

            return result
        except Exception as e:
            logging.error(f"PhysicsAI Error: {e}")
            return f"Error: {str(e)}"

    def solve_from_natural_language(self, sentence: str) -> str:
        """
        Solve a physics problem from a natural language sentence.
        """
        try:
            equation, knowns = self.nlp.parse(sentence)

            if not equation:
                return "Sorry, I couldn't understand the equation from your input."

            return self.solve_equation(equation, knowns)
        except Exception as e:
            logging.error(f"NLP Solve Error: {e}")
            return f"Error: {str(e)}"

    def predict_missing_value(self, params):
        try:
            if "force" in params and "mass" in params:
                return f"Predicted Acceleration: {params['force'] / params['mass']} m/s^2"
            elif "velocity" in params and "time" in params:
                return f"Predicted Acceleration: {params['velocity'] / params['time']} m/s^2"
            else:
                return "Error: Not enough data for prediction"
        except Exception as e:
            logging.error(f"AI Prediction Error: {e}")
            return "Error: Could not compute prediction"

    def classify_equation_type(self, text):
        if "force" in text and "mass" in text and "acceleration" in text:
            return "Newton's Second Law: F = ma"
        elif "voltage" in text and "current" in text and "resistance" in text:
            return "Ohm's Law: V = IR"
        elif "energy" in text and "mass" in text:
            return "Einstein's Energy Equation: E = mc^2"
        else:
            return "Unknown Equation Type"
