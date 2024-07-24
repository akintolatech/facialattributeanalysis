import streamlit as st
import pandas as pd
import numpy as np
import random


from streamlit_webrtc import webrtc_streamer
import av
import cv2

# without flags
# def callback(frame):
#     img = frame.to_ndarray(format="bgr24")
#     img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
#     return av.VideoFrame.from_ndarray(img, format="bgr24")
#

st.write("Facial Recognition App")
st.write({
    "first col": [3, 5, 6, 7],
    "second col": [3, 5, 6, 7],

})

webrtc_streamer(key="example")

emotion_counts = {
    "neutral": random.randint(45, 876),
    "angry": random.randint(45, 876),
    "fear": random.randint(45, 876),
    "disgust": random.randint(45, 876),
    "happy": random.randint(45, 876),
    "sad": random.randint(45, 876),
    "surprise": random.randint(45, 876)
}

st.line_chart(emotion_counts)

map_data = pd.DataFrame(
    np.random.randn(50, 2) / [50, 50] + [9.8965, 8.8583],  # Centered around Jos,
    columns=['lat', 'lon'])

# st.map(map_data)

# buttons
st.button("Start Live Analysis", type="primary")

# select boxes
option = st.selectbox(
    "Language Reference",
    ("English", "Spanish"))

st.write(f"You selected {option}")

# video
video_file = open("../test5.mp4", "rb")
video_bytes = video_file.read()

st.video(video_bytes)
