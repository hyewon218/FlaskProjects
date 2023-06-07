from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.rigwvzf.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    # 닉네임과 응원댓글 받아오기
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name':name_receive,
        'comment':comment_receive
    }
    db.fan.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

# /guestbook으로 들어옴({'result': all_comments}를 받아옴) 
@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    # 몽땅 가져와서 내려주기(여러개 찾기)
    all_comments = list(db.fan.find({},{'_id':False}))
    return jsonify({'result': all_comments})

if __name__ == '__main__':
   app.run()


