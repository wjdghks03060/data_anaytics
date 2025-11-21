from bs4 import BeautifulSoup
import urllib.request as req
import datetime
#Html 가져오기
url = "https://finance.naver.com/marketindex/"
html = req.urlopen(url)

#  Html 분석하기
soup = BeautifulSoup(html, 'html.parser')

#원하는 데이터 추출하기
price = soup.select_one("div.head_info > span.value").string
print('usd/krw',price)
# ,제거하기
price = price.replace(",","")

t = datetime.datetime.today()
print('date: ', t)
base_path = './dollar_data/'
import os 
os.makedirs(base_path, exist_ok= True)
#data, 시간 포맷
getdate = t.strftime('%Y-%m')
#파일에 저장하기
fname = f"{base_path}/{getdate}.csv"
with open(fname, 'w', encoding= "utf-8") as f:
    f.write(getdate + ","+ price + "\n")


# 환율계산기
# 사용자로부터 원화 입력 ->달러로 변환
won = input('원화를 입력하세요: ${price}원 ->')
won = int(won)
dollar = won/int(price)
print(f"${won}원은 ${dollar}입니다.")