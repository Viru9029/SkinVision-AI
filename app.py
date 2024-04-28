import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL certificate verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_cos_env_variable(name, mandatory):
    """Check for the presence of an environment variable."""
    if os.environ.get(name) is None and mandatory:
        print(f"Variable {name} not found!")
        exit(1)
    elif os.environ.get(name) is None and not mandatory:
        return ""
    return os.environ.get(name)


load_dotenv()


API_KEY = check_cos_env_variable("GOOGLE_API_KEY", True)
genai.configure(api_key=API_KEY)


def get_gemini_repsonse(input, image, prompt):
    """Function to load Google Gemini Pro Vision API And get response."""
    model = genai.GenerativeModel('gemini-pro-vision')
    gemini_response = model.generate_content([input, image[0], prompt])

    return gemini_response.text


def input_image_setup(uploaded_file):
    """Setup input image."""
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# initialize our streamlit app
st.set_page_config(page_title="SkinVision-AI", page_icon="🔬")

# Add logo with reduced size
st.image("SkinVision-AI.jpg", use_column_width=True)

# Center the header
st.markdown("<h1 style='text-align: center;'>SkinVision-AI</h1>", unsafe_allow_html=True)

# Adjust info details with reduced text size
st.markdown("""
    <p style='text-align: justify; font-size: 14px;'>
    SkinVision-AI is a groundbreaking Streamlit app leveraging the power of AI to swiftly identify various skin diseases with just the upload of an image depicting the affected area. By simply uploading the image and clicking on the "Proceed to Detection" button, you can swiftly obtain accurate diagnoses. The app not only detects the disease but also furnishes comprehensive information including symptoms, precautions, and available treatments. With its user-friendly interface and efficient functionality, SkinVision-AI streamlines the process of identifying skin conditions, offering users valuable insights into their dermatological health.
    </p>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Proceed to detection")

input_prompt = """
Act as dermatologist who can accurately identify skin conditions from images. 
Additionally, provide detailed information on symptoms, precautions, and remedies associated with the 
detected disease to assist dermatologists and patients in understanding and managing the condition effectively.
"""

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image before proceeding to detection.")
    else:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_repsonse(input_prompt, image_data, input_prompt)
        st.subheader("The Response is")
        st.write(response)
