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
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import urllib.request
import yadisk
import random
y = yadisk.YaDisk(token='y0_AgAAAABjABpGAAteYwAAAAD8h3OKAAAf5oVS6dJNT7ZyxC1l7Vqy124Oug')
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
        p = random.randint(1,3)
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
    
    session['my_var2'] = False
    b = request.form['pass']

    if y.exists("/"+user_prof):
        if y.exists("/"+user_prof+"/"+b+"pass"):
            session['my_var2'] = True
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
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])



 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/up')
def index11(): 
    return render_template('index1.html')
 
@app.route('/up', methods=['POST'])
def upload():
    if 'uploadFile[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('uploadFile[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            msg  = 'File successfully uploaded to /static/uploads! он на рендере не выходи'
            x = random.randint(1,10000)

            y.upload("static/uploads/"+filename, "/Admin123/"+str(x)+filename, overwrite=True)

        else:
            msg  = 'Invalid Uplaod only png, jpg, jpeg, gif'
    return jsonify({'htmlresponse': render_template('response.html', msg=msg, filenames=file_names)})


if __name__ =='__main__':
    print("hello")



    app.run(host='0.0.0.0', debug=True)


#test