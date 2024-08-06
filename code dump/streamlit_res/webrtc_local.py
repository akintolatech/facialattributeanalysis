import streamlit as st
import cv2
import numpy as np

"""
    Basic streamlit web rtc with facial analysis
    All rights reserved Akintola Technologies
"""


# Define a function to capture video from the webcam
def video_capture():
    cap = cv2.VideoCapture(0)  # Capture video from the default webcam (index 0)

    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video")
            break

        # Apply some processing to the frame (example: brighten the image)
        matrix = np.ones(frame.shape, dtype="uint8") * 100
        b_frame = cv2.add(frame, matrix)

        # Display the processed frame in Streamlit
        stframe.image(b_frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


st.title("Facial Attribute Analysis Software")
st.write("Local Version")

# Initialize session state for capturing
if 'capturing' not in st.session_state:
    st.session_state['capturing'] = False

# Define start and stop buttons
if st.button('Start'):
    st.session_state['capturing'] = True
    video_capture()

if st.button('Stop'):
    st.session_state['capturing'] = False
