from ext import app, db
from models import Post, Comment, User

with app.app_context():
    db.drop_all()
    db.create_all()
    
    admin_user = User(username="admin", password="admin123.", role="Admin")
    db.session.add(admin_user)
    db.session.commit()

