# -*- coding: utf-8 -*-
import whisper

def whisper_mp3(file_path):
    whisper_model = whisper.load_model("base")
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

    # detect the spoken language
    _, probs = whisper_model.detect_language(mel)
    detected_lan = max(probs, key=probs.get)

    options = whisper.DecodingOptions(
        fp16=False, prompt="这里是简体字" if detected_lan == "zh" else ""
    )
    result = whisper.decode(whisper_model, mel, options)

    return result.text
