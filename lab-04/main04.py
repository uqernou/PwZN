import json
import argparse
import requests

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
        self.web_response = requests.get('https://www.filmweb.pl/serial/Wikingowie-2013-659055/season/6')
        self.data_json = []

    def run_script(self):
        self.parse_web_app()
        self.read_json()

    def parse_web_app(self):
        soup = BeautifulSoup(self.web_response.text, 'html.parser')
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


if __name__ == '__main__':
    scrapper = WebScrapper()
