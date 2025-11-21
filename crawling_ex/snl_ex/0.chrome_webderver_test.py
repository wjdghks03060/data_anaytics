from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ★ 경로 지정 절대 하지 말기 — Selenium이 자동으로 드라이버 찾아서 다운로드함
driver = webdriver.Chrome(options=options)

driver.get("https://www.kobis.or.kr")

print("-" * 30)

time.sleep(10)
driver.quit()