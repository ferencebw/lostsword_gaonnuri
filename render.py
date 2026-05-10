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

BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIM8l8Q-Te56ELukyXtuU3x1HxCqGFRVEHZeQctyPZpZiHU5srn3xnI9xSz5cmf_ayPMr0LiecHNWr/pubhtml"
USER_ID = "ferencebw"
REPO_NAME = "lostsword_gaonnuri"

def create_html_wrapper(day_key, day_name):
    """미리보기 및 모바일 화면에 이미지가 꽉 차 보이도록 HTML 생성"""
    
    # [설명] 모바일에서 화면 비율을 맞추기 위한 핵심 메타 태그
    viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {viewport_meta}
    <title>로스트 소드 공략 - {day_name}</title>
    
    <meta property="og:title" content="로스트 소드 공략 - {day_name}">
    <meta property="og:description" content="가온누리 {day_name} 최신 공략표 (자동 업데이트)">
    <meta property="og:image" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.png">
    <meta property="og:url" content="https://{USER_ID}.github.io/{REPO_NAME}/{day_key}.html">
    <meta property="og:type" content="website">
    
    <style>
        /* [설명] 모바일 최적화 스타일 */
        body {{
            margin: 0; 
            padding: 0;
            /* [해결 1] 배경색을 흰색으로 변경하여 여백을 숨깁니다. */
            background: white; 
            
            /* [해결 2] 중앙 정렬을 제거하고, 이미지를 상단에 배치합니다. */
            display: block; 
            text-align: center; /* 이미지를 가로 중앙에 배치 */
            width: 100%;
            height: 100%;
        }}
        
        img {{
            /* [해결 3] 이미지 너비를 모바일 화면에 꽉 채웁니다. */
            width: 100vw; 
            max-width: 1000px; /* 데스크탑에서 너무 커지는 것을 방지 */
            height: auto;
            
            /* 불필요한 테두리 및 여백 제거 */
            border: none;
            display: inline-block;
            vertical-align: top; /* 이미지를 상단에 밀착 */
        }}
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
    # 초기 윈도우 크기를 넉넉하게 설정
    options.add_argument('--window-size=1920,5000')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    
    try:
        for day_key, info in SHEETS.items():
            gid = info["gid"]
            day_name = info["name"]
            
            target_url = f"{BASE_URL}?gid={gid}&single=true"
            print(f"[{day_name}] 캡처 프로세스 가동...")
            
            driver.get(target_url)
            
            # 시트의 메인 뷰포트가 나타날 때까지 대기
            wait.until(EC.presence_of_element_located((By.ID, "sheets-viewport")))
            time.sleep(7) # 대용량 시트 렌더링을 위해 시간 연장

            # UI 숨기기 및 레이아웃 고정
            driver.execute_script("""
                var style = document.createElement('style');
                var css = '#header, #footer, #top-bar, .docs-sheet-container-bar { display: none !important; } ' +
                          'body { background: white !important; overflow: visible !important; } ' +
                          '#sheets-viewport { position: static !important; top: 0 !important; }';
                style.appendChild(document.createTextNode(css));
                document.head.appendChild(style);
            """)
            time.sleep(2)

            # [핵심] 시트 내용 전체를 포함하는 컨테이너를 찾아 캡처
            viewport = driver.find_element(By.ID, "sheets-viewport")
            viewport.screenshot(f"{day_key}.png")
            
            create_html_wrapper(day_key, day_name)
            print(f"[{day_name}] 전체 영역 캡처 성공")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
