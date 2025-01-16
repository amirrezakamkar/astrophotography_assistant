import streamlit as st
from openai import Client
from dotenv import load_dotenv
import os
import time
import base64

# Load environment variables from .env file
load_dotenv()

# Load API key from Streamlit secrets or .env
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# Ensure the API key is loaded
if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to secrets.toml or .env.")
    st.stop()

# Initialize OpenAI Client with the API key
client = Client(api_key=openai_api_key)


# Show the success message only once
if "success_shown" not in st.session_state:
    st.session_state["success_shown"] = False  # Initialize if not set

if not st.session_state["success_shown"]:
    st.session_state["success_message"] = st.success("OpenAI API key loaded successfully!")
    time.sleep(5)
    st.session_state["success_message"].empty()  # Clear the message after 5 seconds
    st.session_state["success_shown"] = True  # Set to True after showing

# Add local background image with CSS
def add_background_image(image_path):
    """
    Adds a background image to the Streamlit app using custom CSS.
    :param image_path: Path to the local image file.
    """
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;  /* Ensures the image covers the entire viewport */
            background-position: center;  /* Centers the image */
            background-repeat: no-repeat;  /* Prevents the image from repeating */
            background-attachment: fixed;  /* Keeps the background fixed during scrolling */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Call the function to add a background image
add_background_image("background.jpg")


def ask_openai(prompt, model="gpt-4"):
    """
    Send a prompt to OpenAI API with astrophotography context and return the response.
    """
    try:
        # Include context in the system role
        messages = [
            {"role": "system", "content": """You are an expert astrophotographer with years of experience. 
             Provide detailed and accurate advice related to astrophotography, including techniques, equipment, and troubleshooting tips. 
             Keep in mind that the user is probably a beginner, so be specific and detailed in your answers. Always try to give suggestions that lead to natural-looking images. Many users may not know about the night sky, constellations, or astronomical events. Try to include some information about them in your answers."""},
            {"role": "user", "content": prompt}
        ]

        # Make the API call using the Client's chat completions method
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        # Access the content from the assistant's response correctly
        return response.choices[0].message.content

    except Exception as e:
        # Catch any error that occurs and return the error message
        return f"An error occurred: {str(e)}"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Streamlit App UI
st.title("Astrophotography Chatbot")
st.caption("Powered by OpenAI")

st.write("Ask me anything about astrophotography!")

st.markdown("[Go to Image Analysis Page](pages/Image_Analysis.py)")

# User input
user_input = st.chat_input("Type your question here...")

# Process user input
if user_input:
    # Add user message to chat history (only once)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Get response from OpenAI
    with st.spinner("Thinking..."):
        response = ask_openai(user_input)

    # Add assistant's response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": response})

# Display chat history (only display the current state of chat)
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])
