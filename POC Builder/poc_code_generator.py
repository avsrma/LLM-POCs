import os
import re
import subprocess
from sys import executable

import openai
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

def update_message(current_conversation, role, content):
    message = {"role": role, "content": content}
    current_conversation.append(message)

def chatgpt(content):
    with open("initial_system_prompt.txt", "r", encoding="utf-8") as f:
        initial_system_prompt = f.read()

    conversation = [{"role": "system",
                     "content": initial_system_prompt}]
    update_message(conversation, "user", content)

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        engine="gpt-4-32k-deployment",
        messages=conversation,
        temperature=0.2,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    output = response['choices'][0]['message']['content']

    return output


def launch_poc(text):
    pattern = r"```\n(.+?)```\n"
    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) == 0:
        print("No matches with first pattern")
        pattern = r"```python\n(.+?)```\n"
        matches = re.findall(pattern, text, re.DOTALL)

    python_code = matches[0]
    with open("poc.py", "w", encoding="utf-8") as f:
        f.write(python_code)

    print("Written code to poc.py")
    os.system("python -m streamlit run poc.py")


def app():
    st.title("POC Builder")
    st.subheader("Build POCs using ChatGPT!")

    text = st.text_area("Specify POC credentials",
                        placeholder="Be as detailed or brief as you want",
                        help="Creates a POC using ChatGPT based on specifications provided by you!",
                        height=280)

    if st.button("Generate POC"):
        output = chatgpt(text)
        if "output" not in st.session_state:
            st.session_state["output"] = output
            with open("log.txt", "w", encoding="utf-8") as f:
                f.write(st.session_state["output"])
            st.write(st.session_state["output"])

    if st.button("Launch POC"):
        launch_poc(st.session_state["output"])


if __name__ == '__main__':
    app()

# Sample suggestions:
# Create an app using which users can upload pdf documents, that are then summarized by chatgpt
# Create a sample streamlit app with dataframe, static table, line chart, and scattarplot
# Create an app using which a user can upload pdf documents. There should be a button to get a summary. There should a text area where a user can add some natural language instructions. These instructions should be processed by AI and then used to create bar or pie charts, if the user clicks on appropriate buttons.
