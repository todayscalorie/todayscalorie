from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as elemTree

# xml 파일 파싱
tree = elemTree.parse('keys.xml')
mongodb_pass = tree.find('string[@name="MongoDB_PASSWORD"]').text

app = Flask(__name__)

client = MongoClient(f'mongodb+srv://swlah:{mongodb_pass}@cluster0.g93fmw7.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': ogtitle,
        'desc': ogdesc,
        'image': ogimage,
        'comment': comment_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg': '저장완료!'})


@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({}, {'_id': False}))
    return jsonify({'result': all_movies})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
