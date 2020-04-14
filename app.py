from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
# import math

import threading
import Matcher
import mongoDb
import Questions
import os
import random
import json
from pathlib import Path, PureWindowsPath
import os
import mail
# import Video_Cap
# import emotion_cal
import filedelet
import image_process

app = Flask(__name__)


'''   File Storage Handling    '''

mypath = os.getcwd()
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'txt', 'docx'}


app.config['UPLOAD_FOLDER'] = mypath + "/storage"
app.config["CLIENT_PDF"] = mypath + "/storage"
# app.config["CLIENT_IMAGES"] = mypath + "/storage"
app.config["TEMPLATE"] = mypath + "/static/Docs"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/database_download/<filename>')
def database_download(filename):
    return send_from_directory(app.config["TEMPLATE"], filename, as_attachment=True)


''' Display template '''


@app.route('/')
def screen():
    return render_template('home.html')


@app.route('/quiz')
def quiz():
    return render_template('Quiz_Score.html')


@app.route('/dash')
def dash():
    return render_template('Resume_score.html')


@app.route('/admin')
def admin():
    return render_template('Admin.html')


@app.route('/helps', methods=['GET', 'POST'])
def helps():
    # temp = mypath+"/static/Docs/Data Science Template.csv"
    # qa = mypath +"/static/Docs/Questions.csv
    return render_template('help.html')


@app.route('/C_Login')
def C_Login():
    return render_template('cand_login.html')


@app.route('/C_helps')
def C_helps():
    return render_template('cand_help.html')


''' File upload handling '''


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        filedelet.create_dir()
        data = []
        csvFile = request.files['csv']
        csv_ext = str(csvFile).split("'")

        if ".csv" in csv_ext[1]:
            if csvFile and allowed_file(csvFile.filename):
                csvname = secure_filename(csvFile.filename)
                csvFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], csvname))
                csv_path = mypath + '/storage/' + csvname

                Matcher.csv_handling(csv_path)
        else:
            fail = '''Please upload only CSV file.'''
            return render_template('upload.html', fail=fail)

        queFile = request.files['que']
        que_ext = str(csvFile).split("'")

        if ".csv" in que_ext[1]:
            if csvFile and allowed_file(queFile.filename):
                quename = secure_filename(queFile.filename)
                queFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], quename))
                que_path = mypath + '/storage/' + quename

                Data = []
                Data.append(Questions.question_extract(que_path))
                mongoDb.questions_store(Data)
        else:
            fail = '''Please upload only CSV file.'''
            return render_template('upload.html', fail=fail)

        for f in request.files.getlist('file[]'):
            pdf_ext = str(f).split("'")
            if ".pdf" in pdf_ext[1]:
                if f and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    pdf_path = mypath + '/storage/' + filename
                    name, mail, result = Matcher.create_database(
                        pdf_path, filename)
                    data.append(Matcher.header_Cal(name, mail, result))

            elif ".docx" in pdf_ext[1]:
                if f and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    pdf_path = mypath + '/storage/' + filename
                    name, mail, result = Matcher.create_database(
                        pdf_path, filename)
                    data.append(Matcher.header_Cal(name, mail, result))

            elif ".txt" in pdf_ext[1]:
                if f and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    pdf_path = mypath + '/storage/' + filename
                    name, mail, result = Matcher.create_database(
                        pdf_path, filename)
                    data.append(Matcher.header_Cal(name, mail, result))

            else:
                fail = '''upload only pdf,docx and txt files'''
                return render_template('upload.html', fail=fail)
                break
        # print("-----------")
        mongoDb.collection_store(data)
        Success = "Success"
        filedelet.Delete_files()
        return render_template('upload.html', suc=Success)

    return render_template('upload.html')


''' Data will send to vue js using axios '''


@app.route('/data', methods=['GET'])
def all_data():
    Db = mongoDb.FetchAll()
    for i in range(len(Db)):
        del Db[i]["_id"]
    # print(Db)
    return jsonify({
        'books': Db
    })


