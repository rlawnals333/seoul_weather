import requests
import csv
from datetime import datetime
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY") #보안 
CITY = "Seoul"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()
#print(data)

#온도, 습도, description

temp = data["main"]["temp"]
humidity = data["main"]["humidity"]
description = data["weather"][0]["description"]
timezone = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(temp,humidity,description, timezone)

#위의 4개의 데이터를 가지는 csv파일 생성!!
csv_filename = "seoul_weather.csv"
header = ["timezone","temp","humidity","description"] #timezone이 프라이머리 key로 사용가능

#csv가 존재하면 True 아니면 False
file_exist = os.path.isfile(csv_filename) #boolean 

#mode = "a" : if not file -> create / if is file: 그냥 쓰기 (덮어쓰기 x)
with open(csv_filename,"a",newline="") as file:
    writer = csv.writer(file)

    if not file_exist:# 헤더 없으면(파일이 존재하지 않으면)
        writer.writerow(header)

    writer.writerow([timezone,temp,humidity,description])

    print("csv 저장 완료!!")
