import datetime

from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle as oci
import json
import string
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt

oci.init_oracle_client(lib_dir=r"C:/Program Files/SQLPlus")
conn = oci.connect('admin/Dkdldpdjdb12@iairdb_medium')
cursor = conn.cursor()


def index(request):
    return render(request, 'olympicNow/index.html', {})


def sports(request):
    return render(request, 'olympicNow/sports.html', {})


def players(request):
    return render(request, 'olympicNow/players.html', {})


@csrf_exempt
def data(request):
    getjson = json.loads(request.body)
    startDate = getjson['startDate']
    endDate = getjson['endDate']
    sDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    eDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    cursor.execute("SELECT PNAME, SUM(PCOUNT) AS PCOUNT  FROM OLPNOW_PLAYERS WHERE RDATE >= :sDate AND RDATE <= :eDate GROUP BY PNAME ORDER BY PCOUNT DESC", sDate=sDate, eDate=eDate)
    result = cursor.fetchall()
    rsData =  { "pname": [x[0] for x in result ],
                   "pcount": [x[1] for x in result ] }
    cursor.execute("SELECT SNAME, SUM(SCOUNT) AS SCOUNT  FROM OLPNOW_SPORTS WHERE RDATE >= :sDate AND RDATE <= :eDate GROUP BY SNAME ORDER BY SCOUNT DESC", sDate=sDate, eDate=eDate)
    result = cursor.fetchall()
    rsSports = { "sname": [ x[0] for x in result ],
                 "scount": [ x[1] for x in result ] }
    rsData.update(rsSports)
    return JsonResponse(rsData)

@csrf_exempt
def getwc(request):
    rsData = json.loads(request.body)
    playersWc = {}
    sportsWc = {}
    imageName = ''
    for i in range(20):
        imageName += str(random.choice(string.ascii_lowercase + string.digits))
    sImageFileName = imageName + 's.png'
    pImageFileName = imageName + 'p.png'

    for i in range(len(rsData['pname'])):
        playersWc[rsData['pname'][i]] = rsData['pcount'][i]
    for i in range(len(rsData['sname'])):
        sportsWc[rsData['sname'][i]] = rsData['scount'][i]

    sportsWordcloud = WordCloud(font_path='olympicNow/Cafe24Ohsquare.ttf', background_color='white',
                                 width=1000, height=1000).generate_from_frequencies(sportsWc)
    playersWordcloud = WordCloud(font_path='olympicNow/Cafe24Ohsquare.ttf', background_color='white',
                                 width=1000, height=1000).generate_from_frequencies(playersWc)
    plt.axis('off')
    sportsWordcloud.to_file('static/images/wc/'+sImageFileName)
    playersWordcloud.to_file('static/images/wc/'+pImageFileName)
    returnData = {'simage':sImageFileName, 'pimage':pImageFileName}
    return JsonResponse(returnData)


@csrf_exempt
def getschart(request):
    getjson = json.loads(request.body)
    startDate = getjson['startDate']
    endDate = getjson['endDate']
    sDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    eDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    sName = getjson['sName']
    cursor.execute("SELECT TO_CHAR(RDATE, 'YY-MM-DD') AS RDATE, SCOUNT FROM OLPNOW_SPORTS WHERE SNAME=:sName AND RDATE >= :sDate AND RDATE <= :eDate ORDER BY RDATE",sDate=sDate, eDate=eDate, sName=sName)
    result = cursor.fetchall()
    getData = { "rdate": [ x[0] for x in result ],
                 "scount": [ x[1] for x in result ] }
    return JsonResponse(getData)


@csrf_exempt
def getpchart(request):
    getjson = json.loads(request.body)
    startDate = getjson['startDate']
    endDate = getjson['endDate']
    sDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    eDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    pName = getjson['pName']
    cursor.execute("SELECT TO_CHAR(RDATE, 'YY-MM-DD') AS RDATE, PCOUNT FROM OLPNOW_PLAYERS WHERE PNAME=:pName AND RDATE >= :sDate AND RDATE <= :eDate ORDER BY RDATE",sDate=sDate, eDate=eDate, pName=pName)
    result = cursor.fetchall()
    getData = { "rdate": [ x[0] for x in result ],
                 "pcount": [ x[1] for x in result ] }
    print(getData)
    return JsonResponse(getData)

