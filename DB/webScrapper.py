import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # 패키지 install 먼저

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.

def insert_all():
    # URL 읽고 HTML 받아오기
     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
     data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)
    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
     soup = BeautifulSoup(data.text, 'html.parser')
    # select를 이용해서, li들을 불러오기
     movies = soup.select('#morColl > div.coll_cont > div > ol > li')
     print(len(movies))

    # movies (li들) 의 반복문을 돌리기
     for movie in movies:
        # movie 안에 a가 있으면,
        # 조건을 만족하는 첫번째 요소, 없으면 None을 반환
        tag_element = movie.select_one('#morColl > div.coll_cont > div > ol > li:nth-child(1) > div.wrap_cont > div')
        if not tag_element:
            continue
        title = tag_element.text # a태그 사이의 텍스트 가져오기

        tag_element = movie.select_one('#morColl > div.coll_cont > div > ol > li:nth-child(1) > div.wrap_cont > dl:nth-child(3) > dd')
        if not tag_element:
            continue
        open_date = tag_element.text
        
        # [연.월.일] 형태에서 [연, 월, 일] 추출하기
        # . 을 기준으로 split 한뒤 각각 문자형태에서 숫자형태로 변경
        date_elements = open_date.split('.')
        if len(date_elements) == 3:
            (open_year, open_month, open_day) = [int(element) for element in date_elements]
        else:
            continue  # 형식에 맞지 않는 데이터는 건너뜁니다.

        # (open_year, open_month, open_day) = [int(element) for element in date_elements]

        # 개봉 연도 "22"가 아닌 "2022" 형태로 바꾸기 위해 2000 더하기
        # open_year += 2000

        # 누적 관객수 얻어내기, '783,567명'과 같은 형태
        tag_element = movie.select_one('#morColl > div.coll_cont > div > ol > li:nth-child(1) > div.wrap_cont > dl:nth-child(4) > dd')
        if not tag_element:
            continue
        viewers = tag_element.findChild(string=True, recursive=False)
        viewers = int(''.join([c for c in viewers if c.isdigit()]))

        doc = {
            'title': title,
            'open_year': open_year,
            'open_month': open_month,
            'open_day': open_day,
            'viewers': viewers
        }
        db.movies.insert_one(doc)
        print('완료: ', title, open_year, open_month, open_day, viewers)

if __name__ == '__main__':
    # db.movies.drop() # 기존 movies 콜렉션 삭제
    # insert_all() # 영화 사이트를 scrapping해서 db에 채우기
    print(insert_all())

