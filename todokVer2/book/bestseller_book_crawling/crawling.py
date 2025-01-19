import os
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from book.models import Book, BookDetail
from book.serializers import BookSerializer
from .thread_local import ThreadLocalService
import asyncio
import concurrent.futures
from asgiref.sync import sync_to_async
from django.db import transaction
import threading

from book.ai.services import extract_keywords

CRAWLING_URL = 'https://product.kyobobook.co.kr/KOR'   # 국내도서 section
# 책 제목, 저자, 출판사, 책 소개, 전체 페이지 수, 표지 url, 장르, isbn, 출판일, 목차
TITLE_PATH = '.prod_detail_title_wrap .prod_title_area .prod_title_box .prod_title'
AUTHOR_PATH = '.product_detail_area.product_person .title_wrap .title_heading .person_link .text'
PUBLISHER_PATH = '.prod_detail_view_wrap .prod_detail_view_area .col_prod_info .prod_info_text .btn_publish_link'
BOOK_IMAGE_PATH = '.prod_detail_view_wrap .prod_detail_view_area .col_prod_info.thumb .prod_thumb_swiper_wrap .prod_thumb_list_wrap .prod_thumb_item .blur_img_wrap .portrait_img_box img'   # src 태그
GENRE_PATH = '.product_detail_area.book_intro .intro_book .intro_category_list .category_list_item .intro_category_link'
BASIC_INFO_PATH = '.tbl_row_wrap .tbl_row tbody tr'
BOOK_INFO_PATH = '.product_detail_area.book_intro .intro_bottom .info_text:not(.fw_bold)'
BOOK_TABLE_OF_CONTENT_PATH = '.product_detail_area.book_contents .auto_overflow_wrap .auto_overflow_contents .auto_overflow_inner .book_contents_list .book_contents_item'


class BookCrawler:
    def __init__(self):
        self.thread_local_service = ThreadLocalService()
        self.url_by_genre = [#"https://product.kyobobook.co.kr/category/KOR/01",
                             #"https://product.kyobobook.co.kr/category/KOR/03",
                             #"https://product.kyobobook.co.kr/category/KOR/05",
                             #"https://product.kyobobook.co.kr/category/KOR/07",
                             "https://product.kyobobook.co.kr/category/KOR/13",
                             "https://product.kyobobook.co.kr/category/KOR/15",
                             "https://product.kyobobook.co.kr/category/KOR/17",
                             "https://product.kyobobook.co.kr/category/KOR/29"]
        # 세마포 객체 생성. 한번에 실행될 쓰레드를 2개로 제한
        self.sema = threading.Semaphore(2)


    def main(self):
        # 세마포어 획득
        self.sema.acquire()

        # ThreadPoolExecutor를 사용하여 crawling_by_genre 함수를 병렬로 실행
        # aws 서버의 vCPU = 1 (1코어)인 관계로 max_worker의 수는 최소한으로 !
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(2, os.cpu_count())) as executor:
            futures = [executor.submit(self.crawling_by_genre, url) for url in self.url_by_genre]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # 예외 발생 시 처리
                except Exception as e:
                    print(f"Error occurred: {e}")
        
        #self.thread_local_service.quit_driver()
        # 세마포어 해제
        self.sema.release()

    def crawling_by_genre(self, url):
        print("장르 크롤링 페이지 들어옴")
        driver = self.thread_local_service.get_driver()
        driver.get(url)
        driver.implicitly_wait(3)

        detail_obj = driver.find_elements(By.XPATH, '//*[@id="contents"]/div/aside/div[2]/div[1]/ul/li')

        for obj in detail_obj:
            detail_url = obj.find_element(By.TAG_NAME, 'a').get_attribute("href")
            driver.get(detail_url)
            # ----
            try:
                pagination_list = driver.find_elements(By.XPATH, '//*[@id="allTopPagi"]/div/a')
            except Exception:
                pagination_list = driver.find_elements(By.XPATH, '//*[@id="bestTopPagi"]/div/a')

            try:
                next_page_button = driver.find_element(By.XPATH, '//*[@id="allTopPagi"]/button[2]')
            except Exception:
                next_page_button = driver.find_element(By.XPATH, '//*[@id="bestTopPagi"]/button[2]')
            
            last_page_number = int(pagination_list[-1].text)

            for i in range(last_page_number):
                self.crawling_each_urls()
                #asyncio.run(self.crawling_each_urls())

                if i != (last_page_number-1):
                    driver.execute_script("arguments[0].click();", next_page_button)
                    driver.implicitly_wait(3)
            # ----
        self.thread_local_service.quit_driver()    


    #async def crawling_each_urls(self):
    def crawling_each_urls(self):
        each_book_urls = list()
        #tasks = list()
        driver = self.thread_local_service.get_driver()

        prod_items = driver.find_elements(By.XPATH, '//*[@id="homeTabAll"]/div[4]/ol/li')
        for list_number in range(len(prod_items)):
            book_objs = driver.find_elements(By.XPATH, '//*[@id="homeTabAll"]/div[4]/ol/li[' + str(list_number+1) + ']/div[2]/div[2]/div[1]/div/div')
            for book in book_objs:
                each_book_urls.append(book.find_element(By.TAG_NAME, 'a').get_attribute("href"))

        for each_url in each_book_urls:
            try:
                asyncio.run(EachBookCrawler().get_each_book_info(each_url))
            except Exception:
                continue
            # 각 get_each_book_info 호출을 태스크로 생성하여 tasks 리스트에 추가
        #     tasks.append(asyncio.create_task(self.get_each_book_info(each_url)))
        #
        # await asyncio.wait(tasks)

        #driver.quit()


