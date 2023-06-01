import openai
import os
import azure.cognitiveservices.speech as speechsdk

# Note: The openai-python library support for Azure OpenAI is in preview.
openai.api_type = "azure"
openai.api_base = "https://matsudayui.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")


# チャットの初期状態を設定
def initialize_chat():
    # モデルのID（ChatGPTのIDを使用）
    model_id = 'gpt-35-turbo'

    # 初期状態のチャット履歴
    chat_history = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]

    return model_id, chat_history

# ユーザーからの入力を処理し、モデルに送信して応答を生成する


def generate_response(user_input, model_id, chat_history):
    # チャット履歴にユーザーの入力を追加
    chat_history.append({'role': 'user', 'content': user_input})

    # print(chat_history)

    # OpenAI APIを使用して応答を生成
    response = openai.ChatCompletion.create(
        engine=model_id,
        messages=chat_history,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    # 応答からモデルの生成結果を抽出
    model_response = response['choices'][0]['message']['content']

    # TODO Responseのトークン数の上限超過時の考慮が必要。

    # チャット履歴にモデルの応答を追加
    chat_history.append({'role': 'assistant', 'content': model_response})
    return model_response


def speech_to_text():
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


def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'),
        region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = 'ja-JP-AoiNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(
            "Speech synthesis canceled: {}".format(
                cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(
                    "Error details: {}".format(
                        cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


# メインの会話ループ
def chat_loop():
    # チャットの初期化
    model_id, chat_history = initialize_chat()

    while True:
        # ユーザーからの入力を取得
        user_input = speech_to_text()

        # ユーザーの入力が 'exit' だった場合はループを終了
        if user_input.lower() == 'exit':
            break

        # モデルによる応答の生成
        response = generate_response(user_input, model_id, chat_history)

        print("Assistant:", response)
        text_to_speech(response)


# メインの実行部分
if __name__ == '__main__':
    chat_loop()
