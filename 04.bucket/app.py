# 서버쪽(받는쪽)
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.rigwvzf.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    # bucket_give라는 데이터를 찾아서 bucket_receive라는 변수에 넣는다.
    bucket_receive = request.form['bucket_give']
    #document 만들기
    doc = {
        'bucket' : bucket_receive,
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})
    
# /bucket으로 들어옴('result': all_buckets}를 받아옴)
@app.route("/bucket", methods=["GET"])
def bucket_get():
    # db에서 여러개 찾기
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)


