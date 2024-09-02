# -*- coding: utf-8 -*-
#  Work on gcp
import sys
import math
from selenium import webdriver
import time
import csv
import random

# import configparser
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyotp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from os.path import exists


def pdb():
    import web_pdb

    web_pdb.set_trace()


root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
# CONFIG_DIR = ROOT_DIR + "/config.ini"

# config = configparser.ConfigParser()
# config.read(CONFIG_DIR)
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# chrome_options.binary_location = '/usr/bin/chromium-browser'

# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)

# path_to_chromedriver = "/usr/local/bin/chromedriver"
# service = Service(executable_path=path_to_chromedriver)

# Ngon 1
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
)


# driver = webdriver.Remote(
#     command_executor=f"http://116.104.74.118:4444", options=chrome_options
# )


# TODO: move SessionSaver to another util file
class SessionSaver:
    def __init__(self, driver=driver):
        self.driver = driver
        # TODO: place the paths into the config file
        self.cookies_file_path = "cookies.txt"
        self.localstorage_file_path = "local_storage.txt"

    def save_session(self):
        cookies = self.driver.get_cookies()
        with open(self.cookies_file_path, "w") as cookies_file:
            json.dump(cookies, cookies_file)

        local_storage = driver.execute_script(
            "return JSON.stringify(window.localStorage);"
        )
        with open(self.localstorage_file_path, "w") as local_storage_file:
            local_storage_file.write(local_storage)

    def load_session(self):
        if exists(self.cookies_file_path) and exists(self.localstorage_file_path):
            with open(self.cookies_file_path, "r") as cookies_file:
                cookies = json.load(cookies_file)

                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            with open(self.localstorage_file_path, "r") as local_storage_file:
                local_storage_data = json.load(local_storage_file)

                # Iterate over each key-value pair and set it in localStorage
                for key, value in local_storage_data.items():
                    self.driver.execute_script(
                        f"window.localStorage.setItem(arguments[0], arguments[1]);",
                        key,
                        value,
                    )

    def is_logged_in(self):
        self.driver.get("https://www.linkedin.com/uas/login")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".global-nav__me-photo.evi-image.ember-view")
                )
            )
            if element:
                return True
        except:
            pass

        return False


session_saver = SessionSaver()


def config_to_login():
    return run(
        username="naz665564@gmail.com",
        password="Pakistan@1234*@!",
    )


def write_output(output_file, data_list):
    with open(output_file, "a") as fp:
        row = csv.writer(fp, delimiter=",", lineterminator="\n")
        for data in data_list:
            row.writerow(data)


def get_query_list(query_file):
    query_list = []
    f = open(query_file, "r")
    for i in f:
        i = i.replace("\n", "")
        query_list.append(i)
    return query_list


def write_column_header(output_file_name):
    column_header = [
        "Serial",
        "Page_Link",
        "Company_Li_URL",
        "Li_Id",
        "Co_Name",
        "Co_Indusrty",
        "Co_Emp_Count",
        "total_count",
    ]
    with open(output_file_name, "w", encoding="utf-8") as fp:
        row = csv.writer(fp, delimiter=",", lineterminator="\n")
        row.writerow(column_header)


# NOTE: WebDriverWait with timeout doesn't work sometimes, this is the solution:
# def _get_element_tricky(css_selector, many=False, driver=driver):
#     try:
#         if many == True:
#             return driver.find_elements(By.CSS_SELECTOR, css_selector)
#         return driver.find_element(By.CSS_SELECTOR, css_selector)
#     except NoSuchElementException:
#         raise NoSuchElementException(
#             f"Element with CSS selector '{css_selector}' not found."
#         )


def _get_element_strictly(css_selector, many=False, timeout=6, driver=driver):
    try:
        # WebDriverWait doesn't work well
        # element = WebDriverWait(driver, timeout).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        # )
        if many == True:
            return driver.find_elements(By.CSS_SELECTOR, css_selector)
        return driver.find_element(By.CSS_SELECTOR, css_selector)
    except (NoSuchElementException, TimeoutException):
        raise NoSuchElementException(
            f"Element with CSS selector '{css_selector}' not found."
        )


def _get_element_loosely(css_selector, many=False, timeout=20, driver=driver):
    try:
        return _get_element_strictly(
            css_selector, many=False, timeout=20, driver=driver
        )
    except (NoSuchElementException, TimeoutException):
        pass
    return None


