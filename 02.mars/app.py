from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# 몽고db와 연결
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.rigwvzf.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def mars_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']
    
    # 저장하기
    doc = {
        'name':name_receive,
        'address':address_receive,
        'size':size_receive
    }
    db.mars.insert_one(doc)
    
    return jsonify({'msg':'저장완료!'})

@app.route("/mars", methods=["GET"])
def mars_get():
    # db에 있는 모든 데이터를 다 가져와라
    mars_data = list(db.mars.find({},{'_id':False}))
    # 클라이언트로 내려준다
    return jsonify({'result':mars_data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)


