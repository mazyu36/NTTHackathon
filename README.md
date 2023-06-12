# AlexaとChatGPTで会話させる
NTT OpenAIハッカソン（2023/6/1-2）で作成したAlexa←→Chat GPTで会話させるプログラムを格納

# ディレクトリ構成

```bash
.
├── README.md # このファイル
├── architecture # アーキテクチャ図を格納
│   ├── architecture_1st.drawio.svg
│   └── architecture_2nd.drawio.svg
├── conversation_with_openai.py # プログラム本体
└── work # 試行錯誤時に作成したプログラム
    ├── speak_test.py
    └── speech_recognition.py
```


# アーキテクチャ
以下のAzureのサービスを使用
* Azure Cognitive Services Speech to Text：Alexaの音声をテキストに変換。OpenAIの入力に使用する。
* OpenAI Service：Alexaの発話内容（テキスト）を受け取り、応答（テキスト）を返す。
* Azure Cognitive Services Text to Speech：OpenAIの出力（テキスト）を音声に変換。Alexaへの呼びかけに使用する。

## 初回呼びかけ
Alexa固定の文字列をText to Speechに渡して音声に変換する。

![初回の呼びかけ](architecture/architecture_1st.drawio.svg)


## 2回目以降
Alexaの発話内容をテキストに変換。OpenAIに渡して応答を受け取り、音声に変換した上で回答する。

![2回目以降](architecture/architecture_2nd.drawio.svg)