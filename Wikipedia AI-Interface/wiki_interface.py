import base64
import logging

from brains import chatgpt
from session_manager import update_conversation, fix_typos_in_wake_word
from speech_module.transcription import LiveTranscription

import streamlit as st
from streamlit_chat import message

# from speech_module.tts_model import TextToSpeechModel


def autoplay_audio(file_path="speech.wav", idx=0):
    print("Playing audio file: ", file_path)
    with open(file_path, "rb") as binary_audio:
        audio_bytes = binary_audio.read()

    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)


def get_text():
    # message(transcript, avatar_style="adventurer", seed="Trouble")
    input_text = st.text_input("Schreiben Sie Ihre Anfrage oder starten Sie die Live-Spracherkennung", "", key="input")
    return input_text


def pipeline(engine, logger):
    with open("system_prompt.txt", "r") as f:
        system_prompt = f.read()

    conversation = [{"role": "system",
                     "content": system_prompt}]

    if "assistant" not in st.session_state:
        st.session_state["assistant"] = []

    if "user" not in st.session_state:
        st.session_state["user"] = []

    message("Hallöchen! Ich bin der wikipedia-Bot. Wie kann ich Ihnen helfen?")
    user_input = get_text()
    logger.info("Received text input from user")

    if user_input:
        # message(user_input, avatar_style="adventurer", seed="Trouble")
        update_conversation(conversation, "user", user_input)
        st.session_state.user.append(user_input)

        response = chatgpt(content=conversation, model=engine)
        logger.info("Generated response using GPT-4")
        update_conversation(conversation, "assistant", response)
        st.session_state.assistant.append(response)
        # message(response, is_user=True, avatar_style="adventurer", seed="Whiskers")

    if st.button("Speak"):
        print("Live speech recognition...")
        with st.spinner("Starting speech recognition"):
            logger.info("Starting live speech recognition")
            live_transcription = LiveTranscription()
            live_transcription.start()
            logger.info("Successfully started live transcription...")

        try:
            with st.spinner("Listening..."):
                transcript, sample_length, inference_time, confidence = live_transcription.get_last_text()
            logger.info("Transcription received.")
            print(f"{sample_length:.3f}s\t{inference_time:.3f}s\t{confidence}\t{transcript}")

            st.session_state.user.append(transcript)
            # message(transcript, avatar_style="adventurer", seed="Trouble")

            update_conversation(conversation, "user", transcript)
            with st.spinner("Generating response"):
                response = chatgpt(content=conversation)
            logger.info("Generated response using GPT-4")

            # print("Prompt invoked: ", conversation)
            update_conversation(conversation, "assistant", response)
            st.session_state.assistant.append(response)
            # message(response, is_user=True, avatar_style="adventurer", seed="Whiskers")

            # speech_file = voice.tts_generator(response)
            # autoplay_audio(speech_file)
            with st.spinner("Stopping live transcription"):
                live_transcription.stop()
                logger.info("Stopped live speech recognition")

        except KeyboardInterrupt:
            live_transcription.stop()
            logger.info("Keyboard interrupt. Stopped live speech recognition.")
            exit()

    if st.session_state["assistant"]:
        for i in range(len(st.session_state["assistant"])):
            message(st.session_state["user"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["assistant"][i], key=str(i))
            logger.info("Written messages to streamlit chat")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.info('Starting Logger')

    # tts = TextToSpeechModel()
    # logger.info("TTS model loaded.")

    pipeline(engine="gpt-4-32k-deployment", logger=logger)
