from fastapi import FastAPI
from pydantic import BaseModel
import os
import datetime
from scraping import Scraper
from line_api import LINENotifyBot


# パスの定義
static_path = "static/"
output_excel_path = static_path + "excel/output.xlsx"

# 環境変数の取得
access_token = os.environ.get('ACCESS_TOKEN')

class RequestDataScrape(BaseModel):
    """ apiに渡されるデータの定義 """
    search_keyword_list: list


app = FastAPI()

@app.post("/")
def api_coconala_scrape(api_data: RequestDataScrape):
    # クラウドソーシングからスクレイピングs
    search_keyword_list = api_data.search_keyword_list
    coconala_scraper = Scraper()
    many_data_list = coconala_scraper.scraping_coconala(search_keyword_list)

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



