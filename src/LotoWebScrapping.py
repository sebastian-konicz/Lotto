from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from mechanize import Browser
import requests
import glob
import pandas as pd
from pathlib import Path


def main(dir):
    # SCRAPPING DATA FROM THE NET
    # Downloading rental data from the page
    pageLotto = requests.get("https://www.lotto.pl/lotto/wyniki-i-wygrane/wyszukaj")
    htmlLotto = BeautifulSoup(pageLotto.content, 'html.parser')
    inputLotto = htmlLotto.find("input", id='wyszukaj-wyniki-form-datepicker-popup-0')

    response = fetch('2020-01-02')

    resultsHTML = BeautifulSoup(response, 'html.parser')
    results = resultsHTML.find_all("tr", class_="wynik")

    for result in results:
        lotteryType = result.find("img").get("alt")

        if lotteryType != 'Super Szansa':
            numbers = result.find('div', class_='sortrosnaco').find_all('span')
            resultNumbers = []
            for number in numbers:
                resultNumber = number.text
                resultNumbers.append(resultNumber)
        else:
            numbers = result.find_all('span')
            resultNumbers = []
            for number in numbers:
                resultNumber = number.text
                resultNumbers.append(resultNumber)

        print(lotteryType)
        print(resultNumbers)

def fetch(date):
    # Creating browser object
    br = Browser()
    br.open('https://www.lotto.pl/lotto/wyniki-i-wygrane/wyszukaj')

    # Getting form
    br.form = list(br.forms())[1]

    # Getting date form
    dateForm = br.form.find_control('data_losowania[date]')

    # Setting value
    dateForm.value = date

    # Submiting form
    response = br.submit()

    return response


if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)