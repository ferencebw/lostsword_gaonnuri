from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# 공통 문서 ID
DOC_ID = "1WuLy-H6ii3ScjW-Ldy-pARYTTvDzlnOdFkJGxSyMITk"

# 요일별 GID 매핑
SHEETS = {
    "mon": {"gid": "603726863", "name": "월요일"},
    "tue": {"gid": "1302259291", "name": "화요일"},
    "wed": {"gid": "1698551794", "name": "수요일"},
    "thu": {"gid": "717126084", "name": "목요일"},
    "fri": {"gid": "297088523", "name": "금요일"},
    "sat_magic": {"gid": "307273462", "name": "토요일(마법)"},
    "sat_phys": {"gid": "173358476", "name": "토요일(물리)"},
    "sun": {"gid": "1569757783", "name": "일요일"}
}

USER_ID = "ferencebw"
REPO_NAME = "lostsword_gaonnuri"

def create_html_wrapper(day_key, day_name):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>로스트 소드 공략 - {day_name}</title>
    <meta property="og:title" content="로스트 소드 공략 - {day_name}">
    <meta property="og:description" content="가온누리 {day_name} 최신 공략표 (자동 업데이트)">
    <meta property="og:image" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.png">
    <meta property="og:url" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.html">
    <meta property="og:type" content="website">
    <style>
        body {{ margin: 0; background: #222; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        img {{ max-width: 100%; height: auto; border: 1px solid #444; }}
    </style>
</head>
<body>
    <img src="{day_key}.png" alt="{day_name} 공략">
</body>
</html>"""
    with open(f"{day_key}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def take_screenshots():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,2500') # 높이를 넉넉하게 설정
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    
    try:
        for day_key, info in SHEETS.items():
            gid = info["gid"]
            day_name = info["name"]
            
            # /preview 주소를 사용하여 메뉴바가 없는 깔끔한 화면 호출
            target_url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/preview?gid={gid}"
            
            print(f"[{day_name}] 캡처 시도 중...")
            driver.delete_all_cookies() # 세션 간섭 방지
            driver.get(target_url)
            
            time.sleep(random.uniform(3, 6)) # 렌더링 시간 확보
            
            try:
                # 프리뷰 모드에서는 보통 'grid-table' 클래스나 특정 id의 테이블이 존재함
                # 전체 화면을 캡처하되, 불필요한 여백을 줄이기 위해 본문 영역만 찾음
                canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                canvas.screenshot(f"{day_key}.png")
                
                create_html_wrapper(day_key, day_name)
                print(f"[{day_name}] 완료")
            except Exception as e:
                print(f"[{day_name}] 실패: {e}")
                driver.save_screenshot(f"error_{day_key}.png")
            
            time.sleep(2)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
