from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 요일별 이름과 GID 매핑 (제공해주신 링크 기반)
SHEETS = {
    "mon": "603726863",
    "tue": "1302259291",
    "wed": "1698551794",
    "thu": "717126084",
    "fri": "297088523",
    "sat_magic": "307273462",
    "sat_phys": "173358476",
    "sun": "1569757783"
}

BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIM8l8Q-Te56ELukyXtuU3x1HxCqGFRVEHZeQctyPZpZiHU5srn3xnI9xSz5cmf_ayPMr0LiecHNWr/pubhtml"

def take_screenshots():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,2000')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for day, gid in SHEETS.items():
            # 깔끔한 캡처를 위한 파라미터 조합
            target_url = f"{BASE_URL}?gid={gid}&single=true&widget=false&headers=false&chrome=false"
            
            print(f"[{day}] 캡처 시작: {target_url}")
            driver.get(target_url)
            time.sleep(5) # 이미지 로딩 대기
            
            table_element = driver.find_element(By.TAG_NAME, 'table')
            filename = f"{day}.png"
            table_element.screenshot(filename)
            print(f"[{day}] 저장 완료: {filename}")
            
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshots()