def get_login_linkedin(username, password):
    # TODO: check if the config.get("cookies_file", "cookies_file") & localstorage_file
    print("Logger: start logging in")
    driver.get("https://www.linkedin.com")
    session_saver.load_session()
    is_logged_in = session_saver.is_logged_in()

    def type_in_password():
        password_input = _get_element_strictly('input[id="password"]')
        password_input.send_keys(password)

    if not is_logged_in:
        second_barrier = _get_element_loosely(
            ".member__profile"
        ) and _get_element_loosely('input[id="password"]')
        if second_barrier:
            type_in_password()
        else:
            user = driver.find_element(By.CSS_SELECTOR, 'input[id="username"]')
            user.send_keys(username)
            time.sleep(1)
            pword = driver.find_element(By.CSS_SELECTOR, 'input[id="password"]')
            pword.send_keys(password)
        time.sleep(1)
        login = driver.find_element(
            By.CSS_SELECTOR, 'button[data-litms-control-urn="login-submit"]'
        )
        login.click()
        time.sleep(2)
        print("""Get logged in""")
        second_fa_header = _get_element_loosely("#auth-app-div .content__header")
        if (
            second_fa_header
            and second_fa_header.text
            == "Enter the code you see on your authenticator app"
        ):
            # TODO: get the secret into the config file
            veri_code = pyotp.TOTP("Y4EJYCNDHGUUS7ILAX3WUFVUG62XBZEJ").now()
            verification_code_input = _get_element_strictly(".input_verification_pin")
            verification_code_input.send_keys(veri_code)
            time.sleep(1)
            btn_submit = _get_element_strictly("button.form__submit")
            btn_submit.click()
    if session_saver.is_logged_in():
        driver.get("https://www.linkedin.com/sales/")
        session_saver.save_session()
        print("Logger: DONE logging in")
    else:
        print(f"LOGGER: error: unknown error has occured")

    time.sleep(4)


def get_json():
    all_json_data = driver.find_element(By.CSS_SELECTOR, 'code[style="display: none"]')
    for i in all_json_data:
        i = i.get_attribute("innerHTML")
        if "metadata" in i:
            json_data = i
            json_data = json.loads(json_data)
            # break
    return json_data


def get_list_of_company():
    print("abc")


def debug_return_url(match_obj):
    return match_obj.url


def debug_print_all_urls(driver=driver):
    return list(map(debug_return_url, driver.requests))


