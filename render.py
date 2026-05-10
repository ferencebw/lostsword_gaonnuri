from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 구글 UI(상단 탭 등)를 제거한 pubhtml URL
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIM8l8Q-Te56ELukyXtuU3x1HxCqGFRVEHZeQctyPZpZiHU5srn3xnI9xSz5cmf_ayPMr0LiecHNWr/pubhtml?gid=603726863&single=true&widget=false&headers=false&chrome=false"

def take_screenshot():
    options = Options()
    options.add_argument('--headless') # 화면을 띄우지 않고 백그라운드 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,2000') # 잘리지 않도록 넉넉한 캔버스 크기

    print("크롬 브라우저 세팅 중...")
    # ChromeDriverManager가 서버 환경에 맞는 드라이버를 자동 설치
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL)
        print("페이지 로딩 대기 (캐릭터 이미지 다운로드 확보)...")
        time.sleep(5) # 시트 내 고용량 이미지가 다 뜰 때까지 5초 대기
        
        print("공략표 영역 캡처 중...")
        # pubhtml 문서 구조상 실제 데이터가 담긴 table 태그를 찾아 해당 부분만 캡처
        table_element = driver.find_element(By.TAG_NAME, 'table')
        table_element.screenshot('output.png')
        print("성공: 원본 그대로 output.png 저장 완료")
        
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshot()