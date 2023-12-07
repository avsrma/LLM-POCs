import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

def fix_typos_in_wake_word(sentence, wake_words, wake_word):
    words = sentence.split()  # split the sentence into words
    
    for i in range(len(words)):
        if words[i] in wake_words:
            words[i] = wake_word  # replace the given word with the key word
    formatted_sentence = ' '.join(words)  # join the words back into a sentence

    return formatted_sentence


def is_user_talking_to_me(transcript, wake_words):
    words = transcript.split()  # split the sentence into words
    for word in words:
        if word in wake_words:
            return True
    return False

def get_wikipedia_context(page):
    url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page + '/bare'

    access_token = os.environ.get("WIKI_ACCESS_TOKEN")
    app_name = os.environ.get("APP_NAME")
    email = os.environ.get("EMAIL")

    headers = {'Authorization': f'Bearer {access_token}', 
               'User-Agent': f'{app_name} ({email})'
               }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        overview = data["extract"]
        return overview
    else:
        return ""

def get_wikipage_title(search_param):
    api_key = os.environ.get("YOUDOTCOM_API_KEY")

    search_config = 'Provide the title to the most relevant wikipedia page for this query. Reply with only the title. If no page is found reply with "None": '
    query = search_config + search_param

    url = f"https://api.you.com/youchat?api_key={api_key}&query={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Process the response data
        return data['text']
    else:
        # Handle the error
        return "None"

def update_conversation(current_conversation, role, content):
    if role == "user":
        wikpage_title = get_wikipage_title(search_param=content)
        if wikpage_title != "None":
            system_context = get_wikipedia_context(page=wikpage_title)
            updated_system_prompt = {"role": "system", "content": system_context}
            current_conversation.append(updated_system_prompt)

    message = {"role": role, "content": content}
    current_conversation.append(message)
