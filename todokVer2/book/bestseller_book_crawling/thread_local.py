import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(f"user-agent={User_Agent }")


class ThreadLocalService:
    def __init__(self):
        self._driver_local = threading.local()

    def get_driver(self):
        if not hasattr(self._driver_local, 'driver'):
            # ChromeDriver 설정
            self._driver_local.driver = webdriver.Chrome(options=chrome_options)
        return self._driver_local.driver

    def quit_driver(self):
        if hasattr(self._driver_local, 'driver'):
            self._driver_local.driver.quit()
            del self._driver_local.driver