from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 요일별 설정
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

BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIM8l8Q-Te56ELukyXtuU3x1HxCqGFRVEHZeQctyPZpZiHU5srn3xnI9xSz5cmf_ayPMr0LiecHNWr/pubhtml"
USER_ID = "ferencebw"
REPO_NAME = "lostsword_gaonnuri"

def create_html_wrapper(day_key, day_name):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>로스트 소드 공략 - {day_name}</title>
    <meta property="og:title" content="로스트 소드 공략 - {day_name}">
    <meta property="og:description" content="매시간 업데이트되는 가온누리 {day_name} 최신 공략표">
    <meta property="og:image" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.png">
    <meta property="og:url" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.html">
    <meta property="og:type" content="website">
    <style>
        body {{ margin: 0; background: #222; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        img {{ max-width: 100%; height: auto; }}
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
    options.add_argument('--window-size=2000,3000') # 캔버스 크기를 넉넉하게 조정

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # 최대 20초까지 엘리먼트가 나타나길 기다리는 설정
    wait = WebDriverWait(driver, 20)
    
    try:
        for day_key, info in SHEETS.items():
            gid = info["gid"]
            day_name = info["name"]
            
            target_url = f"{BASE_URL}?gid={gid}&single=true&widget=false&headers=false&chrome=false"
            print(f"[{day_name}] 접속 시도: {target_url}")
            
            driver.get(target_url)
            
            # 핵심 변경 사항: <table> 태그가 화면에 나타날 때까지 최대 20초 대기
            print(f"[{day_name}] 표 로딩 대기 중...")
            table_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            
            # 이미지가 포함된 경우 렌더링 시간을 위해 추가로 3초만 더 대기
            time.sleep(3)
            
            table_element.screenshot(f"{day_key}.png")
            create_html_wrapper(day_key, day_name)
            print(f"[{day_name}] 캡처 및 HTML 생성 완료")
            
    except Exception as e:
        print(f"에러 발생: {e}")
        # 에러 발생 시 현재 화면을 찍어 디버깅용으로 남김 (선택 사항)
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
