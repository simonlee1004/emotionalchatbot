import datetime
import csv


def write_log(req, res, feeling, personality, intent):
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    f = open('log/chat_log_'+today_date+'.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow([req.capitalize(), res.capitalize(), feeling, personality, intent])
    f.close()