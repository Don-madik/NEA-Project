import cv2
import numpy as np
import pytesseract
import logging
import math
import re
from googletrans import Translator
from Physics_solver.unit_store import UnitAwareVariableStore
from Physics_solver.equation_parser import EquationParser
from Physics_solver.equation_solver import EquationSolver


# Setup logging
logging.basicConfig(filename='backend.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
translator = Translator()

class ImageProcessor:
    """Handles image processing for extracting physics equations from images."""
    def __init__(self):
        self.image = None

    def load_image(self, image_path):
        try:
            self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if self.image is None:
                raise ValueError("Failed to load image")
            logging.info(f"Image loaded successfully: {image_path}")
            return self.image
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {e}")
            return None

    def apply_thresholding(self):
        try:
            if self.image is None:
                raise ValueError("No image loaded")
            processed = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
            logging.info("Adaptive thresholding applied successfully")
            return processed
        except Exception as e:
            logging.error(f"Error in thresholding: {e}")
            return None

    def detect_edges(self):
        try:
            if self.image is None:
                raise ValueError("No image loaded")
            edges = cv2.Canny(self.image, 50, 150)
            logging.info("Edge detection applied successfully")
            return edges
        except Exception as e:
            logging.error(f"Error in edge detection: {e}")
            return None

    def remove_noise(self):
        try:
            if self.image is None:
                raise ValueError("No image loaded")
            blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
            logging.info("Noise removal applied successfully")
            return blurred
        except Exception as e:
            logging.error(f"Error in noise removal: {e}")
            return None

    def extract_regions_of_interest(self):
        try:
            if self.image is None:
                raise ValueError("No image loaded")
            processed = self.apply_thresholding()
            contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            bounding_boxes = [cv2.boundingRect(c) for c in contours]
            logging.info(f"Extracted {len(bounding_boxes)} regions of interest")
            return bounding_boxes
        except Exception as e:
            logging.error(f"Error extracting regions of interest: {e}")
            return None


class PhysicsAI:
    def __init__(self):
        self.weights = np.random.rand(5)

    def solve_equation(self, equation: str, knowns: dict) -> str:
        """
        Solve the equation using the EquationSolver pipeline.
        """
        try:
            # Step 1: Parse the equation to identify variables
            parser = EquationParser(equation)
            parser.validate_format()
            parser.parse()
            parser.extract_variables()

            # Step 2: Store the knowns (user input)
            store = UnitAwareVariableStore(knowns)

            # Step 3: Solve the equation using the solver
            solver = EquationSolver(parser, store)
            result = solver.solve_equation()

            return result
        except Exception as e:
            logging.error(f"PhysicsAI Error: {e}")
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


class AdvancedPhysicsSolvers:
    def heat_transfer(self, mass, specific_heat, temp_change):
        return f"Heat Energy: {mass * specific_heat * temp_change} J"

    def bernoulli_equation(self, pressure1, velocity1, height1, pressure2, velocity2, height2):
        g = 9.81
        lhs = pressure1 + (0.5 * velocity1 ** 2) + (g * height1)
        rhs = pressure2 + (0.5 * velocity2 ** 2) + (g * height2)
        return f"Bernoulli's Equation: {lhs} = {rhs}"

    def relativity_time_dilation(self, velocity):
        c = 3.0e8
        gamma = 1 / math.sqrt(1 - (velocity ** 2 / c ** 2))
        return f"Time Dilation Factor: {gamma}"

    def coulombs_law(self, q1, q2, r):
        k = 8.99e9
        force = (k * q1 * q2) / (r ** 2)
        return f"Electric Force: {force} N"


class NLPProcessor:
    def parse_input(self, user_input):
        try:
            user_input = user_input.lower()
            match = re.search(r'find the (acceleration|force) when (\w+) is (\d+) and (\w+) is (\d+)', user_input)
            if match:
                variable, val1, val1_num, val2, val2_num = match.groups()
                return f"{val1}={val1_num}, {val2}={val2_num}, {variable}?"
            return "Error: Could not parse input"
        except Exception as e:
            logging.error(f"Error parsing natural language input {user_input}: {e}")
            return "Error: Could not process input"


class TranslatorModule:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, target_language):
        try:
            translated = self.translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            logging.error(f"Error translating text {text}: {e}")
            return "Error: Could not translate"
