from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# 인코그니토 테스트로 확인된 실제 문서 ID
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
    options.add_argument('--window-size=1920,3000') # 높이를 넉넉하게 설정
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    
    try:
        for day_key, info in SHEETS.items():
            gid = info["gid"]
            day_name = info["name"]
            
            # htmlview 엔드포인트 사용 (GID 리다이렉트 방지 및 로그인 우회)
            target_url = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/htmlview?gid={gid}"
            
            print(f"[{day_name}] 캡처 시도 중: {target_url}")
            driver.get(target_url)
            
            # 1. 시트 내용이 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "sheets-viewport")))
            time.sleep(5) # 폰트 및 이미지 렌더링 시간 확보

            # 2. [핵심] 불필요한 UI(상단 헤더, 하단 탭바) 숨기기 (JavaScript 실행)
            driver.execute_script("""
                document.getElementById('header').style.display = 'none';
                document.getElementById('top-bar').style.display = 'none';
                if(document.querySelector('.docs-sheet-container-bar')) {
                    document.querySelector('.docs-sheet-container-bar').style.display = 'none';
                }
                document.getElementById('sheets-viewport').style.top = '0';
            """)
            time.sleep(1)

            # 3. 공략표가 포함된 영역만 스크린샷
            # htmlview에서는 보통 grid-table-container 또는 body 자체를 찍는 것이 안전합니다.
            content = driver.find_element(By.ID, "sheets-viewport")
            content.screenshot(f"{day_key}.png")
            
            create_html_wrapper(day_key, day_name)
            print(f"[{day_name}] 완료")
            
    except Exception as e:
        print(f"에러 발생: {e}")
        driver.save_screenshot("fatal_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
