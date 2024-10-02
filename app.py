import os
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from fpdf import FPDF
import pyttsx3

# Set the path to the Tesseract executable (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
OUTPUT_FOLDER = 'output/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure the necessary directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Noise removal function
def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

# Perform OCR and return text
def extract_text_from_image(image_path, lang='eng'):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = noise_removal(img_gray)
    processed_image_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
    cv2.imwrite(processed_image_path, processed_img)
    text = pytesseract.image_to_string(processed_img, lang=lang)
    return text, processed_image_path

# Convert PDF to images and extract text
def extract_text_from_pdf(pdf_path, lang='eng'):
    images = convert_from_path(pdf_path)
    full_text = ""
    for i, image in enumerate(images):
        image_path = os.path.join(UPLOAD_FOLDER, f"page_{i}.jpg")
        image.save(image_path, 'JPEG')
        text, _ = extract_text_from_image(image_path, lang)
        full_text += text + "\n\n"
    return full_text

# Text-to-speech (TTS)
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, os.path.join(OUTPUT_FOLDER, 'output_audio.mp3'))
    engine.runAndWait()

# Create PDF from extracted text
def create_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, text)
    pdf.output(output_path)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    lang = request.form.get('language', 'eng')

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Perform OCR (image or PDF)
        if filename.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path, lang)
        else:
            extracted_text, processed_image_path = extract_text_from_image(file_path, lang)

        # Save as txt and pdf
        text_output_path = os.path.join(OUTPUT_FOLDER, f"{filename.rsplit('.', 1)[0]}.txt")
        pdf_output_path = os.path.join(OUTPUT_FOLDER, f"{filename.rsplit('.', 1)[0]}.pdf")

        with open(text_output_path, 'w') as f:
            f.write(extracted_text)

        create_pdf(extracted_text, pdf_output_path)
        text_to_speech(extracted_text)

        return render_template('result.html', text=extracted_text, 
                               text_file_url=url_for('output_file', filename=os.path.basename(text_output_path)),
                               pdf_file_url=url_for('output_file', filename=os.path.basename(pdf_output_path)),
                               audio_file_url=url_for('output_file', filename='output_audio.mp3'))

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
