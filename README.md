# Emotion Model Based Chatbot : 감정 모델 기반의 챗봇
"감정 모델 기반의 챗봇 구현 연구"  논문을 통해 감정 모델 기반의 챗봇을 구현하였다.
감정 모델 기반 챗봇은 감정 분류기와 의도 분석기로 이루어져 있고, 인공 감정 엔진과 챗봇이 상호 작용함으로써 사용자의 감정적 대화에 챗봇이 감정적으로 응답할 수 있다. 감정 분류기는 응답에 해당하는 대화의 감정을 미리 분류한다. 그리고 의도 분석기는 나이브 베이즈 분류 알고리즘을 통해 학습된 대화로 문장의 의도를 분석한다.
챗봇 프로그램은 빠른 구현을 위해 파이썬 언어를 사용하여 구현하였다. 구문 분석에는 NLTK 파이썬 패키지를 사용했다. 그리고 화면 UI는  tkinter 파이썬 패키지를 사용하여 구현하였고 대화 데이터베이스는 SQLite를 사용하였다. 또한 감정 분석기는 NLTK를 사용하여 Multinomial 나이브 베이즈 분류 알고리즘을 직접 구현하여 사용했으며, 의도 분석기는 문장의 감정 학습을 위해 Tensorflow와 GloVe을 사용하여 구현하였다. 인공 감정 엔진은 간단한 인공감정 모델의 구현을 참고하여 파이썬으로 새롭게 구현하였다. 

실행파일
- EmotionalChatbot.py

실행에 필요한 패키지
- Pillow 5.0.0
- SpeechRecognition 3.8.1
- gTTS 1.2.2
- matplotlib 2.1.1
- nltk 3.2.1

참고자료
- 대화 데이터 및 의도 데이터 참고(https://dialogflow.com)
- 의도 분석 알고리즘 참고(https://chatbotslife.com/text-classification-using-algorithms-e4d50dcba45)
- 감정 분류  알고리즘 참고(https://github.com/tlkh/text-emotion-classification)
- 인공 감정 엔진  알고리즘 참고(http://aidev.co.kr/aemotion/486)
