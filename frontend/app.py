import streamlit as st
import requests
import pandas as pd

API_URL = "http://backend:8000"

st.set_page_config(page_title="Records App", page_icon="📊")
st.title("📊 Score Records")

st.subheader("➕ Add New Record(name and score)")

name = st.text_input("Name")
score = st.number_input("Score", min_value=0, max_value=100, step=1)

if st.button("Add Record"):
    if name:
        response = requests.post(
            f"{API_URL}/records",
            json={"name": name, "score": int(score)}
        )
        if response.status_code == 200:
            st.success("Record added successfully!")
        else:
            st.error("Failed to add record")
    else:
        st.warning("Please enter a name")

st.divider()

st.subheader("📋 Existing Records")

try:
    response = requests.get(f"{API_URL}/records")
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records yet")
    else:
        st.error("Could not fetch records")
except Exception as e:
    st.error("Backend not running. Start FastAPI first.")
