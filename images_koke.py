import requests
from bs4 import BeautifulSoup
import urllib.request

URL = "https://biz.koke.kr/products/1089"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
}

res = requests.get(URL, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

product_img_url = soup.select_one('#repImageContainer > img')['src']
urllib.request.urlretrieve(product_img_url, "이미지.jpg")