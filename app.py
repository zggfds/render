from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import  SQLAlchemy
import yadisk
y = yadisk.YaDisk(token='y0_AgAAAABjABpGAAj5-wAAAADZLL3Dq51QeiuoR9CIJp2u6hgciQAov5s')
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/login')
def login():
	return render_template("login.html")


@app.route("/run_log", methods=['POST'])
def log():
	a = request.form['name']
	b = request.form['pass']
	print(y.exists("/"+a))
	if y.exists("/"+a):
		if y.exists("/"+a+"/"+b+"pass"):
			return render_template("home.html")
		else:
			return "password don t work"
	else:
		return "name don t work"


@app.route("/run_reg", methods=['POST'])
def reg():
	a = request.form['name']
	b = request.form['pass']
	c = request.form['fullname']
	print(a,b,c)
	if y.exists("/"+a):
		return "Этот ник уже есть"
	else:
		y.mkdir(a)
		y.mkdir(a+"/"+b+"pass")
		y.mkdir(a+"/"+c+"full")
		return 'pass'



@app.route("/regin")
def regon():
	return render_template("regist.html")




if __name__ =='__main__':
    app.run(host='0.0.0.0', debug=True)
