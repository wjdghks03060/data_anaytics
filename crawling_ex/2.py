from bs4 import BeautifulSoup
import urllib.request as req
import datetime
#Html 가져오기
url = "https://finance.naver.com/marketindex/exchangeList.naver"
html = req.urlopen(url)

#  Html 분석하기
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
# print(soup)

# tbody tr td1, td2
# print(soup.select("tbody > tr")[0].select_one('td').get_text().strip())


import os

exchange_list = []
trs = soup.select('tbody > tr')

for tr in trs:
    title = tr.select_one('td.tit').get_text().strip()
    sale = tr.select_one('td.sale').get_text().strip()
    exchange_list.append([title, sale])

# 날짜 설정
t = datetime.datetime.today()
getdate = t.strftime('%Y-%m-%d')

# 폴더 생성
base_path = './exchange_rate'
os.makedirs(base_path, exist_ok=True)

# csv 파일명 생성
fname = f"{base_path}/{getdate}.csv"

# 저장
with open(fname, 'w', encoding='utf-8') as f:
    f.write("통화명,매매기준율\n")  # CSV 헤더
    for title, sale in exchange_list:
        f.write(f"{title},{sale}\n")
    