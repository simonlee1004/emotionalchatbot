import sqlite3
import random


class ChatDB:

    def __init__(self):
        print("초기화")
        # initialize the connection to the database
        connection = sqlite3.connect('chat_data_dialogflow.db')
        self.cursor = connection.cursor()

    def get_sentence(self):
        self.cursor.execute('select i.name, s.name, r.sentence from intent as i, request as r , SUB_DOMAIN as s '
                       'where i.intent_id = r.intent_id and i.sub_domain_id = s.sub_domain_id ')
        row = self.cursor.fetchall()
        return row

    def get_test_sentence(self):
        self.cursor.execute('SELECT sentence FROM request ORDER BY RANDOM() LIMIT 600')
        row = self.cursor.fetchall()
        return row

    def get_test_all_sentence(self):
        self.cursor.execute('SELECT sentence FROM request ORDER BY RANDOM()')
        row = self.cursor.fetchall()
        return row

    def get_response_intent_emotion(self, intent, emotion, sub_domain):
        self.cursor.execute('select  r.sentence, r.emotion, i.name, s.name '
                       ' from RESPONSE r, INTENT i, SUB_DOMAIN s '
                       ' where r.intent_id = i.intent_id '
                       ' and s.sub_domain_id = i.sub_domain_id '
                       ' and i.name = ? and r.emotion = ? and s.name =?', (intent, emotion, sub_domain))

        row = self.cursor.fetchall()
        return row

    def get_response_emotion(self, sentence, emotion):
        self.cursor.execute('select b.sentence, b.emotion from REQUEST a, RESPONSE b '
                       'where a.sentence like ? and a.intent_id=b.intent_id '
                       'and emotion = ?', (sentence, emotion))
        row = self.cursor.fetchall()
        return row

    def get_response_unknown(self):
        self.cursor.execute('select sentence, emotion from RESPONSE '
                       'where intent_id = 87 ')
        row = self.cursor.fetchall()

        value = random.choice(row)

        return value