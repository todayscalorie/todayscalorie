import sys
import json
import random #세션이나 Secret_Key값을 위해
import certifi
import requests
import jwt
import datetime
import xml.etree.ElementTree as elemTree
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session, redirect

# xml 파일 파싱해서 MongoDB 패스워드 가져오기
tree = elemTree.parse('keys.xml')
# 몽고 db pw
mongodb_pass = tree.find('string[@name="MongoDB_PASSWORD"]').text

# 시크릿 키
SECRET_KEY = tree.find('string[@name="SECRET_KEY"]').text

client = MongoClient(f'mongodb+srv://swlah:{mongodb_pass}@cluster0.g93fmw7.mongodb.net/?retryWrites=true&w=majority')
db = client.todayscalorie

app = Flask(__name__)

######################
##### 메인 페이지 #####
######################
# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

# 메인 페이지 정보 가져오기
@app.route("/get", methods=["GET"])
def foodlist_get():
    all_foods = list(db.foods.find({}, {'_id': False}))
    return jsonify({'result': all_foods})

# 칼로리 계산하기
@app.route("/get/caclkcal", methods=["POST"])
def caclkcal_get():
    foodkcal = request.form['foodrange_give']
    print(foodkcal)
    # db.foods.update_one({'id': id_receive},{'$set':{'status': 'in progress'}})
    # result = db.foods.find({'id' : id_receive})[0]['status']

    return jsonify({'result': 'result'})

#################################
##### 로그인, 회원가입 페이지 #####
#################################
# 로그인 페이지
@app.route('/login')
def login_main():
    return render_template('login.html')

# 로그인 페이지 Post
@app.route('/login/signin', methods=['POST']) #로그인 기능 구현
def login():
    login_user_id = request.form['login_id']
    login_user_pw = request.form['login_pw']
    
    pw_hash = hashlib.sha256(login_user_pw.encode('utf-8')).hexdigest() 
    print("해시까지 걸었고")

    # 임시로 Id 와 Pw라는 변수에 입력된
    user = db.login.find_one({'userId':login_user_id}, {'userPwd':pw_hash})
    print("user값 가져왔고")
    
    if user is not None: # 등록되어있는 데이터 값을 넣었을때 
        payload = {
            'id': login_user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)
        print("잘 되고 있다")
        return jsonify({'result': 'success','token' : token, 'msg' : '로그인에 성공했습니다.'})
        
    else: # DB에 없는 로그인 정보를 넣었을때
        print("뭔가 잘못되었다.")
        return jsonify({'result': 'fail', 'msg' : '로그인에 실패하였습니다.'})

# 회원가입 페이지   
@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/register/signup", methods=["POST"]) # 회원가입 API
def join():
    user_id = request.form['login_id'] #join.html의 user_sign_up함수에서 id값을 받아 변수에 저장
    user_pw = request.form['login_pw'] #join.html의 user_sign_up함수에서 pw값을 받아 변수에 저장
    nick_name = request.form['nickname'] #join.html의 user_sign_up함수에서 nickname 받아 변수에 저장

    # hash 라이브러리를 활용해서 비밀번호값을 암호화해서 넣는다. 
    # 비밀번호를 해시함수로 암호화 해서 데이터베이스에 저장하는 역할.
    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest() 
    
    doc = {
        'userId' : user_id,
        'userPwd' : pw_hash,
        'nickname' : nick_name
    }
    db.login.insert_one(doc) # 받은 값을 doc안에 딕셔너리 형태로 넣어서 MongoDB에 저장한다.
    print("잘 들어갔나?")
    return jsonify({'result' : '유저 등록 완료!', 'page' : 'login'})
    # 유저 등록이 되고 page를 login 화면으로 옮기기 위해 page 키 추가

########################
##### 어드민 페이지 #####
########################
# 어드민 페이지
@app.route('/admin')
def admin_home():
    return render_template('admin.html')

# 어드민 페이지 정보 가져오기
@app.route("/admin/get", methods=["GET"])
def admin_get():
    all_foods = list(db.foods.find({}, {'_id': False}))
    return jsonify({'result': all_foods})

# 어드민 페이지 음식 카드 등록
@app.route("/admin/post", methods=["POST"])
def admin_post():
    imageurl_receive = request.form['imageurl_give']
    foodname_receive = request.form['foodname_give']
    calorie_receive = request.form['calorie_give']
    describe_receive = request.form['describe_give']

    doc = {
        'imageurl': imageurl_receive,
        'foodname': foodname_receive,
        'calorie': calorie_receive,
        'describe': describe_receive
    }

    db.foods.insert_one(doc)

    data = str(db.foods.find_one(doc)['_id'])
    db.foods.update_one(doc,{'$set':{'id': data}})
    db.foods.update_one(doc,{'$set':{'status': 'complete'}})

    return jsonify({'msg': '저장완료!'})

# 등록하고자 하는 이미지 유효성 검사
@app.route("/admin/imagecheck", methods=["POST"])
def image_check():
    imageurl_receive = request.form['imageurl_give']
    r = requests.get(imageurl_receive)
    # print(r.headers['Content-Type'])
    if r.headers['Content-Type'] == 'image/jpeg' or ['Content-Type'] == 'image/gif87a' or ['Content-Type'] == 'image/gif89a' or ['Content-Type'] == 'image/png' or ['Content-Type'] == 'image/bmp' or ['Content-Type'] == 'image/tiff' or ['Content-Type'] == 'image/icon':
        return jsonify({"msg": "이미지입니다.", "status": "True"})
    else:
        return jsonify({"msg": "이미지가 아닙니다.", "status": "False"})

# 등록된 카드 정보 변경 시작 - 수정 가능 상태로 변경 됨 foodname, calorie, describe
@app.route("/admin/updatestart", methods=["POST"])
def admin_update_start():
    id_receive = request.form['id_give']
    db.foods.update_one({'id': id_receive},{'$set':{'status': 'in progress'}})
    result = db.foods.find({'id' : id_receive})[0]['status']

    return jsonify({'result': result})

# 등록된 카드 정보 변경 완료 - 수정 불가 상태로 변경 됨 -> DB에 데이터 저장
@app.route("/admin/updatecomplete", methods=["POST"])
def admin_update_complete():
    id_receive = request.form['id_give']
    foodname_receive = request.form['foodname_give']
    calorie_receive = request.form['caloriegive']
    describe_receive = request.form['describe_give']

    db.foods.update_one({'id': id_receive},{'$set':{'status':'complete','foodname':foodname_receive,'calorie':calorie_receive,'describe':describe_receive}})
    db.foods.update_one({'id': id_receive},{'$set':{'foodname':foodname_receive}})
    db.foods.update_one({'id': id_receive},{'$set':{'calorie':calorie_receive}})
    db.foods.update_one({'id': id_receive},{'$set':{'describe':describe_receive}})
    result = db.foods.find({'id' : id_receive})[0]['status']

    return jsonify({'result': result})

# 등록된 카드 정보 삭제
@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    id_receive = request.form['id_give']
    db.foods.delete_one({'id':id_receive})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
