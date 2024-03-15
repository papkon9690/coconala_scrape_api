from fastapi import FastAPI
from pydantic import BaseModel
import os
import datetime
from scraping import Scraper
from line_api import LINENotifyBot

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# パスの定義
static_path = "static/"
output_excel_path = static_path + "excel/output.xlsx"
log_txt_path = static_path + "log/log.txt"

# 環境変数の取得
access_token = os.environ.get('ACCESS_TOKEN')




def send_py_gmail(
    message_subject , message_body , from_email_smtp_password ,
    from_email , to_email , cc_mail_row_list = [] , file_path = "",
):
    """ メールを送信する関数 """
    msg = MIMEMultipart()
    msg['To'] = to_email
    msg['From'] = from_email
    if cc_mail_row_list !=[]:
        msg['Cc'] = ",".join(cc_mail_row_list)
    msg['Subject'] = message_subject
    msg.attach(MIMEText(message_body))
    # ファイルをメールに添付
    file_name = os.path.basename(file_path)
    with open(file_path , "rb") as f:
        attachment = MIMEApplication(f.read())
    attachment.add_header("Content-Disposition", "attachment", filename = file_name)
    msg.attach(attachment)
    # サーバーを指定しメールを送信
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, from_email_smtp_password)
    server.send_message(msg)
    server.quit()



class logText:
    def __init__(self , log_txt_path) -> None:
        self.log_txt_path = log_txt_path
        # logの保存ファイルを空にする
        with open(self.log_txt_path, 'w') as file:
            file.write('')

    def add_log_txt(self , add_log_text):
        """ logを付け加える関数 """
        with open(self.log_txt_path, 'a') as file:
            file.write("\n" + add_log_text)
log_txt = logText(log_txt_path)


class RequestDataScrape(BaseModel):
    """ apiに渡されるデータの定義 """
    search_keyword_list: list


app = FastAPI()

@app.post("/")
def api_coconala_scrape(api_data: RequestDataScrape):
    # クラウドソーシングからスクレイピング
    try:
        log_txt.add_log_txt("api 開始 : ")
        log_txt.add_log_txt()

        search_keyword_list = api_data.search_keyword_list
        coconala_scraper = Scraper()
        many_data_list = coconala_scraper.scraping_coconala(search_keyword_list)

        log_txt.add_log_txt("many_data_list : ")
        log_txt.add_log_txt(many_data_list)
        log_txt.add_log_txt()

        # LINEで通知
        line_bot = LINENotifyBot(access_token)
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        schedule = now.strftime('%Y/%m/%d %H:%M:%S')
        send_message = "\n\n"
        send_message = send_message + "\n" + "======================="
        send_message = send_message + "\n" + f"==== {schedule} ====="
        send_message = send_message + "\n" + "======================="
        line_bot.send(send_message)

        send_message = "\n\n"
        for loop , search_keyword in enumerate(search_keyword_list):
            send_message = send_message + "\n" + "------------------------------------------------------"
            send_message = send_message + "\n" + f"--- 検索対象 : ---- {search_keyword} ----- "
            send_message = send_message + "\n" + "------------------------------------------------------"
            data_list = many_data_list[loop]
            for small_loop , data in enumerate(data_list):
                if small_loop > 0:
                    send_message = send_message + "\n" + data[0]
                    send_message = send_message + data[1]
                if small_loop != 0 and small_loop % 7 == 0 :
                    send_message = send_message + "\n\n"
                    line_bot.send(send_message)
                    send_message = "\n\n"
            send_message = send_message + "\n" + "------------------------------------------------------"
            line_bot.send(send_message)
            send_message = "\n\n\n"
    except:
        # メールの送信文
        message_subject = "クラウドソーシングのスクレイピング結果"
        message_body = f"""
            エラーが発生しました
        """

        file_path = log_txt_path
        from_email = "debug01app@gmail.com"
        from_email_smtp_password = "wlwjrwxzcmtkpkyj"
        to_email = "yuki0606papkon9690@icloud.com"
        send_py_gmail(
            message_subject , message_body , from_email_smtp_password ,
            from_email , to_email ,
            file_path = file_path ,
        )



