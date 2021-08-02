import datetime
import json
import cx_Oracle as oci
import requests as rq
import math
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from konlpy.tag import Komoran
from bs4 import BeautifulSoup
import pandas

oci.init_oracle_client(lib_dir=r"C:/Program Files/SQLPlus")
conn = oci.connect('admin/Dkdldpdjdb12@iairdb_medium')
cursor = conn.cursor()

sports = ['골프', '권투', '근대5종', '농구', '럭비', '레슬링', '배구', '배드민턴', '사격', '사이클', '수영', '승마', '양궁', '역도',
          '요트', '유도', '육상', '조정', '체조', '축구', '카누', '탁구', '태권도', '테니스', '트라이애슬론', '펜싱', '하키', '핸드볼',
          '야구', '소프트볼', '마라톤', '클라이밍', '스케이트보드', '서핑', '가라테', '스위밍', '트램펄린', '비치발리볼', '다이빙']

players = ['박희준', '고진영', '김세영', '김시우', '김효주', '박인비', '임성재', '김선우', '김세희', '전웅태', '정진화', '강이슬',
           '김단비', '김정은', '박지수', '박지현', '박혜진', '배혜윤', '신지현', '안혜지', '윤예빈', '진안', '한엄지', '김광민',
           '김남욱', '김현수', '박완용', '이성배', '이진규', '장성민', '장용흥', '장정민', '정연식', '최성덕', '안드레진',
           '한건규', '김민석', '류한수', '김수지', '김연경', '김희진', '박은진', '박정아', '안혜진', '양효진', '염혜선', '오지영',
           '이소영', '정지윤', '표승주', '공희용', '김가은', '김소영', '서승재', '신승찬', '안세영', '이소희', '채유정', '최솔규',
           '허광희', '오연지', '임애지', '곽정혜', '권은지', '김모세', '김민정', '김보미', '김상도', '남태윤', '박희문', '배상희',
           '송종호', '이종준', '조은영', '진종오', '추가은', '한대윤', '나아름', '이혜진', '김서영', '김우민', '문승우', '안세현',
           '이유연', '이은지', '이주호', '이호준', '정현영', '조성재', '한다경', '황선우', '권하림', '김수지', '김영남', '김영택',
           '우하람', '서채현', '천종원', '김동선', '강민호', '강백호', '고영표', '고우석', '김민우', '김진욱', '김현수', '김혜성',
           '박건우', '박세웅', '박해민', '양의지', '오승환', '오재일', '오지환', '원태인', '이의리', '이정후', '조상우', '차우찬',
           '최원준', '최주환', '허경민', '황재균', '강채영', '김우진', '김제덕', '안산', '오진혁', '장민희', '강윤희', '김수현',
           '유동주', '이선미', '진윤성', '한명목', '함은지', '박건우', '조성민', '조원우', '하지민', '강유정', '곽동한', '김민종',
           '김성연', '김원진', '김지수', '박다솔', '안바울', '안창림', '윤현지', '이성호', '조구함', '한미진', '한희주', '심종섭',
           '안슬기', '오주한', '우상혁', '진민섭', '최경선', '최병광', '정혜정', '김한솔', '류성현', '신재환', '양학선', '여서정',
           '이윤서', '이준호', '강윤성', '권창훈', '김동현', '김재우', '김진규', '김진야', '박지수', '설영우', '송민규', '송범근',
           '안준수', '안찬기', '엄원상', '원두재', '이강인', '이동경', '이동준', '이상민', '이유현', '정승원', '정태욱', '황의조',
           '조광희', '신유빈', '이상수', '장우진', '전지희', '정영식', '최효주', '심재영', '이다빈', '이대훈', '이아름', '인교돈',
           '장준', '권순우', '강영미', '구본길', '권영준', '김정환', '김준호', '김지연', '마세건', '박상영', '서지연', '송세라',
           '송재호', '오상욱', '윤지수', '이광현', '이혜인', '전희숙', '최수연', '최인정', '강경민', '강은혜', '김보은', '김윤지',
           '김진이', '류은희', '심해인', '원선필', '이미경', '정유라', '정지인', '정진희', '조하랑', '주희', '최수민']

url = 'https://api-gw.sports.naver.com/news/articles/tokyo2020'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}

dateIndex = pandas.date_range(start='20210728', end='20210728')
dateList = dateIndex.strftime("%Y%m%d").tolist()

for searchDate in dateList:

    dateDate = datetime.datetime.strptime(searchDate, "%Y%m%d").date()

    params = {'sort': 'latest', 'date': searchDate, 'page': 10000, 'isPhoto': 'N'}
    source = rq.get(url, params=params, headers=headers)
    endPage = math.ceil(json.loads(source.content)['result']['totalCount']/20)
    result = ''
    for i in range(1, endPage):
        params = {'sort': 'latest', 'date': searchDate, 'page': i, 'isPhoto': 'N'}
        source = rq.get(url, params=params, headers=headers)
        getList = json.loads(source.content)['result']['newsList']
        for getList in getList:
            getTitle = getList['title']
            result += getTitle + ' '

    # nouns = Komoran(userdic='userdic.txt').nouns(result)
    nouns = Komoran().nouns(result)
    getSports = []
    getPlayers = []
    getTotal = []
    for n in nouns:
        getTotal.append(n)
        if n in sports:
            getSports.append(n)
        if n in players:
            getPlayers.append(n)

    cntSports = Counter(getSports).most_common()
    cntPlayers = Counter(getPlayers).most_common()
    cntTotal = Counter(getTotal).most_common()
    print(cntPlayers)
#     for n, c in cntSports:
#         cursor.execute("INSERT INTO OLPNOW_SPORTS VALUES (:RDATE, :SNAME, :SCOUNT)", [dateDate, n, c])
#     for n, c in cntPlayers:
#         cursor.execute("INSERT INTO OLPNOW_PLAYERS VALUES (:RDATE, :PNAME, :PCOUNT)", [dateDate, n, c])
#
# conn.commit()
# conn.close()
# tagSports = {}
# tagPlayers = {}
#
# for n, c in cntSports:
#     tagSports[n] = c
#
# for n, c in cntPlayers:
#     tagPlayers[n] = c
#
# print(cntSports)
# print(tagSports)
#
# wcResult = WordCloud(font_path='Cafe24Ohsquare.ttf', background_color='white',
#                      max_font_size=768, width=3840, height=2160).generate_from_frequencies(tagPlayers)
# plt.axis('off')
# plt.imshow(wcResult, interpolation='bilinear')
# plt.show()
