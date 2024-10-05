from selenium.webdriver.common.by import By
from .thread_local import ThreadLocalService
import asyncio

CRAWLING_URL = 'https://search.kyobobook.co.kr/search?keyword='   # 크롤링 해서 저장된 DB에 없는 책 찾기
NOT_FOUND_TITLE_HEADING_XPATH = '//*[@id="contents"]/div/div/div[1]/h1/span'
BOOK_IMAGE_PATH = '.prod_area.horizontal .prod_thumb_box.size_lg .img_box img'
AUTHOR_PATH = '.switch_prod_wrap .prod_area .prod_info_box .prod_author_info .prod_author_group .author' # 가장 첫 text가 저자임.
TITLE_PATH = '.switch_prod_wrap .prod_area .prod_info_box .prod_name_group .auto_overflow_contents .prod_info'
KEYWORDS_PATH = '.tag_wrap.size_sm .tag' # 여러개
URL_PATH = '.switch_prod_wrap .prod_area .prod_info_box .prod_name_group .auto_overflow_contents .prod_info'


class AdditionalBookCrawler:
    def __init__(self):
        self.thread_local_service = ThreadLocalService()
        self.response_book_list = list()

    def main(self, book_name):
        driver = self.thread_local_service.get_driver()
        driver.get(CRAWLING_URL+str(book_name))

        search_result = driver.find_element(By.XPATH, NOT_FOUND_TITLE_HEADING_XPATH).text
        if search_result == " 상품 검색 결과가 없습니다. ":
            return None
        else:
            book_objs = driver.find_elements(By.XPATH, '//*[@id="shopData_list"]/ul/li')
            #print(len(book_objs))
            for book_obj in book_objs:
                asyncio.run(self.crawling_book_list(book_obj))

            return self.response_book_list

    async def crawling_book_list(self, book_obj):
        book_image = book_obj.find_element(By.CSS_SELECTOR, BOOK_IMAGE_PATH).get_attribute('src')
        author = book_obj.find_elements(By.CSS_SELECTOR, AUTHOR_PATH)[0].text
        title = book_obj.find_element(By.CSS_SELECTOR, TITLE_PATH).text
        keywords = book_obj.find_elements(By.CSS_SELECTOR, KEYWORDS_PATH)
        url = book_obj.find_element(By.CSS_SELECTOR, URL_PATH).get_attribute('href')

        each_book_dict = dict()
        keywords_list = list()

        for keyword in keywords:
            keywords_list.append(keyword.text)

        each_book_dict['book_image'] = book_image
        each_book_dict['author'] = author
        each_book_dict['title'] = title
        each_book_dict['keywords'] = keywords_list
        each_book_dict['url'] = url

        self.response_book_list.append(each_book_dict)