def getCompanyList(query_url, output_file_name):
    print(f"Start crawling with query: {query_url}")
    serial_no = 1
    is_final_page = False
    current_page = 1
    # if button ... is disabled --- > reach_dead_end = True
    while not is_final_page:
        total_count = 0
        url = query_url + f"&page={current_page}"
        driver.get(url)

        items_in_page = None

        try:
            items_in_page = _get_element_strictly(
                ".artdeco-list__item.pl3.pv3 ", many=True
            )
        except NoSuchElementException:
            print(
                f"TODO: log into the system that no company found with the url: {url}"
            )

        # check if .artdeco-list__item.pl3.pv3 exists
        # check if '.t-14.flex.align-items-center.mlA.pl3' exists

        #  else raise error

        # while True:
        #     stop_1 = _get_element_loosely('li[class="artdeco-list__item pl3 pv3 "]')
        #     if stop_1:
        #         break
        #     stop_2 = _get_element_loosely('div[class="t-14 flex align-items-center"]')
        #     if stop_2:
        #         break
        #     stop_3 = _get_element_loosely(
        #         'div[class="t-14 flex align-items-center mlA pl3"]'
        #     )
        #     if stop_3:
        #         break
        time.sleep(random.randint(2, 3))

        limit_reach = _get_element_loosely('header[class="error-header"]')
        if limit_reach:
            print("error")  # break
        try:
            page_not_found = _get_element_loosely(".search-results__no-results")
            if page_not_found:
                break
        except:
            None
        try:
            page_not_found = _get_element_loosely(
                'div[class="illustration-spots-large empty-room"]'
            )
            if page_not_found:
                break
        except:
            None
        try:
            total_count_css = _get_element_strictly(
                'li[class^="artdeco-pagination__indicator"]'
            )
            total_count_css = total_count_css[len(total_count_css) - 1]
            total_count_css = total_count_css.get_attribute(
                "data-test-pagination-page-btn"
            )
            total_count = int(total_count_css) * 25
            if total_count >= 2500:
                total_count = _get_element_strictly(
                    'div[class="ml3 pl4 t-14 t-black--light flex _display-count-spacing_1igybl"]'
                )
        except:
            try:
                total_count = (
                    _get_element_strictly(".t-14.flex.align-items-center.mlA.pl3 span")
                    .text.replace("results", "")
                    .strip(" ")
                )
                if "K+" in total_count:
                    total_count = total_count.replace("K+", "")
                    # TODO: K+ is not nessessary 1000, it could be more
                    total_count = int(total_count) * 1000
                if "M+" in total_count:
                    total_count = total_count.replace("M+", "")
                    # TODO: K+ is not nessessary 1000, it could be more
                    total_count = int(total_count) * 1000000
            except:
                None
        all_data = driver.find_elements(
            By.CSS_SELECTOR, 'li[class^="artdeco-list__item"]'
        )

        items_per_page = len(all_data)
        scroll_count = 1
        # 🔴WIP

        while scroll_count <= items_per_page:
            # TODO: use seleniumwire to get response from api request
            driver.execute_script(
                "return arguments[0].scrollIntoView();",
                all_data[scroll_count - 1],
            )
            time.sleep(0.5)
            scroll_count += 3

        data_list = []
        for i in all_data:
            company_name = "-"
            company_link = "-"
            co_id = "-"
            company_industry = "-"
            company_location = "-"
            company_size = "-"
            all_tech = "-"
            tech_used = "-"
            co_description = "-"
            try:
                company_name = i.find_element(
                    By.CSS_SELECTOR,
                    'a[data-control-name="view_company_via_result_name"]',
                ).text
            except:
                None
            try:
                co_id = (
                    i.find_element(
                        By.CSS_SELECTOR,
                        'a[data-control-name="view_company_via_result_name"]',
                    )
                    .get_attribute("href")
                    .split("?")[0]
                    .split("/")
                )
                co_id = co_id[len(co_id) - 1]
            except:
                None
            try:
                company_link = (
                    i.find_element(
                        By.CSS_SELECTOR,
                        'a[data-control-name="view_company_via_result_name"]',
                    )
                    .get_attribute("href")
                    .split("?")[0]
                    .replace("sales/", "")
                )
            except:
                None
            try:
                company_industry = i.find_element(
                    By.CSS_SELECTOR, 'span[data-anonymize="industry"]'
                )[0].text
            except:
                None
            try:
                try:
                    cz = i.find_element(
                        By.CSS_SELECTOR, 'span[data-anonymize="company-size"]'
                    ).text
                except:
                    cz = ""
            except:
                None
            try:
                company_size = (
                    i.find_element(By.CSS_SELECTOR, 'a[data-anonymize="company-size"]')[
                        0
                    ]
                    .text.replace(" employees", "")
                    .replace(" employee", "")
                )
                if "K+" in company_size:
                    company_size = company_size.replace("K+", "")
                    company_size = int(company_size) * 1000
            except:
                None
            try:
                company_location = "-"
            except:
                None
            # try:
            #     co_description_more_btn=i.find_element(By.CSS_SELECTOR, 'div[class="inline-flex align-items-baseline"]')[0].find_element(By.CSS_SELECTOR, 'button')[0]
            #     co_description_more_btn.click()
            #     co_description=i.find_element(By.CSS_SELECTOR, 'div[class="inline-flex align-items-baseline"]')[0].find_element(By.CSS_SELECTOR, 'div')[0].text
            # except:
            #     None
            try:
                all_tech = "-"
            except:
                None
            try:
                tech_used = "-"
            except:
                None
            # try:
            #     current_page = driver.current_url
            # except:
            #     None
            data = [
                serial_no,
                current_page,
                company_link,
                co_id,
                company_name,
                company_industry,
                company_size,
                total_count,
            ]
            print(serial_no, co_id)
            serial_no = serial_no + 1
            data_list.append(data)
        write_output(output_file_name, data_list)

        is_final_page = True


def run(username, password, outfile="output.txt"):
    write_column_header(outfile)
    query_list = [
        "https://www.linkedin.com/sales/search/company?query=(filters%3AList((type%3AREGION%2Cvalues%3AList((id%3A102890719%2Ctext%3ANetherlands%2CselectionType%3AINCLUDED)%2C(id%3A100565514%2Ctext%3ABelgium%2CselectionType%3AINCLUDED)%2C(id%3A105117694%2Ctext%3ASweden%2CselectionType%3AINCLUDED)%2C(id%3A100456013%2Ctext%3AFinland%2CselectionType%3AINCLUDED)%2C(id%3A104042105%2Ctext%3ALuxembourg%2CselectionType%3AINCLUDED)%2C(id%3A104514075%2Ctext%3ADenmark%2CselectionType%3AINCLUDED)%2C(id%3A103819153%2Ctext%3ANorway%2CselectionType%3AINCLUDED)))%2C(type%3ACOMPANY_HEADCOUNT%2Cvalues%3AList((id%3AI%2Ctext%3A10%252C001%252B%2CselectionType%3AINCLUDED)%2C(id%3AH%2Ctext%3A5%252C001-10%252C000%2CselectionType%3AINCLUDED)))))&sessionId=T4CJnke3R3qVOg6Xyt3t6A%3D%3D"
    ]
    get_login_linkedin(username, password)

    for query in query_list:
        getCompanyList(query, outfile)
    driver.close()
    driver.quit()


if __name__ == "__main__":
    config_to_login()
