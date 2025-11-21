from bs4 import BeautifulSoup
import urllib.request as req
import datetime
import os

# 1. 크롤링 (HTML 가져오기)
url = "https://news.naver.com/section/100" # 네이버 뉴스 정치 섹션
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
request = req.Request(url, headers=headers)
html = req.urlopen(request).read()


# 2. 스크래핑 준비 (BeautifulSoup 객체 생성)
soup = BeautifulSoup(html, 'html.parser')

# 데이터를 저장할 리스트
news_list = []

# 3. 핵심 스크래핑 (원하는 정보 추출)
# 네이버 뉴스 페이지에서 기사 항목 전체를 감싸는 선택자 (sa_item)
articles = soup.select('li.sa_item')

for article in articles:
    # 3-1. 헤드라인: 기사 제목이 담긴 <a> 태그
    headline_tag = article.select_one('strong.sa_text_strong')
    headline = headline_tag.get_text().strip() if headline_tag else "제목 없음"

    # 3-2. 신문사: 언론사 이름이 담긴 요소
    press_tag = article.select_one('div.sa_text_press')
    press = press_tag.get_text().strip() if press_tag else "신문사 없음"

    # 3-3. 썸네일 URL: <img> 태그의 'src' 속성 (수정된 부분)
    thumb_tag = article.select_one('div.sa_thumb_inner img')
    # -----------------------------------------------------
    # URL이 숨겨져 있을 가능성이 높은 'data-src' 속성 먼저 시도
    thumb_url = thumb_tag.get('data-src') 
    # 만약 data-src가 없으면 'src'를 시도
    if thumb_url is None:
        thumb_url = thumb_tag.get('src')
    # -----------------------------------------------------

    # 최종적으로 URL이 없으면 "URL 없음" 처리
    if thumb_url is None:
        thumb_url = "URL 없음"
    
    # 추출한 데이터 저장 (CSV에 맞게)
    news_list.append([headline, press, thumb_url])

# 4. 파일 저장 (최종 파싱 및 CSV 출력)
# 날짜 설정
t = datetime.datetime.today()
getdate = t.strftime('%Y-%m-%d')
base_path = './naver_news_data'
os.makedirs(base_path, exist_ok=True)
fname = f"{base_path}/{getdate}.csv"

with open(fname, 'w', encoding='utf-8') as f:
    f.write("헤드라인,신문사,썸네일URL\n") 
    for headline, press, thumb_url in news_list:
        # 데이터에 쉼표(,)가 포함될 경우를 대비해 쉼표가 들어간 데이터는 따옴표로 감싸는 것이 좋아.
        # 이 예시에서는 단순화를 위해 그대로 저장
        f.write(f'{headline},{press},{thumb_url}\n')

print(f"총 {len(news_list)}개의 기사 정보가 {fname}에 저장되었습니다.")