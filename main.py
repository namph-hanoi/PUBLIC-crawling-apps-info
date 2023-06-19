import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from service import ScrawlingService


google_options = webdriver.ChromeOptions()
google_options.add_experimental_option("detach", True)
driver = webdriver.Remote(
    command_executor='http://debian.vg:4444',
    options=google_options
)

# developer = 'ghi-nguyen'
# developer = 'google-llc'
developer = 'meta-platforms-inc'
driver.get(f"https://www.google.com/search?q={developer}+site%3Ahttps%3A%2F%2Fapps.apple.com%2Fmy%2Fdeveloper%2F{developer}")
driver.maximize_window()

links = driver.find_elements(By.CSS_SELECTOR, "a[href]")

first_apple_link = ScrawlingService.get_destination_page(links)


if first_apple_link is not None:
    driver.get(first_apple_link)
    set_of_see_all_urls = set()
    set_of_targeted_urls = set()

    all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
    ScrawlingService.get_app_urls_first_page(set_of_targeted_urls, all_anchors)
    print(set_of_targeted_urls)
    

    # collect all 'see all' links
    see_more_anchors = driver.find_elements(By.CSS_SELECTOR, "a.section__nav__see-all-link")

    for anchor in see_more_anchors:
        hrefValue = anchor.get_attribute('href')
        set_of_see_all_urls.add(hrefValue)


    # jump into each 'see all', append further items into the set_of_targeted_urls
    for url in set_of_see_all_urls:
        driver.get(url)
        all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        ScrawlingService.get_app_urls_second_page(set_of_targeted_urls, all_anchors)
        print(set_of_targeted_urls)


    print(set_of_targeted_urls)


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
        

    print(response)

else:
    print('Todo: throw httpError 400: searched developer not found')



driver.quit()