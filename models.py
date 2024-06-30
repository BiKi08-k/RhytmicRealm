from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db, login_manager

class Base_Model():
     
    def add(self):
        db.session.add(self)
        db.session.commit()


    def remove(self):
         db.session.delete(self)
         db.session.commit()

    @staticmethod
    def save():
         db.session.commit()
     
               

class User(db.Model, UserMixin, Base_Model):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())  
    prof_pic = db.Column(db.String(), default="default_prof_pic.jpg") 
    role = db.Column(db.String()) 

    def __init__(self, username, password, role="Guest"):
         self.username = username
         self.password = generate_password_hash(password)
         self.role = role


    def check_password(self, password):
         return check_password_hash(self.password, password)
         

@login_manager.user_loader   
def load_user(user_id):
        return User.query.get(user_id)

class Post(db.Model, Base_Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    post = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    post_type=db.Column(db.String(), nullable=False)



class Comment(db.Model, Base_Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id") )


