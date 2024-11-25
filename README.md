# ChatMeme.AI

A sarcastic meme-generating chatbot powered by Grok AI. This chatbot specializes in creating memes and jokes, with a twist - it's sarcastic by default!

## Features

- 🤖 Sarcastic responses by default
- 🎯 Meme generation with #play-it-safe tag
- 💬 Chat history tracking
- 🌙 Dark mode interface
- 🎨 Modern, responsive design

## Usage

1. Chat normally to get sarcastic responses
2. Add `#play-it-safe` to your message to get actual meme suggestions
3. View chat history in the sidebar
4. Clear history anytime with the "Clear History" button

## Development

Requirements:
- Python 3.11+
- Streamlit 1.40.1
- Requests 2.31.0

To run locally:
```bash
streamlit run app.py
```

## Environment Variables

The app uses the following environment variables:
- `GROK_API_KEY`: Your Grok AI API key

## Deployment

This app is deployed on Streamlit Cloud at: https://chatmeme-ai.streamlit.app
