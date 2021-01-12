from abc import ABC, abstractmethod
from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests

# 票券網站抽象類別
class Website(ABC):
    def __init__(self, city_name):
        self.city_name = city_name 
    
    @abstractmethod
    def scrape(self):
        pass


# KKday
class Kkday(Website):
    def scrape(self):
        result = [] # 結果回傳

        if self.city_name:
            response = requests.get(
                f'https://www.kkday.com/zh-tw/product/ajax_productlist/?country=&city=&keyword={self.city_name}'
            )
           

            # 抓取資料
            # 爬取票券的名稱、價格、最早可使用日期、評價及票券內容連結
            # name, price, earliest_sale_date, rating_url, url
            activities = response.json()['data']

            for activity in activities:
                title = activity['name']
                link = activity['url']
                price = int(activity['price'])
                booking_date = datetime.strftime(datetime.strptime(activity['earliest_sale_date'], "%Y%m%d"),'%Y-%m-%d')
                star = activity['rating_star']

                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="KKday")
                )
        return result
# 測試
# demo = kkday('花蓮')
# print(demo.scrape())


# Klook
class Klook(Website):
    def scrape(self):
        result = []

        
        if self.city_name:
            response = requests.get(f'https://www.klook.com/zh-TW/search/?keyword={self.city_name}&template_id=2&sort=price&start=1') 
            soup = bs(response.text,'lxml')

            activities = soup.find_all('div',{"class", "j_activity_item_link j_activity_item_click_action"})

            for activity in activities:
                title = activity.find('a').text.strip()
                link = 'https://www.klook.com' + str(activity.find('a',{'class':'title'}).get('href'))
                price = activity.find('span', {'class':"latest_price"}).find('b').text.strip()
                booking_date = activity.find('span', {'class':"g_right j_card_date"}).get('data-serverdate')[0:10]
                
                star = activity.find('span', {'class':"t14 star_score"}).text.strip() if activity.find('span', {'class':"t14 star_score"}) else "無"
                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="Klook"))
                            
        return result
        