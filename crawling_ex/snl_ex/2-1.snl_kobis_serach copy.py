# webdriver_manager 를 활용하여 크롬 드라이버 연결하기
# selenium-4.6.0, chrome-driver 142.0.7444
# selenium-4.38.0, chrome-driver 114.0.5735.90
## [usage : ]
## pip install webdriver-manager 설치 하기
## from webdriver_manager.chrome import ChromeDriverManager
## chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
###############################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/

chrome = webdriver.Chrome(options=options) 
time.sleep(3) # 간단한 delay, 파이썬 라이브러리
chrome.get(url)
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))


# 한국것만 선택
# label for=repNationNoKor 인것 클릭
label = find(wait, "label[for='repNationNoKor']")
label.click()

# .wrap_btn button.btn_blue 클릭
btn = find(wait, ".wrap_btn button.btn_blue")
btn.click()

time.sleep(2) # 간단한 delay, 파이썬 라이브러리
items = chrome.find_elements(By.CSS_SELECTOR, ".tbl_comm tbody tr")

# selenium 방법으로 데이터 수집
print("영화제목 | 개봉일 | 매출액 | 괸객수")
print("-"*30)
for item in items:
  title = item.find_element(By.CSS_SELECTOR, "td.tal a").text
  open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
  reserve_rate = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.rstrip("%")
  sales_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.replace(",","")
  print(f"{title} | {open_date} | {reserve_rate} | {sales_price}")

#csv 파일로 저장
# 폴더 자동 생성
# 현재 datetime 모듈 활용
import datetime
import os 
now = datetime.datetime.now() 
folder_name = now.strftime("%Y%m%d %H%M%S_kobis")
  
if not os.path.exists(folder_name):
    os.makedirs(folder_name)  
file_path = os.path.join(folder_name, "kobis_serach.csv")
with open(file_path, "w", encoding="utf-8") as f:   
  f.write("영화제목,개봉일,매출액,관객수\n")
  for item in items:
      title = item.find_element(By.CSS_SELECTOR, "td.tal a").text
      open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
      reserve_rate = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.rstrip("%")
      sales_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.replace(",","")
      f.write(f"{title},{open_date},{reserve_rate},{sales_price}\n")
  

print("-"*30)
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료


#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133