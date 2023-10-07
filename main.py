from distutils.debug import DEBUG
from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from flask_cors import CORS
from pytz import timezone 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security,SQLAlchemySessionUserDatastore,UserMixin,RoleMixin

DEBUG=True
app=Flask(__name__)
app.secret_key='hello'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.sqlite3"
db=SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

CORS(app,resources={r'/*':{'origins':'*'}})
db.init_app(app)
class User(db.Model): 
  __tablename__='User'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  username=db.Column(db.String(50),nullable=False)
  email=db.Column(db.String,unique=True)
  password=db.Column(db.String(20),nullable=False)
  
class Logging(db.Model):
  __tablename__='Logging'
  log_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
  id=db.Column(db.Integer,db.ForeignKey('User.id'))
  t_name=db.Column(db.String(50),nullable=False)
  t_type=db.Column(db.String(50))
  setting=db.Column(db.String(100))
  date=db.Column(db.DateTime,default=datetime.now)

class Event(db.Model):
  __tablename__='Event'
  event_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
  id=db.Column(db.Integer,db.ForeignKey('Logging.log_id'))
  when=db.Column(db.String(20),nullable=False)
  value=db.Column(db.String(100),nullable=False)
  notes=db.Column(db.String(50),nullable=False)
  date=db.Column(db.String(50),nullable=False)

users=[]
@app.route('/register',methods=["GET","POST"])
def make_login():
  response_object={'status':"success"}
  if request.method=='POST':
    post_data=request.get_json()
    users.append({
      'username':post_data.get('username'),
      'email':post_data.get('email'),
      'password':post_data.get('password')
    })
    response_object['message']='user added'
  else:
    response_object['register']=users  
  return jsonify(response_object)
  
if __name__=='__main__':
  app.run()
  