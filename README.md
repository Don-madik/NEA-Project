# NEA Physics Solver App 🧪📱

An A-Level NEA project using **Python**, **KivyMD**, and **AI** to solve physics equations and analyze images using a mobile-friendly interface.

---

## ✨ Features

- 🧮 Physics Equation Solver (with AI suggestions)
- 📷 Image Processing with OCR for extracting equations
- 🌐 Multilingual Support (via Google Translate)
- 🤖 AI-Based Predictions (e.g., acceleration from mass & force)
- 📱 Built with KivyMD for a mobile-style UI
- 🔍 Word problem parser (natural language to equations)

---

## 📁 File Structure

```
nea-physics-app/
├── main.py                # KivyMD Interface
├── backend.py             # Physics/AI logic and image processing
├── requirements.txt       # Dependencies
├── README.md              # You're reading this
├── .gitignore             # Ignore unnecessary files
```

---

## 🚀 How to Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python main.py
   ```

---

## 📦 Tech Stack

- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- OpenCV, NumPy, Pytesseract
- Google Translate API (offline fallback optional)

---

## 📌 Notes

- Designed for NEA A-Level standard
- Easily portable to Android using **Buildozer**
- Image processing works best with clean input or scanned handwritten problems

---

## 🔒 License

This project is intended for academic use. Do not redistribute without permission.

