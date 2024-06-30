from flask import render_template, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from forms import RegisterForm, LoginForm, PostForm, CommentForm
from models import Post, Comment, User
from os import path
from ext import app,db

@app.context_processor
def inject_user_id():
    user_id = current_user.id if current_user.is_authenticated else None
    return dict(user_id=user_id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/music_theory')
@login_required
def music_theory():
    admin_posts = Post.query.join(User).filter(Post.post_type == "theory", User.role == "Admin").all()
    comun_posts = Post.query.join(User).filter(Post.post_type == "theory", User.role == "Guest").all()
    return render_template('music_theory.html', admin_posts=admin_posts, comun_posts=comun_posts)


@app.route('/production')
@login_required
def music_production():
    admin_posts = Post.query.join(User).filter(Post.post_type == "production",User.role == "Admin").all()
    comun_posts = Post.query.join(User).filter(Post.post_type == "production", User.role == "Guest").all()
    return render_template('production.html', admin_posts=admin_posts, comun_posts=comun_posts)

@app.route('/mixing')
@login_required
def music_mixing():
    admin_posts = Post.query.join(User).filter(Post.post_type == "mixing",User.role == "Admin").all()
    comun_posts = Post.query.join(User).filter(Post.post_type == "mixing", User.role == "Guest").all()
    return render_template('mixing.html', admin_posts=admin_posts, comun_posts=comun_posts)

@app.route('/mastering')
@login_required
def music_mastering():
    admin_posts = Post.query.join(User).filter(Post.post_type == "mastering",User.role == "Admin").all()
    comun_posts = Post.query.join(User).filter(Post.post_type == "mastering", User.role == "Guest").all()
    return render_template('mastering.html', admin_posts=admin_posts, comun_posts=comun_posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        elif not user :
            flash("You aren't registered", 'danger')   
        else:
            flash('Incorrect Password', 'danger')
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            new_user.add()
            return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, post=form.post.data, user_id=current_user.id, post_type=form.post_type.data )
        if form.image.data:
            image = form.image.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            new_post.image = image.filename
        new_post.add()
        return redirect('/forum') 
    posts = Post.query.filter(Post.post_type == "general").all()
    users_by_id = {user.id: user for user in User.query.all()}
    for post in posts:
        post.user = users_by_id.get(post.user_id)
    return render_template('gen_forum.html', form=form, posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post= Post.query.get(post_id)
    user = User.query.get(post.user_id)
    if post:  
        form = CommentForm()
        if form.validate_on_submit():
            new_com = Comment(text=form.comment.data, post_id=post_id, user_id=current_user.id)
            new_com.add()
            return redirect (f'/post/{post_id}')
    else:
        return redirect("/forum")

    comments= Comment.query.filter(Comment.post_id == post_id).all()
    users_by_id = {user.id: user for user in User.query.all()}
    for comment in comments:
        comment.user = users_by_id.get(comment.user_id)

    return render_template('post.html', post=post, form=form, comments=comments, user=user )

@app.route('/removepost/<int:post_id>')
def remove_post(post_id):
    post=Post.query.get(post_id)
    comments=Comment.query.filter(Comment.post_id == post_id).all()
    if current_user.role == "Admin" or current_user.id == post.user_id:
        post.remove()
        for comment in comments:
            comment.remove()
        return redirect('/forum')
    else:
        return redirect('/forum')
    
@app.route('/removecomment/<int:comment_id>')
def remove_comment(comment_id):
    comment=Comment.query.get(comment_id)
    if current_user.role == "Admin" or current_user.id == comment.user_id:
        post_id = comment.post_id 
        comment.remove()
        return redirect(f'/post/{post_id}')
    else:
        return redirect(f'/post/{post_id}')
    
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter(Post.user_id == user.id).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route('/editprofile/<int:user_id>', methods=['GET','POST'])
def edit(user_id):
    user = User.query.get(user_id)
    form = RegisterForm(username=user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.password = generate_password_hash(form.password.data)
        if form.image.data:
            image = form.image.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            user.prof_pic = image.filename
        user.save()
        return redirect(f'/profile/{user_id}')
    return render_template('edit_user.html', form=form)\

@app.route('/deleteall/<int:user_id>')
def delete_all(user_id):
    user=User.query.get(user_id)
    posts=Post.query.filter(Post.user_id == user.id)
    for post in posts:
        comments=Comment.query.filter(Comment.post_id == post.id)
        for comment in comments:
            comment.remove()
        post.remove()
    return redirect (f'/profile/{user_id}')

@app.route('/allusers')
def all_users():
    if current_user.is_authenticated and current_user.role == "Admin":
        users=User.query.all()
        return render_template('all_users.html', users=users)
    else:
        return redirect('/')

@app.route('/deleteuser/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if current_user.role == "Admin":
        posts = Post.query.filter(Post.user_id == user.id).all()
        comments = Comment.query.filter(Comment.user_id == user.id).all()
        for post in posts:
            post.remove()
        for comment in comments:
            comment.remove()
        user.remove()
        return redirect('/')
    else:
        return redirect('/')
@app.route('/makepost', methods=['GET','POST'])
def make_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, post=form.post.data, user_id=current_user.id, post_type=form.post_type.data )
        if form.image.data:
            image = form.image.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            new_post.image = image.filename
        new_post.add()
        return redirect(form.referrer.data or '/')
    
    if request.method == 'GET':
        form.referrer.data = request.referrer
    return render_template('make_post.html', form=form)  
        