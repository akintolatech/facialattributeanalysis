import streamlit as st
import cv2
import numpy as np

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
        matrix = np.ones(frame.shape, dtype="uint8") * 50
        b_frame = cv2.add(frame, matrix)

        # Display the processed frame in Streamlit
        stframe.image(b_frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

st.title("Facial Attribute Analysis Software")
st.write("Local Version")

video_capture()
