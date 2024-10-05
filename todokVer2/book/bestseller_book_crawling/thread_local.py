import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.86 Safari/537.36"
service = Service(executable_path='/home/ubuntu/server_version2/todokVer2/chromedriver-linux64/chromedriver')

chrome_options = Options()
chrome_options.add_argument("--headless")

# linux 환경에서 필요한 option
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument(f"user-agent={User_Agent }")


class ThreadLocalService:
    def __init__(self):
        self._driver_local = threading.local()

    def get_driver(self):
        if not hasattr(self._driver_local, 'driver'):
            # ChromeDriver 설정
            self._driver_local.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self._driver_local.driver

    def quit_driver(self):
        if hasattr(self._driver_local, 'driver'):
            self._driver_local.driver.quit()
            del self._driver_local.driver
