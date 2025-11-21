from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import time
import os

# ========================
# Chrome 옵션 설정
# ========================
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("window-size=1000,1000")
options.add_argument("--headless")  # 브라우저 창 안뜨게

# ========================
# ChromeDriver 자동 설치/연결
# ========================
service = Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=service, options=options)

# ========================
# KOBIS URL 접속
# ========================
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"
chrome.get(url)
wait = WebDriverWait(chrome, 10)

def find(wait, css_selector):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 한국 영화 선택
label = find(wait, "label[for='repNationNoKor']")
label.click()

# 검색 버튼 클릭
btn = find(wait, ".wrap_btn button.btn_blue")
btn.click()
time.sleep(2)

# 테이블 데이터 수집
items = chrome.find_elements(By.CSS_SELECTOR, ".tbl_comm tbody tr")
data_list = []

for item in items:
    title = item.find_element(By.CSS_SELECTOR, "td.tal a").text
    open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
    reserve_rate = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.rstrip("%")
    sales_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.replace(",", "")
    data_list.append({
        "title": title,
        "open_date": open_date,
        "reserve_rate": reserve_rate,
        "sales_price": sales_price
    })

# ========================
# CSV 파일 저장 (날짜별)
# ========================
today = datetime.today().strftime("%Y%m%d")
save_dir = r"C:\Users\Admin\내 드라이브\KPMG_LAB\data_analytics\crawling_ex\snl_ex"
os.makedirs(save_dir, exist_ok=True)
file_path = os.path.join(save_dir, f"kobis_{today}.csv")

with open(file_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "open_date", "reserve_rate", "sales_price"])
    writer.writeheader()
    for row in data_list:
        writer.writerow(row)

print(f"CSV 저장 완료: {file_path}")

# ========================
# 브라우저 종료
# ========================
chrome.quit()
