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
			return "GOOD"
		else:
			return "password don t work"
	else:
		return "name don t work"



if __name__ =='__main__':
    app.run(host='0.0.0.0', debug=True)
