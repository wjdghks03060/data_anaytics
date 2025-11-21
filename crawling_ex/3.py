from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os
import csv

# html 가져오기
url = "https://news.naver.com/section/101"
html = req.urlopen(url)

# HTML 파싱하기
soup = BS(html, 'html.parser')

lis = soup.select("ul.sa_list > li")
news_list = []
for li in lis:
    title = li.select_one("strong.sa_text_strong").get_text().strip()
    press = li.select_one("div.sa_text_press").get_text().strip()
    image_url = li.select_one("a.sa_thumb_link._NLOG_IMPRESSION::after")

    if image_url:
        img_url = img_url.get("data-src")
        img_url = img_url.split("?")[0]
    else:
        img_url = 'img url 없음'
    print(f"{title} - {press}\n Image Url : {img_url}")
    news_list.append([title, press, img_url])
# print(news_list)

base_path = 'naver_news'
os.makedirs(base_path, exist_ok=True)

filename = datetime.datetime.now().strftime("%Y-%m-%d-%H") + ".csv"

with open(f"{base_path}/{filename}", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(news_list)