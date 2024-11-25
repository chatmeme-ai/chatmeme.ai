import streamlit as st
import json
import requests
from datetime import datetime
import random
import os

# Page configuration
st.set_page_config(
    page_title="MemeGPT - Your Sarcastic Meme Companion",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2e2e2e;
    }
    .bot-message {
        background-color: #0e48a1;
    }
    .sidebar .element-container {
        background-color: #2e2e2e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def generate_response(prompt, play_it_safe=False):
    # Get API key from environment variable or use the hardcoded one for development
    API_KEY = os.getenv("GROK_API_KEY", "xai-lzlQOcSbR7B4CdJH3anxBEt0bUf9BmA1ByOR6ZDxV5kpY54PvLqXdB9VFGH0yU96X3iiHu8yJ5wqARAq")
    API_URL = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Sarcastic responses for non-play-it-safe mode
    sarcastic_responses = [
        "Oh, you want me to do something? How about... no. Try adding #play-it-safe if you're serious.",
        "Sorry, I only speak in memes, and I don't see a #play-it-safe tag. Try again!",
        "Error 404: Cooperation not found. Have you tried using #play-it-safe?",
        "I'm as helpful as a chocolate teapot right now. Use #play-it-safe for actual help.",
        "I'm currently in 'maximum sass' mode. Use #play-it-safe to switch to 'actually helpful' mode."
    ]

    if not play_it_safe:
        return random.choice(sarcastic_responses)

    # Define the system message based on whether it's play_it_safe mode
    system_message = """You are MemeGPT, a specialized AI that excels in creating memes and jokes. 
    Your responses should be creative, funny, and meme-worthy. Focus on generating humorous content 
    and meme suggestions. Always format your responses with proper spacing and structure. If suggesting
    a meme, provide a clear format like:
    
    Meme Format:
    [Description of the meme template]
    Top text: [Your suggestion]
    Bottom text: [Your suggestion]
    
    Or for modern memes:
    Caption: [Your suggestion]
    Image: [Description of the image to use]"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    data = {
        "messages": messages,
        "model": "grok-beta",
        "stream": False,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Grok AI: {str(e)}")
        return "Sorry, I'm having trouble connecting to my meme-generating powers right now. Try again later!"
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return "Oops! Something went wrong with my meme circuits. Please try again!"

# Sidebar with chat history
with st.sidebar:
    st.header("💬 Chat History")
    if st.button("Clear History", key="clear"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.experimental_rerun()
    
    for chat in st.session_state.chat_history:
        with st.container():
            st.text(f"🕒 {chat['timestamp']}")
            st.text(f"💭 {chat['query'][:50]}...")

# Main chat interface
st.title("🤖 MemeGPT - Your Sarcastic Meme Companion")
st.markdown("""
    Welcome to MemeGPT! I'm your sarcastic meme-generating companion.
    - Use `#play-it-safe` at the end of your message for actual meme generation
    - Without `#play-it-safe`, expect maximum sass!
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind? (Use #play-it-safe for memes)"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Check if #play-it-safe is in the prompt
    play_it_safe = "#play-it-safe" in prompt.lower()
    
    # Generate response
    response = generate_response(prompt, play_it_safe)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Add to sidebar chat history
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        "timestamp": timestamp,
        "query": prompt
    })
