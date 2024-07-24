import streamlit as st
from streamlit_webrtc import webrtc_streamer, ClientSettings

st.title("My first Streamlit app")
st.write("Hello, world")

client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},  # Only request video, not audio
)

webrtc_streamer(key="example", client_settings=client_settings)