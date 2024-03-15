"""
detailページへはボタンで遷移する
"""

import time
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# パスの定義
static_path = "static/"
log_txt_path = static_path + "log/log.txt"


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




class Scraper:
    def __init__(self , browse_visually = "no"):
        self.driver = self.browser_setup(browse_visually)
        self.wait_driver = WebDriverWait(self.driver, 10)
    
    def debug_page_html(self , file_name = "1"):
        html = self.wait_driver.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body"))).get_attribute("outerHTML")
        with open(file_name + ".html", "w", encoding="utf-8") as file:
            file.write(html)

    def browser_setup(self , browse_visually = "no" , user_agent_flag = False):
        """ブラウザを起動する関数"""
        options = webdriver.ChromeOptions()
        if browse_visually == "no":
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(1)
        return driver

    def scraping_coconala(self , search_keyword_list):
        many_data_list = []
        for loop , search_keyword in enumerate(search_keyword_list):
            log_txt.add_log_txt("def scraping_coconala 開始 : ")
            log_txt.add_log_txt(many_data_list)
            log_txt.add_log_txt()

            url = f"https://coconala.com/requests?keyword={search_keyword}&recruiting=true&page=1"
            self.driver.get(url)
            time.sleep(2)

            log_txt.add_log_txt("many_data_list : ")
            log_txt.add_log_txt(many_data_list)
            log_txt.add_log_txt()

            html = self.driver.page_source
            data_list = [] #ここにd_listを置かないとデータが蓄積されない。19段に置くと常に更新されて、csvに一つのデータしか入らない。

            soup = BeautifulSoup(html, 'lxml')
            # print(soup)
                
            indi_tags = soup.select('div.c-searchItem') #各詳細ページの項目タグになる。
            # print(indi_tags)

            data_list.append([
                    "titles" , "urls" ,
                ])
            for i, ind in enumerate (indi_tags):
                # areas = ind.select_one('h3.job-lst-main-ttl-txt').text
                titles = ind.select_one('div.c-itemInfo_title > a').text
                urls = ind.select_one('div.c-itemInfo_title > a').get('href')
    #             # dataes = ind.select_one('div.c-itemTileLine_remainingDate').text

                list1 = ['\n' + titles.strip() + '\n' + urls] # ここで '\n' + を入れないとURLがURLとして認識されない
                # list1 = list(filter(None,list1))
    #             # url = ind.select_one('div.c-searchPage_itemList')
                
    #             print(areas)
                # print(titles)
                # print(urls)
    #             # print(dataes)
    #         # u3_tags = soup.select('div.c-itemInfo_title > a').get('href') 
    #         # u3_tags = soup.select_one('div.c-itemInfo_title > href').text

    #         # print(len(indi_tags))
    #         # print(u3_tags)
    #         # u3_tags = soup.select_one('span.d-requestPrice_emphasis').text
    #         # u4_tags = soup.select_one('div.c-contentHeader > nav > ul > li:nth-of-type(4) > a ').text

                data_list.append([
                    titles , urls ,
                ])
                # print('='*30, i, '='*30 )
                # print(d_list[-1])
            
            # df = pd.DataFrame(data_list)
            # df.to_csv(f"coconala_{loop}.csv" , index=None, encoding='utf-8-sig')
            many_data_list.append(data_list)
        
        self.driver.quit()
        return many_data_list


def main():
    page_url = "https://www.google.com/"

if __name__ == "__main__":
    main()
