import azure.cognitiveservices.speech as speechsdk
from config import AZURE_SPEECH_KEY, AZURE_REGION, VOICE_MAPPING
import os


def synthesize_speech(text, output_path, voice_name="storyteller"):
    """使用Azure TTS为整个故事合成语音"""
    from config import AZURE_SPEECH_KEY, AZURE_REGION, VOICE_MAPPING

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)

    # 使用配置中映射的讲故事者音色
    selected_voice = VOICE_MAPPING.get(voice_name)
    if selected_voice:
        speech_config.speech_synthesis_voice_name = selected_voice

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise Exception(f"语音合成失败: {result.reason}")
    print(f"[INFO] 语音合成完成: {output_path}")
    return output_path