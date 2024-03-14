import requests


def main():
    api_site_url = "https://scraping-api-b9nu.onrender.com"
    search_keyword_list = [
        "スクレイピング" , 
        "Python" ,
    ]
    api_params = {
        "search_keyword_list": search_keyword_list ,
    }
    requests.post(api_site_url , json = api_params)


if __name__ == "__main__":
    main()