import time
import torchaudio
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN


class TextToSpeechModel():
    def __init__(self) -> None:
        self.tacotron2 = Tacotron2.from_hparams(source="padmalcom/tts-tacotron2-german", savedir="../models/text_to_speech")
        self.hifi_gan = HIFIGAN.from_hparams(source="padmalcom/tts-hifigan-german", savedir="../models/text_to_speech")

    def tts_generator(self, input_text, use_gpu=False, device="cpu") -> str:
        print("input_text ", input_text)
        st = time.time()

        mel_output, mel_length, alignment = self.tacotron2.encode_text(input_text)
        waveforms = self.hifi_gan.decode_batch(mel_output)
        out_file_path = f"saved_audio/speech{time.time()}.wav"
        torchaudio.save(out_file_path, waveforms.squeeze(1), 22050)

        et = time.time()
        print("Time:", et - st)

        return out_file_path

tts = TextToSpeechModel()
tts.tts_generator("Das ist random Nachricht.")

# def voice_generator(input_text):
#     tts = TextToSpeechModel()
#     return tts.tts_generator(input_text)

# print(voice_generator("some text randoom"))