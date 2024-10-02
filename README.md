# ocr_extraction

About the Project: OCR and Text-to-Speech Assistive Tool
This project is a web-based application designed to assist users in extracting text from images using Optical Character Recognition (OCR) and converting that text into speech using Text-to-Speech (TTS) technology. Built with Python and Flask, the tool provides a user-friendly interface where users can:

Upload image files (e.g., scanned documents or photos of text).
Extract text from the images using Tesseract OCR.
Convert the extracted text into audio (MP3 format) for easy listening.
Download both the processed text and the audio file for offline use.
The application features user authentication, allowing users to securely manage their uploaded documents and access their personalized content. This tool is particularly useful for visually impaired individuals, providing them with an accessible way to convert written content into audible speech.

Technologies and Libraries Used:
Python: Core programming language for the application.
Flask: Web framework for building the application interface and handling requests.
Tesseract-OCR: Open-source OCR engine for text extraction from images.
OpenCV: Image processing library to prepare and clean images before OCR.
Pyttsx3: Python text-to-speech library for generating audio files from text.
Werkzeug: Utility library used for password hashing and security.
FPDF: Python library for generating PDF files (optional enhancement).
Bootstrap: CSS framework used for creating a responsive and attractive UI.
This tool is particularly useful in industries like education and accessibility, helping visually impaired individuals access textual content in audio form, thereby fostering inclusivity and equal access to information.
