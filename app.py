import streamlit as st
# import cv2
import numpy as np
from PIL import Image
import requests
import google.generativeai as genai


api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set.")
    st.stop()

genai.configure(api_key=api_key)

models = genai.list_models()
model_names = [model.name for model in models]
selected_model = st.selectbox("Select a Gemini model gemini-1.5-flash for cost effective and gemini-1.5-flash for high accuracy", model_names)


st.title("עוזר למורה 🍎")
st.write("הזן את קריטריוני הציונים והעלה את עבודת הכתב של התלמיד.")

# 1. Teacher's Parameters (The Guide)
teacher_guide = st.text_area(
    "מחוון למורה",
    placeholder="תן תבחין לציון והסבר על חלוקת ציוןים (למשל: מצוין, בינוני, צריך שיפור) עבור התשובה של התלמיד.",
    height=150
)

# 2. Image Upload
uploaded_file = st.file_uploader("Upload Student's Hand-written Answer", type=["jpg", "png", "jpeg"])

if st.button("Analyze & Grade"):
    if not teacher_guide.strip() or not uploaded_file:
        st.warning("⚠️ Please provide both the grading guide and the student's work.")
    else:
        try:
            image = Image.open(uploaded_file)
            model = genai.GenerativeModel(selected_model)
            
            # Constructing the complex instruction
            full_prompt = f"""
            You are a professional teacher's assistant.
            
            ### GRADING RUBRIC / TEACHER GUIDE:
            {teacher_guide}
            
            ### TASK:
            1. Transcribe the handwritten Hebrew text from the image accurately.
            2. Evaluate the content based ONLY on the Grading Rubric provided above.
            3. Provide a breakdown of points (Excellent/Moderate/Needs Work).
            4. Suggest a final grade.
            
            Please provide the response in Hebrew, formatted clearly with Markdown headers.
            """
            
            with st.spinner("Decoding handwriting and grading..."):
                response = model.generate_content([full_prompt, image])
                
                st.subheader("Grading Report")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Analysis failed: {e}")