# Updated Streamlit App
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8019/execute"

st.title("🩺 Doctor Appointment System")

user_id = st.text_input("Enter your ID number:", "")
query = st.text_area("Enter your query:", "Can you check if a dentist is available tomorrow at 10 AM?")

if st.button("Submit Query"):
    if user_id and query:
        try:
            payload = {
                "id_number": int(user_id),
                "messages": [
                    {"role": "user", "content": query}
                ]
            }
            response = requests.post(API_URL, json=payload, verify=False)
            if response.status_code == 200:
                st.success("Response Received:")
                response_data = response.json()["messages"]
                for msg in response_data:
                    if msg["role"] == "assistant":
                        st.markdown(f"**Assistant:** {msg['content']}")
                    elif msg["role"] == "user":
                        st.markdown(f"**You:** {msg['content']}")
            else:
                st.error(f"Error {response.status_code}: Could not process the request.")
        except Exception as e:
            st.error(f"Exception occurred: {e}")
    else:
        st.warning("Please enter both ID and query.")