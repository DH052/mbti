# MBTI Daily Messages 🌟

A Streamlit web application that generates personalized daily messages based on your MBTI personality type and selected theme.

## Features

- 16 MBTI personality types support
- 4 different themes: 감성 (Emotional), 유머 (Humor), 연애 (Romance), 철학 (Philosophy)
- AI-powered message generation using OpenAI GPT-3.5
- Beautiful, responsive UI with gradient backgrounds
- Personalized cards for each MBTI type

## Live Demo

Visit the live application: [Your Streamlit App URL]

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key in `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the app: `streamlit run mbti.py`

## Deployment

This app is deployed on Streamlit Cloud. Make sure to add your OpenAI API key in the Streamlit Cloud secrets management.

## Technologies Used

- Streamlit
- OpenAI GPT-3.5
- Sentence Transformers
- LangChain
- Python-dotenv