import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class LanguageProcess:

    def simplify(self, sentence):
        return sentence.strip().lower()

    def stop_word_processing(self, sentence):
        postag = nltk.pos_tag(nltk.word_tokenize(sentence))
        for letter in sentence:
            if not(letter.isalnum()):
                if letter == "'" or letter == ' ':
                    continue
                sentence = sentence.replace(letter, '')
                # if letter == " u " or letter == "u "or letter == " u":
                #     sentence = sentence.replace(letter, ' you ')

        for item in postag:
            if item[1] == 'RB' or item[1] == 'LS' or item[1] == 'FW' or item[1] == 'UH' or item[1] == '.' or item[1] == ',':
                sentence = sentence.replace(item[0], '')

        sentence = sentence.strip()
        sentence = sentence.replace('  ', ' ')
        return sentence

    def sentiment_analyzing(self, sentence):
        sid = SentimentIntensityAnalyzer()
        #print(sentence)
        ss = sid.polarity_scores(sentence)

        if ss['compound'] > 0.2:
            #print("positive")
            return "positive"
        elif ss['compound'] < -0.2:
            #print("negative")
            return "negative"
        else:
            #print("neutral")
            return "neutral"
        #print("--------------")