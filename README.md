# ATS Resume Expert

ATS Resume Expert is a web application designed to help job seekers evaluate their resumes against a given job description using an AI-powered model. The application uses Google’s Gemini AI to analyze the uploaded resume and provides insights, such as the match percentage and suggestions for improvement based on ATS (Applicant Tracking System) functionality.

## Features

- **Resume Evaluation**: Upload a resume (PDF) and input a job description. The app evaluates the resume against the job description, providing a professional evaluation of how well the candidate's profile matches the role.
- **ATS Compatibility**: The app can simulate an ATS scanner to evaluate resumes for key skills and keywords. It shows the match percentage and identifies missing keywords.
- **AI-Powered Responses**: Powered by Google’s Gemini AI model, the app offers detailed, natural language feedback on resumes and job descriptions.

## Technologies Used

- **Streamlit** - For building the interactive web interface.
- **Python** - Programming language for the backend logic.
- **Google Generative AI (Gemini)** - For processing and generating resume evaluations and responses.
- **pdf2image** - To convert PDF resumes to images for processing.
- **Pillow (PIL)** - For image manipulation and conversion to byte format.
- **Base64** - For encoding images to base64 format.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Pip to install Python packages.

To run this project locally, you will need to install the necessary dependencies.

### Dependencies

```bash
pip install streamlit google-generativeai pdf2image Pillow python-dotenv
```
# Setup
## 1. Clone the Repository:

```bash
git clone <my-repository-url>
cd <project-folder>
```
## 2. Set up Google API Key:

- Create a Google Cloud project if you don't already have one.
- SEnable the Gemini API and get your API Key from Google Cloud.
- Create a .env file in the project root and add the following:

  ```bash
  GOOGLE_API_KEY=your_api_key_here
  ```
## 3. Running the App:
1. Create a Virtual Environment

2.After setting up the API key and installing the dependencies, you can run the Streamlit app locally:
 ```bash
streamlit run app.py
 ```
The app will open in your browser, and you can start uploading resumes and inputting job descriptions.

# Usage

1. Enter Job Description:

- You can paste the job description in the provided text box.

2. Upload Your Resume:

- Use the file uploader to upload your resume (PDF format).

3. Generate Results:

- Click on "Tell Me About the Resume" to get a detailed evaluation of the resume and its match to the job description.
- Click on "Percentage match" to receive the percentage of how well your resume matches the job description, along with missing keywords and final thoughts.

# Example:
- Job Description Input
- Uploaded Resume
The resume should highlight skills such as Python, machine learning, and data analytics.
-  Result:
The AI will evaluate the resume and show a response indicating strengths, weaknesses, and how well it matches the job description.

# Error Handling

- No API Key Found: Make sure the .env file is correctly configured with your Google API key.
- Model Deprecation Error: If the Gemini model is deprecated, make sure you are using an updated model like gemini-1.5-flash.
- File Upload Issues: Ensure the file uploaded is in PDF format. The app will only process PDF resumes.
