from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import warnings
import time
warnings.filterwarnings(action='ignore')

# 드라이버 불러오기
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 메인 페이지
url = 'https://biz.koke.kr/products?filters=%7B%22categoryGroup%22%3A%22WholeBean%22%7D'
driver.get(url) # go to website
time.sleep(2)

links = [] # 제품 링크 리스트

# 약 4분 30초 소요
for i in range(31):
    raw = driver.find_elements(By.TAG_NAME,"img")
    link_elements = raw[0].find_elements(By.TAG_NAME,'a') 
    href_links = [link.get_attribute('href') for link in link_elements]
    links = links + href_links # 현재 페이지에 있는 상품 가져오기
    time.sleep(5)

    if i is not 30:
        button = driver.find_elements(By.CSS_SELECTOR ,"button.text-gray-500.bg-white.border.border-gray-200.koke-button")
        print(len(button))
        button[-1].click()
        time.sleep(7)

links = set(links)
print(len(links)) # 총 556개
links

def get_product_images(links):
    product_images = []
    
    for link in links:
        driver.get(link)
        time.sleep(3)
        
        # 이미지를 가져올 CSS 선택자를 사용하십시오. 해당 웹 사이트의 구조에 따라 수정해야 할 수 있습니다.
        image_elements = driver.find_elements(By.TAG_NAME,"img")
        
        # 이미지 URL을 가져와서 리스트에 추가합니다.
        for image_element in image_elements:
            image_url = image_element.get_attribute('src')
            product_images.append(image_url)
    
    return product_images

# 위에서 수집한 제품 링크를 사용하여 제품 이미지를 가져옵니다.
product_images = get_product_images(links)

# 결과를 출력하거나 저장하는 등의 추가 작업을 수행할 수 있습니다.
# 예를 들어, 이미지 URL을 파일로 저장하려면 다음과 같이 할 수 있습니다.
import requests
import os

def download_images(links, save_directory):
    # 이미지를 저장할 디렉토리를 만듭니다.
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            # 이미지 파일 이름을 추출하거나 지정합니다.
            image_filename = os.path.join(save_directory, 'image{}.jpg'.format(links.index(link)))
            
            # 이미지를 파일로 저장합니다.
            with open(image_filename, 'wb') as file:
                file.write(response.content)
            print(f"이미지 저장 완료: {image_filename}")
        else:
            print(f"이미지 다운로드 실패: {link}")

# 위에서 수집한 제품 링크를 사용하여 제품 이미지를 다운로드합니다.
save_directory = 'images'  # 이미지를 저장할 디렉토리
download_images(links, save_directory)