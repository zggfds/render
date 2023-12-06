from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import  SQLAlchemy
import yadisk
import urllib.request
import os
from werkzeug.utils import secure_filename
import random
from PIL import Image
import time
import zipfile
y = yadisk.YaDisk(token='y0_AgAAAABjABpGAAj5-wAAAADZLL3Dq51QeiuoR9CIJp2u6hgciQAov5s')
app = Flask(__name__)


@app.route('/test')
def test():
    return render_template("login.html")
    return render_template("home.html")


@app.route('/')
def index():
    user_prof1 = session.get('my_var', None)
    print(user_prof1)


    user_prof2 = session.get('my_var2')

    print(user_prof2)
    if user_prof2:
        p = random.randint(1,8)
        p = str(p)
        y.download("/Admin123/photo"+p, "static/foto/down.zip")
        with zipfile.ZipFile('static/foto/down.zip', 'r') as zip_ref:
            zip_ref.extractall('static/foto')
        path = "static/foto/photo"+p
        dir_list = os.listdir(path)
        statement = ['static/foto/photo'+ p +'/'+ food for food in dir_list]
        print(statement)
        return render_template("have_log.html", file=statement, name = user_prof1)
        #страница с загрузкой фото
    else:
        print(")")
        return render_template("regist.html") #без фото

        #

@app.route('/prof')
def prof():
    y.download("/Admin123", "static/foto/down.zip")
    with zipfile.ZipFile('static/foto/down.zip', 'r') as zip_ref:
        zip_ref.extractall('static/foto')
    path = "static/foto/Admin123"
    dir_list = os.listdir(path)
    statement = ['static/foto/Admin123/' + food for food in dir_list]
    print(statement)
    return render_template("have_log.html", file=statement)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/run_log", methods=['POST'])
def log():
    global user_prof
    user_prof = request.form['name']
    session['my_var'] = user_prof
    session['my_var2'] = True
    b = request.form['pass']

    if y.exists("/"+user_prof):
        if y.exists("/"+user_prof+"/"+b+"pass"):
            return redirect("/up")
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


app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/up')
def upload_form():
    return render_template('upload.html')


@app.route('/up', methods=['POST'])
def upload_image():
    user_prof = session.get('my_var', None)
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            rand = str(random.randint(0, 10000))
            y.upload("static/uploads/" + filename, "/Admin123/" + user_prof + "_foto" + rand + ".jpg")
            os.remove("static/uploads/" + filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    return render_template('upload.html', filenames=file_names)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ =='__main__':
    print("hello")



    app.run(host='0.0.0.0', debug=True)
