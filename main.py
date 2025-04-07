from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image
from backend import ImageProcessor, PhysicsAI
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
import re

# Function to extract variables (single-letter) from the equation
def extract_variables(equation: str) -> list:
    return re.findall(r'\b[a-zA-Z]\b', equation)  # Finds single-letter variables


class NEAInterface(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        main_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title_label = MDLabel(text="NEA AI-Powered Physics & Image Processor", halign='center', theme_text_color="Custom", text_color=(0, 0, 0, 1), font_style="H5")
        main_layout.add_widget(title_label)

        # Image Processing Section
        img_section = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), height=300)
        img_section.add_widget(MDLabel(text="Image Processing", font_style="H6", halign="center"))

        self.image_display = Image(size_hint=(1, 0.6))
        img_section.add_widget(self.image_display)

        upload_button = MDRaisedButton(text="Upload Image", size_hint=(1, None), on_release=self.open_file_chooser)
        img_section.add_widget(upload_button)

        main_layout.add_widget(img_section)

        # Physics Equation Solver Section
        physics_section = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), height=350)
        physics_section.add_widget(MDLabel(text="Physics Equation Solver", font_style="H6", halign="center"))

        self.equation_input = MDTextField(hint_text="Enter physics equation", size_hint=(1, None), height=40)
        physics_section.add_widget(self.equation_input)

        solve_button = MDRaisedButton(text="Solve Equation", size_hint=(1, None), on_release=self.call_solve_equation)
        physics_section.add_widget(solve_button)

        self.result_label = MDLabel(text="Result:", theme_text_color="Secondary", size_hint_y=None, halign="left")

        scroll_view = MDScrollView(size_hint=(1, 0.4))
        scroll_view.add_widget(self.result_label)
        physics_section.add_widget(scroll_view)

        main_layout.add_widget(physics_section)

        return main_layout

    def open_file_chooser(self, instance):
        self.file_manager = MDFileManager(select_path=self.display_image, exit_manager=self.close_file_manager)
        self.file_manager.show('/')

    def close_file_manager(self, *args):
        self.file_manager.close()

    def display_image(self, image_path):
        self.close_file_manager()
        processor = ImageProcessor()
        processor.load_image(image_path)
        tex = processor.apply_thresholding()
        self.image_display.texture = tex

    def call_solve_equation(self, instance):
        print("Button clicked!")
        equation = self.equation_input.text.strip()

        # Step 1: Extract variables from the equation
        variables = extract_variables(equation)

        # Step 2: Create input fields dynamically for missing variables
        knowns = {}
        for var in variables:
            # Dynamically check if an input field exists for each variable
            input_field = getattr(self, f"{var}_input", None)
            if input_field:  # If input field exists
                user_input = input_field.text.strip()
                if user_input:
                    knowns[var] = user_input

        if not knowns:
            self.result_label.text = "Please enter values for all missing variables."
            return

        # Step 3: Pass the knowns into PhysicsAI to solve the equation
        ai = PhysicsAI()
        result = ai.solve_equation(equation, knowns)

        self.result_label.text = f"Result:\n{result}"

if __name__ == "__main__":
    NEAInterface().run()
