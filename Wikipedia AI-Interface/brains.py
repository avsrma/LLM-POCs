import json
import os
import openai

from dotenv import load_dotenv


def chatgpt(content, model="gpt-4-32k-deployment"):
    load_dotenv(".env")

    openai.api_type = "azure"
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        engine=model,
        messages=content,
        temperature=0.4,  # control randomness of token generation
        max_tokens=300,
        top_p=0.95,  # control randomness of token generation
        frequency_penalty=0,  # decrease likelihood of repeating the exact same text in a response
        presence_penalty=0,  # increase likelihood of introducing new topics in a response
        stop=None
    )

    output = response['choices'][0]['message']['content']

    return output
