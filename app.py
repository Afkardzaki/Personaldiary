from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

mongodb_name = 'mongodb+srv://test:sparta@cluster0.hzfbzhd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(mongodb_name)
db = client.personal_diary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)
    
    doc = {
        'file':filename,
        'title':title_receive,
        'content':content_receive
    }

    db.diary.insert_one(doc)
    return jsonify({'msg': 'Data Saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)