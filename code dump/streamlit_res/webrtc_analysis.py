import streamlit as st
from streamlit_webrtc import webrtc_streamer, ClientSettings
import av
import cv2


def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


st.title("Facial Attribute analysis software")
st.write("Web version")

client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},  # Only request video, not audio
)

webrtc_streamer(key="example",  client_settings=client_settings, callback=callback,)
