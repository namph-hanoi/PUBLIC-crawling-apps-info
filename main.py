import re
from selenium import webdriver
from selenium.webdriver.common.by import By


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

first_apple_links: str

for link in links:
    hrefValue = link.get_attribute('href')

    pattern = r'^https://apps.apple.com/my/developer'
    if re.match(pattern, hrefValue):
        # print(hrefValue)
        first_apple_links = hrefValue
        break

if first_apple_links is not None:
    driver.get(first_apple_links)
    set_of_targeted_urls = set()
    set_of_see_all_urls = set()

    all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")


    for anchor in all_anchors:
        hrefValue = anchor.get_attribute('href')

    # collect all item urls within first_apple_links
        pattern_app_item = r'^https://apps.apple.com/\w+/app/'
        if re.match(pattern_app_item, hrefValue):
            set_of_targeted_urls.add(hrefValue)
            # print(hrefValue)

    # collect all 'see all' links
    see_more_anchors = driver.find_elements(By.CSS_SELECTOR, "a.section__nav__see-all-link")

    for anchor in see_more_anchors:
        hrefValue = anchor.get_attribute('href')
        set_of_see_all_urls.add(hrefValue)


    # jump into each 'see all', append further items into the set_of_targeted_urls
    for url in set_of_see_all_urls:
        driver.get(url)
        all_anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        # todo: make it common
        pattern_app_item = r'^https://apps.apple.com/\w+/app/'
        for anchor in all_anchors:
            hrefValue = anchor.get_attribute('href')
            if re.match(pattern_app_item, hrefValue):
                set_of_targeted_urls.add(hrefValue)


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








driver.quit()