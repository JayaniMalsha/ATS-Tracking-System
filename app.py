from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdf2image
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styles
st.markdown("""
<style>
    .main-header {
        font-family: 'Helvetica', sans-serif;
        font-size: 36px;
        font-weight: bold;
        color: #4B56D2;
        text-align: center;
        margin-bottom: 20px;
        padding-top: 20px;
    }
    .sub-header {
        font-size: 24px;
        color: #472D2D;
        margin-bottom: 15px;
    }
    .stButton > button {
        background-color: #4B56D2;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .result-container {
        border-left: 5px solid #4B56D2;
        padding-left: 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 15px;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
        background-color: rgba(40, 167, 69, 0.1);
        text-align: center;
        padding: 10px;
        border-radius: 5px;
    }
    .stProgress > div > div {
        background-color: #4B56D2;
    }
    .stTextInput, .stTextArea, .stFileUploader {
        border-radius: 8px;
        border: 2px solid #4B56D2;
        padding: 10px;
    }
    .stButton > button:hover {
        background-color: #3c48b0;
        cursor: pointer;
    }
    a:hover {
        color: #4B56D2;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<div class="main-header">📝 ATS Resume Expert</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <p style="font-size: 18px; color: #6c757d;">
        Maximize your job application success with AI-powered resume analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 18px; color: #6c757d; font-weight: bold; padding: 10px;">
    🚀 Get started by uploading your resume and pasting the job description to receive an in-depth analysis!
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("🔑 API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# PDF processing
def input_pdf_setup(file):
    file_bytes = file.getvalue()
    images = pdf2image.convert_from_bytes(file_bytes)
    img_byte_arr = io.BytesIO()
    images[0].save(img_byte_arr, format='JPEG')
    encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode()
    return [{"mime_type": "image/jpeg", "data": encoded_img}]

# Gemini API call
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# === SECTION: Upload Resume ===
st.markdown('<div class="sub-header">📄 Upload Your Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.markdown('<div class="success-message">✅ Resume uploaded successfully!</div>', unsafe_allow_html=True)
    try:
        preview = pdf2image.convert_from_bytes(uploaded_file.getvalue(), first_page=1, last_page=1)
        st.image(preview[0], width=250, caption="Resume Preview")
    except Exception as e:
        st.warning(f"Preview error: {e}")

# === SECTION: Enter Job Description ===
st.markdown('<div class="sub-header">📋 Enter Job Description</div>', unsafe_allow_html=True)
input_text = st.text_area(
    "Paste the job description here (e.g., Responsibilities, Qualifications, etc.):",
    height=250,
    key="input",
    help="Include the job title, responsibilities, qualifications, and key skills required"
)

# === SECTION: Analysis Options ===
st.markdown('<div class="sub-header">🔍 Analysis Options</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    submit1 = st.button("📊 Detailed Analysis")
with col2:
    submit3 = st.button("🎯 Match Percentage")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Analyze the resume against the job description and provide:

1. Overall assessment (strong match, moderate match, or needs improvement)
2. Key strengths
3. Gaps or missing experience
4. Skills match
5. Actionable resume improvement suggestions

Use clear section headings.
"""

input_prompt3 = """
You are an advanced ATS scanner. Analyze the resume vs job description:

1. MATCH PERCENTAGE: Show a percentage match score
2. KEYWORDS:
   - Present in resume (with examples)
   - Missing (suggest adding)
3. SKILLS ALIGNMENT: Match vs job needs
4. RECOMMENDATIONS to boost match rate

Start with MATCH PERCENTAGE at the top.
"""

# === SECTION: Results ===
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📈 Results")

if submit1 or submit3:
    if uploaded_file and input_text:
        with st.spinner("🔄 Analyzing your resume..."):
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)

            try:
                pdf_content = input_pdf_setup(uploaded_file)
                prompt = input_prompt1 if submit1 else input_prompt3
                response = get_gemini_response(prompt, pdf_content, input_text)

                st.markdown("## 📝 Analysis Result" if submit1 else "## 🎯 Match Analysis")
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Analysis",
                    data=response,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume.")
        if not input_text:
            st.warning("⚠️ Please enter the job description.")

st.markdown('</div>', unsafe_allow_html=True)

# === FOOTER ===
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 20px;">
    <p style="font-size: 16px; font-weight: bold; color: #4B56D2;">ATS Resume Expert</p>
    <a href="https://yourwebsite.com/privacy" style="color: #6c757d;">Privacy Policy</a> | 
    <a href="https://yourwebsite.com/terms" style="color: #6c757d;">Terms of Service</a>
</div>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("### 💡 Tips for Success")
    st.markdown("""
    **Resume Tips:**
    - Tailor your resume for each job
    - Use job description keywords
    - Quantify achievements
    - Keep formatting simple

    **Common ATS Issues:**
    - Complex designs
    - Graphics/tables
    - Headers/footers

    **To Improve Match:**
    - Use industry terms
    - Add missing skills/certs
    - Mirror job language
    """)
