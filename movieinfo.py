import requests
import dotenv
import os
import datetime 
from pytz import timezone
import json

### 
#   설정파일(dotenv 패키지 사용) 로드
###
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

### 
#   시간관련(datetime, pytz 사용) 함수
###
def get_now():
  time_now = datetime.datetime.now(timezone("Asia/Seoul"))
  return time_now


def get_today() :
  time_today = get_now().strftime("%Y%m%d")
  return time_today


def get_yesterday() :
  time_yesterday = get_now() - datetime.timedelta(1)
  time_yesterday = time_yesterday.strftime("%Y%m%d")
  return time_yesterday

### 
#   boxoffice 관련 함수
###
def get_boxoffice_url() :
  kofic_api_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
  kofic_api_key = os.environ["kofic_api_key"]
  targetdt = get_yesterday()
  return f"{kofic_api_url}?key={kofic_api_key}&targetDt={targetdt}"


def get_dailyboxoffice():
  url = get_boxoffice_url()
  response = requests.get(url)
  response.encoding = "utf-8"
  result = json.loads(response.text)
  return result["boxOfficeResult"]["dailyBoxOfficeList"]


# dailyboxoffice top10을 딕셔너리 형태로 저장 -> 1~10위까지 어제날짜로 가져온다
def get_dailyboxoffice_top10():
  rank_movie = get_dailyboxoffice()
  rank_result = {}
  for i in rank_movie :
    rank_result[i["rank"]] = i["movieNm"] 
  return rank_result


###
#   firebase 연동 관련 함수
###

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("sixman-movie-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
  'databaseURL' : 'https://sixman-movie-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# 최초 db선택 위치(최상위)
ref = db.reference()

# firebase create, update요청(기본적으로 put을 이용하여 )
def set_dailyranking():
  dailyranking_ref = db.reference("dailyranking")
  dailyranking_ref.set({get_yesterday():get_dailyboxoffice_top10()})

def get_dailyranking():
  daily = get_yesterday()
  dailyranking_ref = db.reference(f"dailyranking/{daily}")
  result = dailyranking_ref.get()
  return result

print(get_dailyranking())