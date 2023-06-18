import re
from selenium import webdriver
from selenium.webdriver.common.by import By


google_options = webdriver.ChromeOptions()
google_options.add_experimental_option("detach", True)
driver = webdriver.Remote(
    command_executor='http://debian.vg:4444',
    options=google_options
)

developer = 'ghi-nguyen'
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

    links = driver.find_elements(By.CSS_SELECTOR, "a[href]")


    for link in links:
        hrefValue = link.get_attribute('href')

        pattern = r'^https://apps.apple.com/\w+/app/'
        if re.match(pattern, hrefValue):
            print(hrefValue)


driver.quit()