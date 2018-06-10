import threading
import time
import matplotlib.pyplot as plt
import matplotlib as mpl

# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
mpl.rcParams['axes.unicode_minus'] = False

class EmotionManager(threading.Thread):
    # 감정모델을 초기화
    m_fPersonality = []
    m_fPersonality_Prev = []
    m_fMood = []
    m_fMood_Prev = []
    m_fEmotion = []
    m_fEmotion_Prev = []
    m_fFeeling = []
    m_fFeeling_Prev = []
    m_iPersonality = 0
    m_iMood = 0
    m_iFeeling = 0
    m_fMu = 0.0
    m_fLambda = 0.0
    m_fEpsilon = 0.0
    m_fAlpha = 0.0
    m_fBeta = 0.0
    m_fGamma = 0.0
    m_fDelta = 0.0
    iMode = 0
    emotion = 3

    is_stop = 0

    temp_feeling = ""
    temp_personality = ""
    #on_change_feeling = None

    def __init__(self):
        #print("초기화")

        threading.Thread.__init__(self)
        threading.Thread.daemon = True

        for i in range(0, 3):
            self.m_fPersonality.append(0)
            self.m_fPersonality_Prev.append(0)
            self.m_fMood.append(0)
            self.m_fMood_Prev.append(0)
            self.m_fEmotion.append(0)
            self.m_fEmotion_Prev.append(0)
            self.m_fFeeling.append(0)
            self.m_fFeeling_Prev.append(0)

        #self.m_iPersonality = self.m_iMood = self.m_iFeeling = self.emotion.value
        self.m_iPersonality = 3
        self.m_iMood = 3
        self.m_iFeeling = 3


        self.m_fMu = 0.005
        #self.m_fLambda = 0.1
        self.m_fLambda = 0.15
        self.m_fEpsilon = 0.005
        self.m_fAlpha = 0.1
        self.m_fBeta = 0.5
        self.m_fGamma = 0.4
        self.m_fDelta = 0.2
        self.iMode = 0
        self.emotion = 3

    def stop(self):
        self.is_stop = 1

    # 현재 감정의 종류를 결정
    def get_emotion_type(self, value):
        max_n = 0
        max = -100.0
        min = 100.0

        # 최대, 최소를 구함
        for i in range(0, 3):
            if value[i] > max:
                max = value[i]
                max_n = i
            if value[i] < min:
                min = value[i]
                min_n = i

        # 최대값과 최소값의 차를 구함
        diff = max - min;

        # 차가 delta 미만이면 현재 감정은 Stable
        if diff < self.m_fDelta:
            return 3

        if max_n == 0:  #happy
            return 0
        if max_n == 1:  #sad
            return 1
        if max_n == 2: #stable
            return 2

        return 3 #stable

    def set_on_change_feeling(self, callback = None):
        if callback:
            self.on_change_feeling = callback

    # 감정변수들을 사용하여 현재의 감정을 계산
    def process_emotion(self):

        i = 0
        # Mood값을 계산
        for i in range(0, 3):
            self.m_fMood[i] = self.m_fLambda * self.m_fEmotion[i] + self.m_fMood_Prev[i]

            if self.m_fMood[i] > 0.0:
                self. m_fMood[i] = self. m_fMood[i]-self.m_fEpsilon
                if self.m_fMood[i] < 0.0:
                    self.m_fMood[i] = 0.0
            elif self.m_fMood[i] < 0.0:
                self.m_fMood[i] = self.m_fMood[i] + self.m_fEpsilon
                if self.m_fMood[i] > 0.0:
                    self.m_fMood[i] = 0.0
            if self.m_fMood[i] > 1.0:
                self.m_fMood[i] = 1.0
            if self.m_fMood[i] < -1.0:
                self.m_fMood[i] = -1.0
            self.m_fMood_Prev[i] = self.m_fMood[i];

        self.m_iMood = self.get_emotion_type(self.m_fMood);
        # ------------------------------------------------
        # Personality값을 계산
        # ------------------------------------------------
        for i  in range(0,3):
            self.m_fPersonality[i] = self.m_fMu * self.m_fMood[i] + self.m_fPersonality_Prev[i]
            if self.m_fPersonality[i] > 1.0: self.m_fPersonality[i] = 1.0
            if self.m_fPersonality[i] < -1.0: self.m_fPersonality[i] = -1.0
            self.m_fPersonality_Prev[i] = self.m_fPersonality[i]
        self.m_iPersonality = self.get_emotion_type(self.m_fPersonality);

        # ------------------------------------------------
        # Feeling값을 계산
        # ------------------------------------------------
        for i in range(0,3):
            self.m_fFeeling[i] = (self.m_fAlpha * self.m_fEmotion[i]) + (self.m_fBeta * self.m_fMood[i]) + (self.m_fGamma * self.m_fPersonality[i])

        self.m_iFeeling = self.get_emotion_type(self.m_fFeeling)

        # ------------------------------------------------
        # Emotion값을 초기화
        # ------------------------------------------------
        for i in range(0,3):
            self.m_fEmotion[i] = 0.0

    def set_emotion(self, type, up, down):
        if type == 0:
            self.m_fEmotion[0] = up
            self.m_fEmotion[1] = down
            self.m_fEmotion[2] = down
        elif type == 1:
            self.m_fEmotion[1] = up
            self.m_fEmotion[0] = down
            self.m_fEmotion[2] = down
        elif type == 2:
            self.m_fEmotion[2] = up
            self.m_fEmotion[0] = down
            self.m_fEmotion[1] = down

    def get_emotion(self, input_emotion):
        result = "NONE"
        if input_emotion == 3:
            result = "STABLE"
        elif input_emotion == 0:
            result = "HAPPY"
        elif input_emotion == 1:
            result = "SAD"
        elif input_emotion == 2:
            result = "ANGRY"
        return result

    def get_feeling(self):
        return self.get_emotion(self.m_iFeeling)

    def get_personality(self):
        return self.get_emotion(self.m_iPersonality)


    def run(self):
        while self.is_stop == 0:
            #self.iMode = 2
            if self.iMode == 1:
                self.set_emotion(0, 1.0, -0.5)
            elif self.iMode == 2:
                self.set_emotion(2, 1.0, -0.5)
            elif self.iMode == 0:
                #self.set_emotion(1, 0.1, 0.0)
                self.set_emotion(1, 0.05, 0.0)

            self.iMode = 0

            self.process_emotion()

            if self.on_change_feeling is not None:
                self.on_change_feeling(self.get_emotion(self.m_iFeeling), self.get_emotion(self.m_iPersonality))

            self.print_info()

            time.sleep(0.5)

    m_times = []
    m_happy = []
    m_sad = []
    m_angry = []
    m_happy_p = []
    m_sad_p = []
    m_angry_p = []
    m_count = 0


    def print_info(self):
        # 아바타 얼굴 출력
        print("avatar:")
        if self.m_iFeeling == 3:
            print("stable")
        elif self.m_iFeeling == 0:
            print("happy")
        elif self.m_iFeeling == 1:
            print("sad")
        elif self.m_iFeeling == 2:
            print("angry")
        print("------------------------")

        # 사용자 얼굴 출력
        print("user face:")
        if self.iMode == 1:
            print("stable")
        elif self.iMode == 2:
            print("scold")
        print("------------------------")

        #문자 출력
        print("Text status")

        print("Personality:")
        self.get_emotion(self.m_iPersonality)
        print("Mood:")
        self.get_emotion(self.m_iMood)
        print("Feeling:")
        self.get_emotion(self.m_iFeeling)
        print("------------------------")

        # 수치 출력
        is_print_num = False
        if(is_print_num):
            print("[Personality]")
            print("Happy:"+str(self.m_fPersonality[0]))
            print("Sad:"+str(self.m_fPersonality[1]))
            print("Angry:"+str(self.m_fPersonality[2]))

            print("[Mood]")
            print("Happy:"+str(self.m_fMood[0]))
            print("Sad:"+str(self.m_fMood[1]))
            print("Angry:"+str(self.m_fMood[2]))

            print("[Feeling]")
            print("Happy:"+str(self.m_fFeeling[0]))
            print("Sad:"+str(self.m_fFeeling[1]))
            print("Angry:"+str(self.m_fFeeling[2]))

            self.m_count = self.m_count + 0.5

            self.m_times.append(self.m_count)
            self.m_happy.append(self.m_fFeeling[0])
            self.m_sad.append(self.m_fFeeling[1])
            self.m_angry.append(self.m_fFeeling[2])

            self.m_happy_p.append(self.m_fPersonality[0])
            self.m_sad_p.append(self.m_fPersonality[1])
            self.m_angry_p.append(self.m_fPersonality[2])

            # if self.m_count == 20:
            #     self.drawGraph("happy")
            #     self.drawGraph("sad")
            #     self.drawGraph("angry")
            #     self.drawGraph2("happy")
            #     self.drawGraph2("sad")
            #     self.drawGraph2("angry")

    def drawGraph(self, type):
        plt.rcParams["font.family"] = 'AppleGothic'

        if type=="happy":
            plt.plot(self.m_times, self.m_happy, color='green')
            plt.title("시간에 따른 행복 감정 변화")
        elif type=="sad":
            plt.plot(self.m_times, self.m_sad, color='blue')
            plt.title("시간에 따른 슬픔 감정 변화")
        elif type=="angry":
            plt.plot(self.m_times, self.m_angry, color='red')
            plt.title("시간에 따른 분노 감정 변화")

        plt.ylabel("감정 지수")
        plt.savefig("./log/"+type+"_graph.png")
        plt.clf()
        #plt.show()

    def drawGraph2(self, type):
        plt.rcParams["font.family"] = 'AppleGothic'

        if type=="happy":
            plt.plot(self.m_times, self.m_happy_p, color='green')
            plt.title("시간에 따른 행복 성격 변화")
        elif type=="sad":
            plt.plot(self.m_times, self.m_sad_p, color='blue')
            plt.title("시간에 따른 슬픔 성격 변화")
        elif type=="angry":
            plt.plot(self.m_times, self.m_angry_p, color='red')
            plt.title("시간에 따른 분노 성격 변화")

        plt.ylabel("감정 지수")
        plt.savefig("./log/"+type+"_graph2.png")
        plt.clf()