class EachBookCrawler:
    def __init__(self):
        self.thread_local_service = ThreadLocalService()

    def filter_none_element(self, path, default=""):
        try:
            driver = self.thread_local_service.get_driver()
            return driver.find_element(By.CSS_SELECTOR, path).text
        except NoSuchElementException:
            return default

    async def get_each_book_info(self, url):
        driver = self.thread_local_service.get_driver()
        driver.get(url)
        driver.implicitly_wait(3)

        # 책 제목, 저자, 출판사, 책 소개, 목차, 장르, isbn, 출판일, 전체 페이지 수, 표지 url
        title = self.filter_none_element(TITLE_PATH)
        author = self.filter_none_element(AUTHOR_PATH)
        publisher = self.filter_none_element(PUBLISHER_PATH)
        intro = self.filter_none_element(BOOK_INFO_PATH)
        table_of_content = self.filter_none_element(BOOK_TABLE_OF_CONTENT_PATH)
        genre = driver.find_elements(By.CSS_SELECTOR, GENRE_PATH)[1].text

        th_elements = driver.find_elements(By.CSS_SELECTOR, BASIC_INFO_PATH)
        # 찾고자 하는 텍스트 값 목록
        targets = ["쪽수", "발행(출시)일자", "ISBN"]
        # 결과를 저장할 딕셔너리
        result = {}

        # 각 타겟 텍스트에 대해 td 값을 가져옴
        for th_element in th_elements:
            for target in targets:
                if th_element.find_element(By.TAG_NAME, 'th').text.strip() == target:  # 각 th 요소의 텍스트가 타겟과 일치하는지 확인
                    td_element = th_element.find_element(By.TAG_NAME, 'td')  # 해당 th의 형제인 td 요소 찾기
                    result[target] = td_element.text.strip()  # 결과 딕셔너리에 추가
                    break  # 일치하는 값을 찾으면 루프 종료

        # 각 값을 변수에 저장, 값이 없으면 기본값 ""을 사용
        total_pages = result.get("쪽수", "")
        # 값이 유효한 경우에만 숫자로 변환하고, 그렇지 않으면 기본값 설정
        if total_pages[:-1].isdigit():
            entire_pages = int(total_pages[:-1])
        else:
            entire_pages = 0
        isbn = result.get("ISBN", "")
        published_at = result.get("발행(출시)일자", "")

        try:
            image_element = driver.find_element(By.CSS_SELECTOR, BOOK_IMAGE_PATH)
            book_image = image_element.get_attribute('src')
        except NoSuchElementException:
            book_image = ""

        # 책 소개 기반 키워드 추출
        try:
            keywords = extract_keywords(intro)
        except Exception:
            self.thread_local_service.quit_driver()
            return

        # 트랜잭션을 사용하여 데이터베이스 작업을 원자적으로 처리
        # 중복된 데이터가 저장되는 것을 방지
        def db_operations():
            # isbn에 해당하는 책이 이미 저장되어 있는지 확인
            try:
                book_obj = Book.objects.get(isbn=isbn)
                return book_obj.book_id
            except Book.DoesNotExist:
                with transaction.atomic():
                    # 데이터베이스에 저장하는 작업을 비동기적으로 처리
                    book_data_dict = dict(
                        title=title,
                        author=author,
                        publisher=publisher,
                        genre=genre,
                        isbn=isbn,
                        published_at=published_at,
                        table_of_content=table_of_content,
                        keywords=keywords,
                        entire_pages=entire_pages,
                        book_image=book_image)
                    serializer = BookSerializer(data=book_data_dict)
                    if serializer.is_valid():  # 유효성 검사 (책 중복 저장 방지)
                        book = serializer.save()  # 저장
                        BookDetail.objects.create(
                            book=book,
                            intro=intro
                        )
                return book.book_id

        book_id = await sync_to_async(db_operations)()

        self.thread_local_service.quit_driver()
        return book_id
