import streamlit as st
from streamlit_webrtc import webrtc_streamer, ClientSettings

st.title("Facial Attribute analysis software")
st.write("Web version")

client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},  # Only request video, not audio
)

webrtc_streamer(key="example", client_settings=client_settings)