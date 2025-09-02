import streamlit as st
import google.generativeai as genai

# --- Configuration ---
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")

# --- API Key Configuration ---
# For deployment, use Streamlit's secrets management.
# Add a secret in your app's settings named "GEMINI_API_KEY"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("🚨 GEMINI_API_KEY not found. Please add it to your Streamlit secrets!")
    st.stop()

# --- Model Setup ---
# Using a modern, efficient model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Streamlit App ---
st.title("🤖 My Personal AI Assistant")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from the chat input box at the bottom
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response and display it
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Use streaming for a better user experience
            response_stream = model.generate_content(prompt, stream=True)
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌") # Typing cursor effect
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "Sorry, I ran into a problem."
            
    # Add the final bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})