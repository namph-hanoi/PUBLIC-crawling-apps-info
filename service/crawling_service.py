import re
from selenium.webdriver.remote.webdriver import WebDriver

class ScrawlingService:
    base_app_url_regex = r'^https://apps.apple.com/\w+/app/'

    @staticmethod
    def get_destination_page(google_search_results: list):
      first_apple_link: (str | None) = None

      for link in google_search_results:
          hrefValue = link.get_attribute('href')

          pattern = r'^https://apps.apple.com/my/developer'
          if re.match(pattern, hrefValue):
              # print(hrefValue)
              first_apple_link = hrefValue
              break
      return first_apple_link

    @staticmethod
    def get_app_urls_in_page(set_of_targeted_urls: set, all_anchors_in_page: list):
        for anchor in all_anchors_in_page:
            hrefValue = anchor.get_attribute('href')
            if hrefValue is not None and re.match(ScrawlingService.base_app_url_regex, hrefValue):
                set_of_targeted_urls.add(hrefValue)
