from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as elemTree

# xml 파일 파싱해서 MongoDB 패스워드 가져오기
tree = elemTree.parse('keys.xml')
mongodb_pass = tree.find('string[@name="MongoDB_PASSWORD"]').text
client = MongoClient(f'mongodb+srv://swlah:{mongodb_pass}@cluster0.g93fmw7.mongodb.net/?retryWrites=true&w=majority')
db = client.todayscalorie

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/admin", methods=["POST"])
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

    return jsonify({'msg': '저장완료!'})

# 이미지 판별 함수
@app.route("/admin/imagecheck", methods=["POST"])
def image_check():
    imageurl_receive = request.form['imageurl_give']
    print(imageurl_receive)
    r = requests.get(imageurl_receive)
    print(r.headers['Content-Type'])
    if r.headers['Content-Type'] == 'image/jpeg' or ['Content-Type'] == 'image/gif87a' or ['Content-Type'] == 'image/gif89a' or ['Content-Type'] == 'image/png' or ['Content-Type'] == 'image/bmp' or ['Content-Type'] == 'image/tiff' or ['Content-Type'] == 'image/icon':
        return jsonify({"msg": "이미지입니다.", "status": "True"})
    else:
        return jsonify({"msg": "이미지가 아닙니다.", "status": "False"})

# @app.route("/admin/update", methods=["POST"])
# def admin_update():
#     imageurl_receive = request.form['imageurl_give']
#     foodname_receive = request.form['foodname_give']
#     calorie_receive = request.form['calorie_give']
#     describe_receive = request.form['describe_give']

#     doc = {
#         'imageurl': imageurl_receive,
#         'foodname': foodname_receive,
#         'calorie': calorie_receive,
#         'describe': describe_receive
#     }

#     db.foods.insert_one(doc)

#     return jsonify({'msg': '저장완료!'})

# @app.route("/admin/delete", methods=["POST"])
# def admin_delete():
#     imageurl_receive = request.form['imageurl_give']
#     foodname_receive = request.form['foodname_give']
#     calorie_receive = request.form['calorie_give']
#     describe_receive = request.form['describe_give']

#     doc = {
#         'imageurl': imageurl_receive,
#         'foodname': foodname_receive,
#         'calorie': calorie_receive,
#         'describe': describe_receive
#     }

#     db.foods.insert_one(doc)

#     return jsonify({'msg': '저장완료!'})

@app.route("/admin", methods=["GET"])
def admin_get():
    all_foods = list(db.foods.find({}, {'_id': False}))
    return jsonify({'result': all_foods})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
