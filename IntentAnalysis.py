import nltk
from nltk.stem.lancaster import LancasterStemmer

class IntentAnalysis:

    stemmer = None
    training_data = []
    corpus_words = {}
    class_words = {}

    def __init__(self):
        print("초기화")
        # word stemmer
        self.stemmer = LancasterStemmer()


    def train(self, sentences):

        for sentence in sentences:
            self.training_data.append({"class": sentence[1] + "_" + sentence[0], "sentence": sentence[2].lower()})

        classes = list(set([a['class'] for a in self.training_data]))
        for c in classes:
            self.class_words[c] = []

        for data in self.training_data:
            for word in nltk.word_tokenize(data['sentence']):
                if word not in ["?", "'s"]:
                    stemmed_word = self.stemmer.stem(word.lower())
                    if stemmed_word not in self.corpus_words:
                        self.corpus_words[stemmed_word] = 1
                    else:
                        self.corpus_words[stemmed_word] += 1

                    self.class_words[data['class']].extend([stemmed_word])

    def calculate_class_score(self, sentence, class_name, show_details=True):
        score = 0
        for word in nltk.word_tokenize(sentence):
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                score += 1

                if show_details:
                    print("   match: %s" % self.stemmer.stem(word.lower()))
        return score

    def calculate_class_score_commonality(self, sentence, class_name, show_details=True):
        score = 0
        for word in nltk.word_tokenize(sentence):
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                score += (1 / self.corpus_words[self.stemmer.stem(word.lower())])

                if show_details:
                    print("   match: %s (%s)" % (
                    self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
        return score

    def classify(self, sentence):
        high_class = None
        high_score = 0
        for c in self.class_words.keys():
            score = self.calculate_class_score_commonality(sentence, c, show_details=False)
            if score > high_score:
                high_class = c
                high_score = score

        return high_class, high_score