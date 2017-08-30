from flask import Flask,Response,views,render_template,request,redirect,url_for,session,flash
from flask_wtf import CsrfProtect
from forms import RegistForm

app = Flask(__name__)
app.config.from_pyfile('config.py')
CsrfProtect(app)


@app.route('/')
@app.route('/index/')
def index():
	return 'hello world'

#注册视图
class RegisterView(views.MethodView):

	def get(self):
		return render_template('regist.html')

	def post(self):
		form = RegistForm()
		if form.validate():
			username = form.username.data
			password = form.password.data
			return render_template('login.html',username=username,password=password)
		else:
			return redirect(url_for('regist'))


#登陆验证器
def login_required(func):
	def warpfunc(*args,**kwargs):
		allow = session.get('username',None)
		if allow:
			return func()		
		return redirect(url_for('login'))
	return warpfunc

#登陆视图
class LoginView(views.MethodView):

	def get(self):
		return render_template('login.html')

	def post(self):
		username = request.form.get('username')
		password = request.form.get('password')
		if request.form.get('remember'):
			session['username'] = username
			session.permanent = True
		session['remember'] = username
		return redirect(url_for('index'))

app.add_url_rule('/regist/',endpoint='regist',view_func=RegisterView.as_view('regist'))
app.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))


@app.route('/list/')
@login_required
def article_list():
	return 'hello world'

if __name__ == '__main__':
	app.run()