@app.route('/que_data', methods=['GET'])
def Questions_all():
    Db = mongoDb.Questions_All()

    for i in range(len(Db)):
        del Db[i]["_id"]

    header = Db[0]['Header']
    data = {}
    data = Db[0]
    ress = res[-1]
    data['Selected'] = option[0:len(header)]
    data['Name'] = ress[0]["Name"]
    data['Email'] = ress[0]["Email"]
    Data = []
    Data.append(data)
    return jsonify({
        'questions': Data})


@app.route('/result_data', methods=['GET'])
def result_data():
    Db = mongoDb.Result_All()
    for i in range(len(Db)):
        del Db[i]["_id"]
    # print(Db)
    return jsonify({
        'books': Db
    })


@app.route('/request_data', methods=['GET'])
def request_data():
    Db = mongoDb.request_All()
    for i in range(len(Db)):
        del Db[i]["_id"]
    # print(Db)
    return jsonify({
        'books': Db
    })


''' Mail send function '''
@app.route("/Mail", methods=['GET', 'POST'])
def sendMail():
    if request.method == 'POST':
        json_data = request.get_json()

        email = json_data['username']
        psw = json_data['password']
# Admin mail function required
        res = mongoDb.signinVerify(email)
        Name = res[0]["Name"]

        if mail.mail_send(Name, email, psw):
            return jsonify("successs")


''' Users sign in  & sign up '''
global res
res = []
@app.route("/Login", methods=['GET', 'POST'])
def signin():

    if request.method == 'POST':

        name = request.form['name']
        psw = request.form['psw']

        welcome = ''

        if (name == "admin@admin" and psw == "admin"):
            return render_template('Admin.html')

        if (name == "hr@hr" and psw == 'hr'):
            return render_template('upload.html')

        res.append(mongoDb.signinVerify(name))
        ress = res[-1]
        if not ress:
            welcome = "user not exist"
            return render_template('signin.html', wel=welcome)

        if name == ress[0]['Email'] and psw == ress[0]['Password']:
            welcome = ress[0]['Name']
            Que = mongoDb.Questions_All()
            header = Que[0]['Header']
            length = len(header)
            return render_template('cand_welcome.html', Name=welcome, Header=header, length=length)

        else:
            welcome = "user not exist"
            return render_template('signin.html', wel=welcome)

    return render_template('signin.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        data = []
        hr_list = {}
        name = request.form['name']
        mail = request.form['mail']
        hr_list["Name"] = name
        hr_list["Email"] = mail
        hr_list['Uid'] = random.randint(1000, 9999)
        hr_list["Psw"] = name[0:3] + str(random.randint(1000, 9999))
        data.append(hr_list)
        mongoDb.request_Store(data)

        return render_template('signin.html', suc='You can access the tool only after your request is approved.')
    return render_template('signup.html',)


''' candidate rate herself  function'''

global option
option = []
@app.route("/cand_choose", methods=['POST'])
def Choose():

    Que = mongoDb.Questions_All()
    header = Que[0]['Header']

    for i in range(0, len(header)):
        value = "{0}_{1}".format(header[i], request.form.get(str(i)))
        option.insert(i, value)

    return render_template('Questions.html')


''' video capture connection established  here'''


@app.route("/Quez_Ans", methods=['POST'])
def Ans():

    if request.method == 'POST':
        json_data = request.get_json()

        data = {}
        Capture = []
        emo = {'confused': 0, 'neutral': 0, 'confident': 0}
        data = json_data['Result']
        Capture = json_data['Captures']
        emo_list = image_process.frame_process(Capture)
        emo_len = len(emo_list)
        # print(emo_len)
        for elem in emo_list:
            # If element exists in dict then increment its value else add it in dict
            if elem in emo:
                emo[elem] += 1

        emo_result = {}
        emo_head = []
        emo_score = []

        # print("result")
        # print(emo)

        for key in emo:
            emo_head.append(key)
            emo_score.append((emo[key]*100)//emo_len)
        emo_result["emo_head"] = emo_head
        emo_result["emo_score"] = emo_score

        data.update(emo_result)
        Data = []
        Data.append(data)

        mongoDb.result_Store(Data)
        return "success"
    return "error"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(debug=True, port=8080)
