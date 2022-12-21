import json
import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self):
        self.extract_params()
        self.run_script()

    def extract_params(self):
        parser = argparse.ArgumentParser(description="Argument parser")
        parser.add_argument("-file", "--File", help="File to save JSON", type=str, required=False, default="none")
        argument = parser.parse_args()
        self.filename = argument.File
        # self.web_response = requests.get('https://www.filmweb.pl/serial/Wikingowie-2013-659055')
        self.data_json = []
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.option)
        self.driver.get("https://www.filmweb.pl/serial/Wikingowie-2013-659055")
        self.driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()
        time.sleep(4)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/button').click()
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight/10)')
        self.driver.find_element(By.XPATH, '//*[@id="site"]/div[4]/div[2]/div/div[2]/section/div/div/div[4]/div/div[1]/div/a[1]').click()
        self.ads = 0
        time.sleep(5)
        self.check_exists_by_xpath('//*[@id="sas_closeButonWrapper"]')
        for i in range(0, 35):
            time.sleep(0.025)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight*'+ str(10+i)+'/100)')

        self.web_response = self.driver.page_source


    def run_script(self):
        self.parse_web_app()
        self.read_json()

    def parse_web_app(self):
        soup = BeautifulSoup(self.web_response, 'html.parser')
        first_class = soup.find("div", class_="filmEpisodesListSection__list")
        second_class = first_class.find_all('div', {"class": "preview__header"})
        for div in second_class:
            odcinek = div.find("strong")
            tytul = div.find("span")
            self.data_json.append((odcinek.text.strip(), tytul.text.strip()))
        with open(f"{self.filename}.json", "w", encoding="utf-8") as file:
            json.dump(self.data_json, file, ensure_ascii=False, indent=4)

    def read_json(self):
        with open(f"{self.filename}.json", "r", encoding="utf-8") as data:
            print(json.dumps(json.loads(data.read()), ensure_ascii=False, indent=4))

    def check_exists_by_xpath(self, xpath):
        try:
            if self.driver.find_element(By.XPATH, xpath):
                self.driver.find_element(By.XPATH, xpath).click()
            self.ads = 1
        except NoSuchElementException:
            self.ads = 0

if __name__ == '__main__':
    scrapper = WebScrapper()