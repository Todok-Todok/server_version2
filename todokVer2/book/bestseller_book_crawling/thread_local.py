import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
service = Service(executable_path='/home/ubuntu/server_version2/todokVer2/chromedriver-linux64/chromedriver')
chrome_options = Options()
chrome_options.add_argument("--headless")

# linux 환경에서 필요한 option
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-allow-origins=*")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument(f"user-agent={User_Agent }")


class ThreadLocalService:
    def __init__(self):
        self._driver_local = threading.local()
        # 세마포 객체 생성. 한번에 실행될 쓰레드를 3개로 제한
        self.sema = threading.Semaphore(3)

    def get_driver(self):
        if not hasattr(self._driver_local, 'driver'):
            # 세마포어 획득
            self.sema.acquire()
            # ChromeDriver 설정
            self._driver_local.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self._driver_local.driver

    def quit_driver(self):
        if hasattr(self._driver_local, 'driver'):
            self._driver_local.driver.quit()
            del self._driver_local.driver

            # 세마포어 해제
            self.sema.release()
