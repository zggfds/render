from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import  SQLAlchemy
import yadisk
import urllib.request
import os
from werkzeug.utils import secure_filename

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
	global user_prof
	user_prof = request.form['name']
	b = request.form['pass']
	print(y.exists("/"+user_prof))
	if y.exists("/"+user_prof):
		if y.exists("/"+user_prof+"/"+b+"pass"):
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
		y.mkdir(a+'/'+c+"fullname")
		return redirect('/login')
		



@app.route("/regin")
def regon():
	return render_template("regist.html")


 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/up')
def home():
    return render_template('home.html')
 
@app.route('/up', methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
    	print(user_prof)
    	filename = secure_filename(file.filename)
    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    	#print('upload_image filename: ' + filename)
    	flash('Image successfully uploaded and displayed below')
    	print(filename)
    	y.upload("static/uploads/"+filename, "/Admin123/ABOBA2.jpg")
    	os.remove("static/uploads/"+filename)
    	return render_template('index.html', filename=filename)
    else:
    	flash('Allowed image types are - png, jpg, jpeg, gif')
    	return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)





if __name__ =='__main__':
    app.run(host='0.0.0.0', debug=True)