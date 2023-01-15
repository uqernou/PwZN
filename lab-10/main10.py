import requests
import re

from bs4 import BeautifulSoup
import time
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageFilter


url = "http://www.if.pw.edu.pl/~mrow/dyd/wdprir/"

def download(name):
    file = open(name, "wb")
    file.write(requests.get(url + name).content)
    file.close()
    picture2 = Image.open(name)
    picture2 = picture2.filter(ImageFilter.GaussianBlur(radius=5))
    picture2.save(name)
    picture2.close()
    picture = Image.open(name)
    picture = picture.convert('1')
    picture.save(name)
    picture.close()


if __name__ == '__main__':
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'html.parser')
    picture_links = soup.find_all('a', href=re.compile('.png'))
    picture_href = [img['href'] for img in picture_links]

    start = time.time()
    with ProcessPoolExecutor(24) as ex:
        futures = [ex.submit(download, picture_href[names]) for names in range(len(picture_href))]
    end = time.time()
    print(f'Czas pobierania przy osobnych procesach: {end - start}')

    start = time.time()
    for names in range(len(picture_href)):
        download(picture_href[names])
    end = time.time()
    print(f'Czas pobierania \'jak leci\': {end - start}')

# Czas pobierania przy osobnych procesach: 28.884482622146606
# Czas pobierania 'jak leci': 77.4077079296112
