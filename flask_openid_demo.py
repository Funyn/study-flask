from flask import Flask,g,session,request,redirect,render_template,flash,url_for
from flask_openid import OpenID
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost:3306/flask_openid?charset=utf8'
oid = OpenID(app,r'D:\flask_demo\flask_openid_demo\tmp',safe_roots=[])

class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    openid = db.Column(db.String(50))
    name = db.Column(db.String(60),unique=True)
    email = db.Column(db.String(120),unique=True,index=True)

# db.create_all()

#-----------每次请求都会先到这个上下文管理函数---------------------#
@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.query.filter_by(openid=openid).first()

@app.route('/')
@app.route('/index/')
def index():
    return 'Hello World!'

#----------登录函数处理---------#
@app.route('/login/',methods=['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid,ask_for=['email','nickname'],ask_for_optional=['fullname']) #----重新尝试去请求登录视图函数------#
    return render_template('login.html',next=oid.get_next_url(),error=oid.fetch_error())

#----------登陆成功后-----------#
@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url       #resp.identity是访问openid返回的url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user:
        flash('Success sign in ')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile',next=oid.get_next_url(),name=resp.fullname or resp.nickname,email=resp.email))

#-----登陆成功后却没有注册信息,返回到下面函数,注册信息到数据库----#
@app.route('/create-profile',methods=['GET','POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if not name:
            flash('Error: 请必须输入您的名字')
        elif '@' not in email:
            flash('Error: 请输入正确的邮件地址')
        else:
            flash('创建成功')
            db.session.add(User(name=name,email=email,openid=session['openid']))
            db.session.commit()
    return render_template('create_profile.html',next=oid.get_next_url())
#-----------登出,退出登陆状态----------#
@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())

if __name__ == '__main__':
    app.run()
