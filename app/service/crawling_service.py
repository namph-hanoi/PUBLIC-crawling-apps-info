import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import abort
from selenium.webdriver.remote.webdriver import WebDriver
from app.bootstrap.config import Config

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CrawlingService:
    base_app_url_regex = r'^https://apps.apple.com/\w+/app/'

    @staticmethod
    def get_destination_page(google_search_results: list):
      first_apple_link: (str | None) = None

      for link in google_search_results:
          hrefValue = link.get_attribute('href')

          pattern = r'^https://apps.apple.com/my/developer'
          if re.match(pattern, hrefValue):
              first_apple_link = hrefValue
              break
      return first_apple_link

    @staticmethod
    def get_app_urls_in_page(set_of_targeted_urls: set, all_anchors_in_page: list):
        for anchor in all_anchors_in_page:
            hrefValue = anchor.get_attribute('href')
            if hrefValue is not None and re.match(CrawlingService.base_app_url_regex, hrefValue):
                set_of_targeted_urls.add(hrefValue)

    # Todo: create an e2e mock google search result page using Jinja template
    def _navigate_to_relevant_google_search(self, driver: WebDriver, developer: str):
        if os.getenv('FLASK_ENV') != 'test':
            driver.get(f"https://www.google.com/search?q={developer}+site%3Ahttps%3A%2F%2Fapps.apple.com%2Fmy%2Fdeveloper%2F{developer}")
        else:
            driver.get(f'http://{Config.APP_HOST}:{Config.APP_PORT}/e2e/mock-google-test-result')

    def get_apps_info(self, developer: str):
        google_options = webdriver.ChromeOptions()
        google_options.add_experimental_option("detach", True)
        # driver = webdriver.Remote(
        #     command_executor=f'http://{Config.CHROME_HOST}:{Config.CHROME_PORT}',
        #     options=google_options
        # )
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=google_options,
        )
        driver.get(f"https://www.google.com/search?q={developer}+site%3Ahttps%3A%2F%2Fapps.apple.com%2Fmy%2Fdeveloper%2F{developer}")
        driver.maximize_window()

        links = driver.find_elements(By.CSS_SELECTOR, "a[href]")

        first_apple_link = CrawlingService.get_destination_page(links)

        if first_apple_link is not None:
            driver.get(first_apple_link)
            set_of_see_all_urls = set()
            set_of_targeted_urls = set()

            all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
            CrawlingService.get_app_urls_in_page(set_of_targeted_urls, all_anchors)
            

            # collect all 'see all' links
            see_more_anchors = driver.find_elements(By.CSS_SELECTOR, "a.section__nav__see-all-link")

            for anchor in see_more_anchors:
                hrefValue = anchor.get_attribute('href')
                set_of_see_all_urls.add(hrefValue)


            # jump into each 'see all', append further items into the set_of_targeted_urls
            for url in set_of_see_all_urls:
                driver.get(url)
                all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                CrawlingService.get_app_urls_in_page(set_of_targeted_urls, all_anchors)

            response = []
            # start crawling in each url
            for app_url in set_of_targeted_urls:
                driver.get(app_url)
                app = {}
                app['app_url'] = app_url

                title = driver.find_element(By.CSS_SELECTOR, '.app-header__title')
                app['name'] = title.text

                id_regex_match = re.search(r'id(\d+)', app_url)
                if id_regex_match:
                    app['app_id'] = id_regex_match.group(1)
                
                devices_in_tags = driver.find_elements(By.CSS_SELECTOR, '.information-list__item__definition__item__term')

                app['app_targets'] = [tag.text for tag in devices_in_tags]

                response.append(app)

            driver.quit()
            return response

        else:
            driver.quit()
            abort(404, 'company_name not found')



