from flask import Flask, render_template, request, flash, redirect, session
from forms import Forms, Posts
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from hash import make_pw_hash, check_pw_hash
from flask_paginate import Pagination



app = Flask(__name__)
app.config['DEBUG'] = True ##enable debug option
app.secret_key = 'Luanchcode tampabay 2017'   ###CSRF key

#create connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode2017@localhost:3306/blogz'

app.config['SQLALCHEMY_ECHO'] = True

#Create alchemy object
db = SQLAlchemy(app)


#create persistent class to be use in database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    message = db.Column(db.String(10000))
    create_date = db.Column(db.DateTime, default=db.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,subject,message,owner):

        self.subject = subject
        self.message = message
        self.owner = owner 

#persistent User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    blogs = db.relationship('Post', backref='owner')

    def __init__(self,username,password):
        self.username=username
        self.password=password



"""Rendering home page"""
@app.route('/')
def home():
    users = User.query.all() 

    return render_template('home.html',users=users,user_auth=is_authenticated())


"""must sign in to post blog"""
@app.before_request
def require_login():
    allow_routes=['login','blog','home','signup','about','logout','static']
    if(request.endpoint not in allow_routes and 'username' not in session):
        return redirect('/login')


"""Rendering blog page"""
@app.route('/blog/<int:page>', methods=['POST','GET'])
@app.route('/blog', methods=['POST', 'GET'])
def blog(page=1):
    posts = Post.query.paginate(page,per_page=5) 
 
    id=request.args.get('id')
    user=request.args.get('user')
    sort=request.args.get('sort')
    last_post=-1 #last entry in post object
    if(id): #query post base on id
        ###posts= Post.query.filter_by(id=id).first()
        posts= Post.query.get(id)
        return render_template('entry.html', posts=posts,user_auth=is_authenticated()) 

    if(user): #query post by user
        user=User.query.filter_by(username=user).first()
        posts=Post.query.filter_by(owner_id=user.id).all()
        return render_template('entry.html',posts=posts, query_by="author",last_post=last_post,user_auth=is_authenticated())

    if(sort == "newest" or sort == "oldest"): #sort post from newest to oldest
        uname=request.args.get('uname')
        user=User.query.filter_by(username=uname).first()
        if(user and sort == "newest"): #descending post for selected user 
            posts=Post.query.filter_by(owner_id=user.id).all()
            last_post=len(posts) - 1
            return render_template('entry.html',posts=posts, query_by="author",last_post=last_post,user_auth=is_authenticated())
        elif(user and sort == "oldest"): #ascending post for selected user 
            posts=Post.query.filter_by(owner_id=user.id).all()
            return render_template('entry.html',posts=posts, query_by="author",last_post=last_post,user_auth=is_authenticated())

        elif(not user and sort == "newest"): #descending for all posts 
            posts = Post.query.order_by('id desc').paginate(page,per_page=5)

    return render_template('blog.html',posts=posts,last_post=last_post,user_auth=is_authenticated())



"""Instantiate signup form and rendering welcome page if successfully validated, else rendering signup page"""
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = Forms()
    error=""
    if(request.method == 'POST' and form.validate_on_submit()):
        
        username= request.form['username']
        hash_password = make_pw_hash(request.form['password1'])
        user=User.query.filter_by(username=username).first()
        if(not user): #create new user
            session['username']=username
            user=User(username,hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect('/post') 
        else: #duplicated user
            error="Duplicated user!"
	
    return render_template('signup.html',form=form,error=error) 


"""Instantiate login form and rendering welcome page if successful, else rendering login page"""
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Forms()
    error=""
    if(request.method == 'POST'):
        username=request.form['username']
        user=User.query.filter_by(username=username).first()
        password = request.form['password1']
        if(user):
            if(check_pw_hash(password,user.password)):
                session['username']=username
                return redirect('/post')
            else:
                flash("Invalid password!")
                error="Invalid Password!"
                #return render_template('login.html',form=form,error=error)
        else:
            flash("Username does not exist!")
            error="Username does not exist!"
            #return redirect('/login') 
        
    return render_template('login.html', form=form, error=error)

#delete user session
@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username',None)
    return redirect('/blog')

"""rendering about page"""
@app.route('/about')
def about():
    return render_template('about.html',  user_auth=is_authenticated())


"""rendering new post """
@app.route('/post', methods=['POST','GET'])
def post():
    form = Posts()
    user=User.query.filter_by(username=session['username']).first()
    if(request.method == 'POST' and form.validate_on_submit()):
        subject=request.form['subject']
        message=request.form['message']
        post=Post(subject,message,user)
        db.session.add(post)
        db.session.commit()
        ###posts = Post.query.filter_by(id=post.id).first()
        posts = Post.query.get(post.id)
        return render_template('entry.html', posts=posts,query_by="post",user_auth=is_authenticated()) 
        
    return render_template('post.html', form=form, user_auth=is_authenticated())

def is_authenticated():

    user=""
    if('username' in session):
       return session['username'] 
    else:
        return user 

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000)
