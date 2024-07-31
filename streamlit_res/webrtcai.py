"""
    Basic streamlit web rtc with facial analysis
    All rights reserved Akintola Technologies
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoProcessorBase
import av
import cv2


class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        return av.VideoFrame.from_ndarray(img, format="bgr24")


st.title("Facial Attribute Analysis Software")
st.write("Web Version")

rtc_configuration = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

webrtc_streamer(
    key="example",
    rtc_configuration=rtc_configuration,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)
