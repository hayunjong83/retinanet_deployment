import streamlit as st
import numpy as np
from PIL import Image

st.title('>>Object Detection using RetinaNet<<')
img_file_buffer = st.file_uploader("Uploading a Image")

if img_file_buffer is not None:
    submit = st.button('Start Detection')
    image = np.array(Image.open(img_file_buffer))
    placeholder = st.image(image)
    if submit:
        ret = inference.process_through_streamlit(image)
        placeholder.empty()
        placeholder = st.image(np.array(Image.open(ret)))