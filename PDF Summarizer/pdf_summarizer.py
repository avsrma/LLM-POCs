import os
import openai
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfFileReader

load_dotenv()


def update_message(current_conversation, role, content):
    message = {"role": role, "content": content}
    current_conversation.append(message)


def chatgpt(system_prompt, user_prompt):
    conversation = [{"role": "system",
                     "content": system_prompt},
                    {"role": "user",
                     "content": user_prompt}]

    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        engine="gpt-4-32k-deployment",
        messages=conversation,
        temperature=0.7,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0
    )

    output = response["choices"][0]["message"]["content"]
    return output


def summarize_pdf(file):
    with st.spinner('Summarizing PDF...'):
        pdf = PdfFileReader(file)
        text = ""
        for page in range(pdf.getNumPages()):
            text += pdf.getPage(page).extractText()

        summary = chatgpt("Summarize the following text in German:", text)
        return summary


st.set_page_config(page_title="PDF Summarizer")

st.title("PDF Summarizer using GPT-4")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    summary = summarize_pdf(uploaded_file)
    st.write("Summary:")
    st.write(summary)
