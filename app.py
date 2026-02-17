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


st.write("Streamlit is also great for more traditional ML use cases like computer vision or NLP. Here's an example of edge detection using OpenCV. 👁️") 
user_input = st.text_input("כתוב את הטקסט מחוון")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
else:
    image = Image.open(requests.get("https://picsum.photos/200/120", stream=True).raw)

st.image(image, use_container_width=True)


# Button to send
if st.button("שלח את הטקסט ל-Gemini"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text before sending.")
    else:
        try:
            # ---------------------------
            # SEND TO GEMINI
            # ---------------------------
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_input)

            # Display Gemini's response
            st.subheader("Gemini's Response:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")