from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

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

BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_v218jP6t6TliliGxDYnRVJrkyUrQ_NlhqJr6ncwbdBbTHRjkIYgkxcFppFtIp1uCZA1_MHzteVZH/pubhtml"
USER_ID = "ferencebw"
REPO_NAME = "lostsword_gaonnuri"

def create_html_wrapper(day_key, day_name):
    """모바일에서 확대가 가능하고 화면에 꽉 차는 HTML 생성"""
    
    # =========================================================================
    # [수정 1] 메신저 캐시 우회를 위한 실행 시점 타임스탬프 생성
    # =========================================================================
    timestamp = int(time.time())
    
    viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    
    # =========================================================================
    # [수정 2] og:image 및 og:url 뒤에 타임스탬프 버전 파라미터(?v=...) 자동 부여
    # 메신저(카카오톡 등)가 이전 미리보기 썸네일을 캐싱하지 않고 최신 이미지를 강제로 로드합니다.
    # =========================================================================
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {viewport_meta}
    <title>로스트 소드 공략 - {day_name}</title>
    <meta property="og:title" content="로스트 소드 공략 - {day_name}">
    <meta property="og:description" content="가온누리 {day_name} 최신 공략표">
    <meta property="og:image" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.png?v={timestamp}">
    <meta property="og:url" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.html?v={timestamp}">
    <meta property="og:type" content="website">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: white;
            display: flex;
            flex-direction: column;
            align-items: center; /* 가로 중앙 정렬 */
        }}
        img {{
            width: 100%;
            max-width: none;
            height: auto;
            display: block;
        }}
    </style>
</head>
<body>
    <!-- 본문 이미지 경로에도 타임스탬프를 부여하여 웹 브라우저 캐시 방지 -->
    <img src="{day_key}.png?v={timestamp}" alt="{day_name} 공략">
</body>
</html>"""
    with open(f"{day_key}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def take_screenshots():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=2000,5000') 
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    
    try:
        for day_key, info in SHEETS.items():
            gid = info["gid"]
            day_name = info["name"]
            
            target_url = f"{BASE_URL}?gid={gid}&single=true"
            print(f"[{day_name}] 작업 시작...")
            
            driver.get(target_url)
            
            # 시트 내용 로딩 대기
            canvas = wait.until(EC.presence_of_element_located((By.ID, "sheets-viewport")))
            
            driver.execute_script("document.body.style.zoom='1.2'")
            time.sleep(7) 

            # UI 숨기기
            driver.execute_script("""
                var style = document.createElement('style');
                var css = '#header, #footer, #top-bar, .docs-sheet-container-bar { display: none !important; } body { background: white !important; }';
                style.appendChild(document.createTextNode(css));
                document.head.appendChild(style);
            """)
            time.sleep(2)

            # 캡처 (가장 큰 영역인 viewport 지정)
            canvas.screenshot(f"{day_key}.png")
            
            create_html_wrapper(day_key, day_name)
            print(f"[{day_name}] 완료")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
