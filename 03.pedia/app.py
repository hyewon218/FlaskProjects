
# 영화 url과 코멘트를 받아서 url을 기반으로 제목, 설명, 이미지를 가지고 온 다음에 url코멘트까지 다 해서 DB에 넣기

from bs4 import BeautifulSoup
import requests
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# dbprac에서 복붙
ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.rigwvzf.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    # url,코멘트 받기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    # url을 기반으로 크롤링
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
        'comment': comment_receive,
        'star': star_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg': '저장완료!'})

# 서버만들기(서버 : 영화를 다 가져다 내려주는 역할)
@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':False}))
    # {'result': all_movies} = data
    return jsonify({'result': all_movies})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

