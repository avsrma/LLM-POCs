import os
import openai
import tiktoken

from dotenv import load_dotenv

import streamlit as st


def summarize(content: str, model="davinci"):

    load_dotenv(".env")

    openai.api_type = "azure"
    openai.api_base = os.environ.get("OPENAI_API_BASE") 
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    system = "Provide a summary of the following meeting Transcript:\n\n"

    prompt = system + content

    response = openai.Completion.create(engine=model, 
                                        prompt=prompt, 
                                        max_tokens=300
                                        )

    output = response['choices'][0]['text']


    if model == "chat":
        response = openai.ChatCompletion.create(
                    engine=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides concise meeting summaries."},
                        {"role": "user", "content": system + content}
                    ]
                )

        output = response['choices'][0]['message']['content']

    return st.write(f"{output}")


def token_count(content):
    davinci = "text-davinci-003"
    chatgpt = "gpt-3.5-turbo"
    gpt4 = "gpt-4"

    enc = tiktoken.encoding_for_model(davinci)
    
    return len(enc.encode(content))


if __name__ == "__main__":

    input_text = st.text_area("Summarize conversations", 
                            placeholder="Provide a conversation (eg. a meeting transcript)", 
                            help="Paste a transcript of an interview or a meeting.", 
                            height=280)

    st.code("Token count: " + str(token_count(input_text)))

    if st.button("Summarize"): 
        summarize(input_text)
    
