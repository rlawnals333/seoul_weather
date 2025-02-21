# html에서 투표받은 place, category, customMenu에서
# 선택 된 category, customMenu 중에 랜덤으로 선택하는 py파일을 만들어야함.
# html파일로 투표하는 인원은 총 4명, 예를 들어 4명 중 3명이 중식을 투표하고, 나머지 1명은 일식을 투표하였을때, 중식3표+일식1표에서 랜덤으로 카테고리를 하나 뽑아야함
# (참고로 html을 조원 4명에게 메일로 배포할것임)
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sqlite3

from flask import Flask, request, render_template, redirect, url_for, jsonify
import random
import json
import os
#from crawling import craw
import schedule
import time

url = "http://127.0.0.1:5000/vote"

#특정시간 vote 페이지 열기기
def open_web():
    driver = wb.Chrome()
    driver.get(url)     

    time.sleep(3600)
    driver.close()
task_test = schedule.every().day.at("11:50").do(open_web)

#global votes = {}
app = Flask(__name__)

VOTE_FILE = "votes.json"

# 투표 데이터 초기화 (처음 실행 시 파일이 없으면 생성)
if not os.path.exists(VOTE_FILE):
    with open(VOTE_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('vote_page_시간대상관없이됨.html')  # HTML 폼

@app.route('/vote', methods=['POST'])
def vote():
    
    
    place = request.form.get("place")
    category = request.form.get("category")
    custom_menu = request.form.get("customMenu") if category == "기타" else None
   
    
    # 투표 데이터 저장
    with open(VOTE_FILE, "r", encoding="utf-8") as f:
        votes = json.load(f)
    votes.append({
        "place": place,
        "category": category if category != "기타" else custom_menu
    })
    with open(VOTE_FILE, "w", encoding="utf-8") as f:
        json.dump(votes, f, ensure_ascii=False, indent=4)
    
   


    return redirect(url_for('result'))

@app.route('/result')
def result():
    with open(VOTE_FILE, "r", encoding="utf-8") as f:
        votes = json.load(f)

    if not votes:
        return "아직 투표된 데이터가 없습니다!"

    # 랜덤으로 하나의 카테고리 선택
    selected = random.choice([vote["category"] for vote in votes])

    return f"🎉 오늘의 점심 메뉴는: {selected} 🎉"
    

if __name__ == '__main__':
    app.run(debug=True)

# 오픈서버를 만들어서(ngrok), 각각 다른 기기로 접속한 사람들의 모든 투표가 json파일에 실시간으로 저장되게 해야함
