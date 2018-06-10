import tkinter as tk
import random
from tkinter import *
from PIL import ImageTk, Image
from EmotionManager import EmotionManager
import time
import speech_recognition as sr
from gtts import gTTS
import os

from tkinter import messagebox

import ChatLog
from IntentAnalysis import IntentAnalysis
from ChatDB import ChatDB
from LanguageProcess import LanguageProcess

class EmotionalChatbot:

    def __init__(self):
        print("초기화")
        self.log_print = True
        self.input_sentence = ""
        self.db = ChatDB()
        self.intent_analysis = IntentAnalysis()
        self.intent_analysis.train(self.db.get_sentence())
        # setting UI
        self.set_ui()

    def set_ui(self):
        self.window = tk.Tk()
        self.window.title("Chatbot")
        self.window.geometry("500x300")
        self.window.configure(background='white')

        self.res_label = Label(text="Hello")
        self.entry_value = StringVar()

        self.req_entry = Entry(textvariable=self.entry_value)

        def key(event):
            if event.char == '\r':
                self.response_ui()

        self.req_entry.bind("<Key>", key)
        image_file_name = ["angry1", "angry2","angry_angry", "angry_happy",
                           "happy1","happy2","happy_greeting","happy_happy",
                           "sad1","sad2","sad_happy","sad_sad",
                           "stable1","stable2","w_cool","w_love","w_money"]

        self.images = []

        for fname in image_file_name:
            full_name = "emotions/"+fname+".png"
            img = ImageTk.PhotoImage(Image.open(full_name))
            self.images.append(img)

        Label(text="Hobert").pack()

        w = tk.Label(self.window, image=img)
        w.pack(expand="yes")

        Label(text="응답").pack()

        self.res_label.pack()

        self.req_entry.pack()

        def on_click():
            self.response_ui()

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.window.destroy()
                self.emotionManager.stop()

        def on_click2():
            self.input_sentence = self.speech_recogition()
            value = self.process_sentence()
            self.speak(value[0])

        def on_change_feeling(feeling, personality):
            #print("feeling: " + feeling)
            #print("personality: " + personality)

            if feeling == "HAPPY":
                if "cool" in self.input_sentence.lower():
                    num = 14
                elif "love" in self.input_sentence.lower():
                    num = 15
                elif "money" in self.input_sentence.lower():
                    num = 16
                else:
                    if personality == "ANGRY":
                        num = 3
                    elif personality == "HAPPY":
                        num = 7
                    elif personality == "SAD":
                        num = 10
                    else:
                        num = random.choice([4, 5])
            elif feeling == "SAD":
                if personality == "SAD":
                    num = 11
                else:
                    num = random.choice([8, 9])
            elif feeling == "ANGRY":
                if personality == "ANGRY":
                    num = 2
                else:
                    num = random.choice([0, 1])
            else:
                num = 13

            w.configure(image=self.images[num])

        self.emotionManager = EmotionManager()
        self.emotionManager.set_on_change_feeling(on_change_feeling)
        self.emotionManager.start()
        #self.testChat()

        b = tk.Button(self.window, text="입력", command=on_click)
        b.pack()

        b = tk.Button(self.window, text="음성인식", command=on_click2)
        b.pack()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)

        self.window.mainloop()

    def response_ui(self):
        origin_value = self.entry_value.get()
        self.input_sentence = origin_value
        self.entry_value.set("")
        value = self.process_sentence()
        self.res_label['text'] = value[0]

    def process_sentence(self):
        nlp = LanguageProcess()
        target_value = nlp.stop_word_processing(self.input_sentence)
        request = nlp.simplify(target_value)
        sentiment = nlp.sentiment_analyzing(request)
        # print("sentiment:"+sentiment)
        if sentiment == "positive":
            self.emotionManager.iMode = 1
        elif sentiment == "negative":
            self.emotionManager.iMode = 2
        else:
            self.emotionManager.iMode = 0
        time.sleep(0.3)
        # print("Feeling" + emotionManager.get_feeling())
        result = self.intent_analysis.classify(request)[0]
        if result:
            arr = str(result).split('_')
            results = self.db.get_response_intent_emotion(arr[1], self.emotionManager.get_feeling(), arr[0])
            # for result in results:
            #     print(str(result))
        else:
            results = None
        if results is not None and len(results) > 0:
            value = random.choice(results)
            # print(results[0])
            self.res_label['text'] = value[0]

            category = arr[0] + ", " + arr[1]
            if self.log_print:
                ChatLog.write_log(self.input_sentence, value[0], self.emotionManager.get_feeling(),
                                  self.emotionManager.get_personality(), category)
        else:
            results = self.db.get_response_emotion(request, self.emotionManager.get_feeling())

            if len(results) > 0:
                value = random.choice(results)
                if self.log_print:
                    ChatLog.write_log(self.input_sentence, value[0], self.emotionManager.get_feeling(),
                                      self.emotionManager.get_personality(),
                                      "pattern matching")
            else:
                value = self.db.get_response_unknown()
                if self.log_print:
                    ChatLog.write_log(self.input_sentence, value[0], self.emotionManager.get_feeling(),
                                      self.emotionManager.get_personality(),
                                      "unknown")
        return value

    def speech_recogition(self):
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

            # Speech recognition using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                result = r.recognize_google(audio)
                print("You said: " + result)

                return result
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

    def speak(self, sentence):
        print("speak:"+sentence)
        tts = gTTS(text=sentence, lang='en')
        tts.save("./temp/tts.mp3")
        os.system("mpg321 ./temp/tts.mp3")

    def testChat(self):

        sentences = self.db.get_test_sentence()
        self.entry_value.set("Testing")

        for sentence in sentences:
            print("req:"+sentence[0].capitalize())
            self.input_sentence = sentence[0]
            result = self.process_sentence()
            print("res:"+result[0])

            time.sleep(5)

        #self.res_label['text'] = value[0]


emotional_chatbot = EmotionalChatbot()

