import streamlit as st
# import cv2
import numpy as np
from PIL import Image
import requests

st.write("Streamlit is also great for more traditional ML use cases like computer vision or NLP. Here's an example of edge detection using OpenCV. 👁️") 
text = st.text_input("כתוב את הטקסט מחוון")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
else:
    image = Image.open(requests.get("https://picsum.photos/200/120", stream=True).raw)
    
tab1, tab2 = st.tabs(["Detected edges", "Original"])
tab1.image(image, use_container_width =True)
tab2.image(image, use_container_width =True)