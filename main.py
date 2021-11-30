from typing import KeysView
from flask import Flask,request
import json
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

#object for the flask

app=Flask(__name__)

#configeration

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'


#object for SQLAlchemy

db=SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(100))
    def __init__(self,url):
        self.url=url 

@app.route('/index/',methods=['POST'])
def index():
    data = request.args.get('url')

    #var = request.get_json(force=True)
    #data = json.loads(request.data)
    print(data)
    user=User(data)
    db.session.add(user)
    db.session.commit()

    return '<h1> Added New Url </h1>'

@app.route('/get/<url>',methods=["GET"])
def get(url):
    user =User.query.filter_by(url=url)
    if user.count():
        if user!=0:
            return ({'message':'this is malware url'})
        else:
            return ({'message':'url allowed'})
    return ({'message':'url allowed'})
            
    
@app.route('/upload',methods=['POST'])
def upload():
    
    value = request.files['file']
    for post in value:
        if not post:
            return "No file uploaded",400
        newFile = User(post)
        db.session.add(newFile)
        db.session.commit()
    return 'Saved successfully'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)