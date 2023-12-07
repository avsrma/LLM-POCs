# LLM-based applications
This repository contains various applications built based on Large Language Models (GPT-4, ChatGPT, and/or LLAMA). 

- Meeting Summarizer
- PDF Summarizer
- POC Builder
- Wikipedia LLM-Interface

## Meeting Summarizer
Summarizes a meeting or a conversation based on an input transcript. 

![image](Meeting%20Summarizer/data/screenshot.png)

## PDF Summarizer
Upload a PDF document and summarize it in language of choice. 

![image](PDF%20Summarizer/data/demo.png)

## POC Builder / Code Generator
Generates code for any given use-case using GPT-4. Enables users to specify their requirements in natural language, 
and creates a webapp using Streamlit. Provided an experimental solution to quickly build POCs using LLMs. 

![image](POC%20Builder/data/builder_image.png)

```
Examples of use-cases:
# Create an app using which users can upload pdf documents, that are then summarized by chatgpt
# Create a sample streamlit app with dataframe, static table, line chart, and scattarplot
# Create an app using which a user can upload pdf documents. There should be a button to get a summary. There should a text area where a user can add some natural language instructions. These instructions should be processed by AI and then used to create bar or pie charts, if the user clicks on appropriate buttons.

```

## Wikipedia LLM-Interface
A conversational knowledge bank built by combining the language capabilities of GPT-4 with the You.com search engine and Wikipedia API. This Streamlit-based webapp provides a natural language interface to Wikipedia. 
Enables users to ask questions via voice or have a multi-turn interaction via a text-based chat. 

Below is an illustration of various components: 

![image](Wikipedia%20LLM-Interface/data/arch.jpeg)

Streamlit app interface: 

![image](Wikipedia%20LLM-Interface/data/demo.png)
