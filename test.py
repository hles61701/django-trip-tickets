from abc import ABC, abstractmethod
from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests


# 票券網站抽象類別
# class Website(ABC):
#     def __int__(self, city_name):
#         self.city_name = city_name 
    
#     @abstractmethod
#     def scrape(self):
#         pass

class Kkday:
    def __init__(self, city_name):
        self.city_name = city_name
    
    def scrape(self):
        result = [] # 結果回傳

        if self.city_name:
            response = requests.get(
                f'https://www.kkday.com/zh-tw/product/ajax_productlist/?country=&city=&keyword={self.city_name}'
            )
            # f"https://www.kkday.com/zh-tw/product/ajax_productlist/?keyword={self.city_name}&cat=TAG_4_4&sort=rdesc"

            # 抓取資料
            # 爬取票券的名稱、價格、最早可使用日期、評價及票券內容連結
            # name, price, earliest_sale_date, rating_url, url
            activities = response.json()['data']

            for activity in activities:
                title = activity['name']
                link = activity['url']
                price = activity['price']
                booking_date = activity['earliest_sale_date']
                star = activity['rating_star']

                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="KKday")
                )
        return result

demo = Kkday('花蓮')
print(demo.scrape())
