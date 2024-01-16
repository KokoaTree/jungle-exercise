import requests
from bs4 import BeautifulSoup

def insert_all():
    # URL 읽고 HTML 받아오기
     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
     data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)
