import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from datetime import datetime, timedelta
import re
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://sparta:a072a072@cluster0.fmlpq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template('index.html', user_info=user_info, user_id=payload["id"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    rpw_receive = request.form['rpw_give']
    id_num = list(db.uesr.find({}, {'id': False}))  # 가입시 넘버 부여 카운트 1로 시작
    count = len(id_num) + 1

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    if len(id_receive) < 5 or len(id_receive) > 10 and not re.findall("[0-9]+", id_receive) and not \
            re.findall("[a-z]", id_receive):
        # flash("아이디 5자 이상 입력.", category="error")
        return jsonify({'result': '아이디 형식이 일치하지 않습니다.'})

    elif len(pw_receive) < 8 or len(pw_receive) > 20 and not re.findall("[0-9]+", pw_receive) and not \
            re.findall("[a-z]", pw_receive) or not re.findall("[~!@#$%^&*(),<.>/?]+", pw_receive):
        # flash("영문과 숫자로 조합하여 8~20자의 비밀번호", category="error")
        return jsonify({'result': '비밀번호 형식이 일치하지 않습니다.'})

    elif len(name_receive) < 2:
        # flash("이름은 2자 이상 입력.", category="error")
        return jsonify({'result': '이름은 형식이 일치하지 않습니다.'})

    elif pw_receive != rpw_receive:
        # flash("비밀번호와 비밀번호재입력이 서로 다릅니다.", category="error")
        return jsonify({'result': '비밀번호와 비밀번호재입력이 서로 다릅니다.'})
    else:

        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'name': name_receive, 'num': count})
    return jsonify({'result': 'success'})


# DB dnt EXIST 중복값 확인 FINE 사용으로 중복없으면 false, 있으면 true
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    exists = bool(db.user.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    db.user.update_one({'num': int(1)}, {'$inc': {'num': + int(1)}})  # 디비 업데이트 구분수정
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    else:  # 찾지 못하면
        return jsonify({'result': 'fail', 'msg': '아이디 및 비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://comic.naver.com/webtoon/genre?genre=comic', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

webtoons = soup.select('#content > div.list_area > ul > li')

L = (len(webtoons))
webtoon_list = []
x = 0
for webtoon in webtoons:
    x = x + 1
    title = webtoon.select_one('dt > a')['title']
    # 제목
    image = webtoon.select_one('div > a > img')['src']
    # 썸네일
    star1 = webtoon.select_one('div > strong').text
    star = float(star1)
    # 별점(정수)
    artist = webtoon.select_one('dl > dd.desc > a').text
    # 작가
    date = webtoon.select_one('dl > dd.date2').text.strip()
    # 완결날짜
    link = webtoon.select_one('dt > a')['href']
    # 링크
    temp_list = [x, title, image, star, artist, date, link, int(star), star - int(star)]
    webtoon_list.append(temp_list)


@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})


@app.route("/webtoon", methods=["GET"])
def webtoon_get():
    print(webtoon_list)
    return jsonify({'webtoon': webtoon_list})


@app.route('/review')
def review():
    return render_template('review.html')


@app.route("/review/bucket", methods=["POST"])
def bucket_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.user.find_one({'id': payload['id']})
        bucket_receive = request.form['bucket_give']
        smile_receive = request.form['smile_give']
        date_receive = request.form["date_give"]
        title_receive = request.form["title_give"]

        bucket_list = list(db.bucket.find({}, {'_id': False}))
        count = len(bucket_list) + 1

        doc = {
            'num': count,
            'title': title_receive,
            'bucket': bucket_receive,
            'smile': smile_receive,
            'ID': user_info['id'],
            'date': date_receive
        }
        print("#1", doc)
        db.bucket.insert_one(doc)
        return jsonify({'msg': '리뷰가 등록되었습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/review/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제되었습니다.'})


@app.route("/review/bucket", methods=["GET"])
def bucket_get():
    title = request.args["title"]
    all_list = list(db.bucket.find({"title": title}, {'_id': False}))
    print(title, all_list)
    return jsonify({'list': all_list})


@app.route('/mypage')
def go_mypage():
    # 마이페이지로이동 (현재는 메인페이지와 연동을 하지않아 더보기 버튼으로 대체)
    return render_template('mypage.html')


@app.route('/test', methods=["GET"])
def call_info():
    call_id = request.args['info_id']
    #
    info = list(db.user.find({'id': call_id}, {'_id': False}))
    reviews = list(db.bucket.find({'ID': call_id}, {'_id': False}))
    count = len(reviews)
    call_name = info[0]['name']
    if count == 0:
        review_1 = {"title": 'None', "bucket": 'None'}
        review_2 = {"title": 'None', "bucket": 'None'}
    elif count == 1:
        review_1 = reviews[0]
        review_2 = {"title": 'None', "bucket": 'None'}
    else:
        review_1 = reviews[0]
        review_2 = reviews[1]

    print(count, review_1, review_2)
    return jsonify({'name': call_name, 'count': count, 'review_1': review_1, 'review_2': review_2, 'myreview': reviews})


@app.route('/pw_change', methods=["POST"])
def pw_change():
    newpw = request.form['new_pw']
    orgpw = request.form['org_pw']
    pw = hashlib.sha256(orgpw.encode('utf-8')).hexdigest()
    npw = hashlib.sha256(newpw.encode('utf-8')).hexdigest()
    id = request.form['id']
    print(id, pw)
    user = db.user.find_one({"id": id, "pw": pw})
    print(user)
    if user is not None:
        db.user.update_one({'id': id}, {'$set': {'pw': npw}})
        return jsonify({'msg': "비밀번호 변경완료", 'key': 0})
    else:
        return jsonify({'msg': "기존 비밀번호가 일치하지 않습니다.", 'key': 1})


@app.route('/byebye', methods=["POST"])
def byebye():
    id = request.form['id']
    pw1 = request.form['pw']
    pw = hashlib.sha256(pw1.encode('utf-8')).hexdigest()
    user = db.user.find_one({"id": id, "pw": pw})
    if user is not None:
        db.user.delete_one({"id": id, "pw": pw})
        return jsonify({'msg': '회원님의 탈퇴가 완료되었습니다.', 'key': 0})
    else:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.', 'key': 1})


@app.route('/myreview')
def go_myreview():
    # 마이페이지로이동 (현재는 메인페이지와 연동을 하지않아 더보기 버튼으로 대체)
    return render_template('myreview.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
