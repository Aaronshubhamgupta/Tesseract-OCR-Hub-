import streamlit as st
import cv2
import pytesseract
import numpy as np
import pyperclip  # Required for copying text to clipboard
import pyttsx3  # Required for text-to-speech

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the pyttsx3 engine (initialize it outside the function)
engine = None

def initialize_engine():
    global engine
    engine = pyttsx3.init()

def perform_ocr(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(gray_image)
    return text

def text_to_speech(text):
    global engine
    # Ensure engine is initialized before using it
    if engine is None:
        initialize_engine()
    
    # Use pyttsx3 to convert text to speech
    engine.say(text)
    engine.runAndWait()

def main():
    # Title of the Streamlit app
    st.title("Tesseract OCR Hub")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the uploaded image using OpenCV
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Perform OCR
        text = perform_ocr(image)

        # Display the uploaded image
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Display the extracted text
        st.header("Extracted Text:")
        st.write(text)

        # Button to copy text to clipboard
        if st.button("Copy Text"):
            pyperclip.copy(text)
            st.success("Text copied to clipboard!")

        # Button to read text aloud
        if st.button("Read Text Aloud"):
            text_to_speech(text)
            st.success("Text read aloud!")

if __name__ == "__main__":
    main()

