from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdf2image
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found. Please check your .env file.")
else:
    # Configure Google Generative AI with the API key
    genai.configure(api_key=api_key)

# Function to get response from Gemini model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to 'gemini-1.5-flash'
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process PDF and convert it to images
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
