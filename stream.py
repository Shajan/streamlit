import time
import streamlit as st

def stream_data(n):
  for i in range(n):
    yield f"{i} "
    time.sleep(0.02) 

st.write_stream(stream_data(100))
