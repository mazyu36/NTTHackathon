import openai
import os
import azure.cognitiveservices.speech as speechsdk

# Note: The openai-python library support for Azure OpenAI is in preview.
openai.api_type = "azure"
openai.api_base = "https://matsudayui.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and
    # "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'),
        region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "ja-JP"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    # TODO 長い音声を認識する場合は .start_continuous_recognition_async を使う。
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(
            speech_recognition_result.no_match_details))
        return None
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print(
            "Speech Recognition canceled: {}".format(
                cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(
                "Error details: {}".format(
                    cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
        return None


def get_from_openai(text):
    response = openai.ChatCompletion.create(engine="gpt-35-turbo",
                                            messages=[{"role": "system",
                                                       "content": "You are an AI assistant that helps people find information."},
                                                      {"role": "user",
                                                       "content": text},
                                                      {"role": "assistant",
                                                       "content": ""}],
                                            temperature=0.7,
                                            max_tokens=800,
                                            top_p=0.95,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=None)

    answer_text = response["choices"][0]["message"]["content"]
    print(answer_text)
    return answer_text


# 音声からテキストを抽出
text = recognize_from_microphone()

# 音声で抽出したテキストをOpenAIにリクエストして結果を取得
openai_response = get_from_openai(text)
