
import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Customer Support Chatbot for Voltedge",page_icon="🤖")


st.markdown("""
<style>
.banner {
    background: linear-gradient(90deg, #4aaaaa, #000000);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 35px;
    font-weight: bold;
    margin-bottom: 25px;
}
</style>

<div class="banner">
   Customer Support Chatbot for Voltedge<br>
(Powered by LN AI Academy)
</div>
""", unsafe_allow_html=True)


st.sidebar.image("flag.jpg")

st.sidebar.title("About us")
st.sidebar.text("We are developing Agentic Chatbot for Company Voltedge using langgraph in LN AI Academy")

st.sidebar.title("About Project")
st.sidebar.text("This bot handles customer query as real agent")

st.sidebar.title("Contact us")
st.sidebar.text("+919958966311")


# FastAPI endpoint
API_URL = "https://chatbotapi-1-5nnb.onrender.com/chat"

# Unique session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Apna message likhein..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "message": prompt,
                        "session_id": st.session_state.session_id
                    },
                    timeout=120
                )

                response.raise_for_status()
                data = response.json()

                # Apne API response ke according key badlein
                answer = data["answer"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")

            except (KeyError, ValueError):
                st.error(
                    "Response format check karein: "
                    + str(response.text)
                )
