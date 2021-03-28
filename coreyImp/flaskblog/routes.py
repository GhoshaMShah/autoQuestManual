from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect,Flask,request,make_response
from flaskblog import app
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import date 
from requests.models import Response
from flask import Response
import tkinter
from tkinter import messagebox
import pyautogui as pag
import pdfkit as pdf
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
import pandas
from io import StringIO
import sys




#from flask.ext.cache import Cache   

global dat
dat = date.today()
global semester1
global subject1
global subjectCode
global duration
global totalMarks
totalMarks = 0
global marks1
marks1 = 0
global marks2
marks2=0
global marks3
marks3=0
global difficultyLevel1
global number_of_Ques1
global number_of_Ques2
global number_of_Ques3
global dataA
dataA = ''
global dataB
dataB = ''
global dataC
dataC = ''
global getPdf
getPdf = 0




posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    Response().headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    Response().headers["Pragma"] = "no-cache"
    Response().headers["Expires"] = "0"
    Response().headers['Cache-Control'] = 'public, max-age=0'
    return render_template('home.html', title='Home',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contactUs")
def contactUs():
    return render_template('contactUs.html', title='Contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form = RegistrationForm()
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        found = 0
        myName = form.username.data
        myEmail = form.email.data
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName:
                found=1
                flash('Username already exists', 'danger')
                break
            elif row[2]==myEmail:
                found=1
                flash('Email already exists', 'danger')
                break
        if found==0:
            val = (form.username.data,form.email.data,form.password.data)
            query ="INSERT INTO login(Username,Email,Password) VALUES (%s,%s,%s)"
## There is no need to insert the value of rollno 
## because in our table rollno is autoincremented #started from 1
## storing values in a variable
## executing the query with values
            cur.execute(query,val)
## to make final output we have to run 
## the 'commit()' method of the database object
            db.commit()
            flash(f'Account created for {myName} ! ', 'success')
    return render_template('register.html', title='Register', form=form)


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    form = RegistrationForm()
    return render_template('welcome.html', title='Welcome',form=form)        
 


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    found = 0
    myName = form.username.data
    myEmail = form.email.data
    myPassword = form.password.data
    if form.validate_on_submit():
        form = LoginForm()
        found = 0
        myPassword = form.password.data
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName and row[3]==myPassword:
                if row[2]==myEmail:
                    found=2
                    break
                else:
                    found=1
                    flash('Login Unsuccessful. Please check email', 'danger')

        if found==0:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        elif found==2:
            flash("Login successful",'success')
            response = make_response()
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            Response().headers["Pragma"] = "no-cache"
            Response().headers["Expires"] = "0"
            Response().headers['Cache-Control'] = 'public, max-age=0'
            return redirect(url_for('Index',username=myName))
    return render_template('login.html', title='Login', form=form)


@app.route('/index/<string:username>')
#@app.cache.cached(timeout=0)
def Index(username):
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT * FROM questions WHERE Username=%s",(username,))
    data = cur.fetchall()
    cur.close()
    """
    response = make_response()

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    Response().headers["Pragma"] = "no-cache"
    Response().headers["Expires"] = "0"
    Response().headers['Cache-Control'] = 'public, max-age=0'
    """
    return render_template('index2.html', questions=data, username=username)

@app.route('/home', methods = ['POST'])
def logout():
    response = make_response()
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #Response().headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    Response().headers["Pragma"] = "no-cache"
    Response().headers["Expires"] = "0"
    Response().headers['Cache-Control'] = 'public, max-age=0'
    return render_template('home.html', title='Home')




@app.route('/insert/<string:username>', methods = ['POST'])
def insert(username):

    if request.method == "POST":
        recordFound = 0
        
        
        #driver = webdriver.Chrome(executable_path="E:/darshan sem 7/project/flaskTutorial/flaskAutoQuestCRUD/chromedriver.exe")
        #driver = webdriver.get("file:///E:/darshan%20sem%207/project/flaskTutorial/flaskAutoQuestCRUD/templates/addstudent.html")
        #element = driver.find_element_by_id("semesterDropDown")
        #drp = Select(element)
        #semester = drp.first_selected_option.text
        #print(select.first_selected_option.text)
        #print(select.first_selected_option.get_attribute("value"))
        
        semester = int(request.form.get('semester'))
        subject = request.form['subject']
        #marks = int(request.form['marks'])
        #difficultyLevel = request.form['difficultyLevel']
        marks = int(request.form['marks'])
        
        difficultyLevel = request.form.get('difficultyLevel')
        
        question = request.form['question']

        #if question==" ":
         #   root = tkinter.Tk()
          #  root.withdraw()

# message box display
           # messagebox.showerror("Error", "Please insert the question")
        
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor(buffered=True)
        cur.execute("SELECT * FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Question=%s",(username,semester,subject,question))
        r=cur.fetchall()
        recordFound=cur.rowcount
        if recordFound==1:
            flash("Record already exists\n You might want to update it.",'danger')
            return redirect(url_for('Index',username=username))
            

        elif recordFound==0:
            cur = db.cursor(buffered=True)
            cur.execute("INSERT INTO questions (Username,Semester,Subject,Marks,Difficulty_level,Question) VALUES (%s, %s, %s, %s , %s, %s)", (username,semester,subject,marks,difficultyLevel,question))
            db.commit()
            flash("Question Inserted Successfully","success")
            return redirect(url_for('Index',username=username))


    


@app.route('/delete/<string:id_data>/<string:username>', methods = ['POST','GET'])
def delete(id_data,username):
    flash("Question Has Been Deleted Successfully","success")
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("DELETE FROM questions WHERE id=%s", (id_data,))
    db.commit()
    return redirect(url_for('Index',username=username))



@app.route('/update/<string:username>',methods=['POST','GET'])
def update(username):

    if request.method == 'POST':
        id_data = request.form['id']
        
        #semester = request.form.select['semester']
        semester = int(request.form.get('semester'))

        subject = request.form['subject']
        marks = request.form['marks']
        difficultyLevel = request.form.get('difficultyLevel')
        question = request.form['question']
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("""
               UPDATE questions
               SET Semester=%s, Subject=%s, Marks=%s, Difficulty_level=%s, Question=%s
               WHERE id=%s
            """, (semester,subject,marks,difficultyLevel,question, id_data))
        flash("Question Updated Successfully","success")
        db.commit()
        return redirect(url_for('Index',username=username))



@app.route('/index/<string:username>/generate')
def generate(username):
    return render_template('generate.html', username=username)

@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperGenerate(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    sectionError = 0
    msg1 = ''
    msg2 = ''
    msg3 = ''
    global semester1
    semester1 = request.form.get('semester')
    global subject1
    subject1 = request.form['subject']
    global subjectCode
    subjectCode = request.form['subjectCode']
    durationHours = request.form['hours']
    durationMinutes = request.form['mins']
    global duration
    duration = durationHours+' hours '+durationMinutes+' minutes'
    global marks1
    marks1 = int(request.form['marks1'])
    difficultyLevel1 = request.form.get('difficultyLevel1')
    global number_of_Ques1
    number_of_Ques1 = int(request.form['noOfQues1'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")

    cur1 = db.cursor(buffered=True)
    cur1.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s",(username,semester1,subject1,marks1,difficultyLevel1))
    
    if cur1.rowcount<number_of_Ques1:
        sectionError+=1
        msg1+='\nSection-A:\nInsert desired questions in the AutoQuest system'

    #global dataA
    #dataA = cur1.fetchall()

    
        
    global marks2
    marks2 = int(request.form['marks2'])
    difficultyLevel2 = request.form.get('difficultyLevel2')
    global number_of_Ques2
    number_of_Ques2 = int(request.form['noOfQues2'])
    cur2 = db.cursor(buffered=True)
    cur2.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s ",(username,semester1,subject1,marks2,difficultyLevel2))
    if cur2.rowcount<number_of_Ques2:
        sectionError+=1
        msg2+='\nSection-B:\nInsert desired questions in the AutoQuest system'
    

    global marks3
    marks3 = int(request.form['marks3'])
    difficultyLevel3 = request.form.get('difficultyLevel3')
    global number_of_Ques3
    number_of_Ques3 = int(request.form['noOfQues3'])
    cur3 = db.cursor(buffered=True)
    cur3.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s",(username,semester1,subject1,marks3,difficultyLevel3))
    if cur3.rowcount<number_of_Ques3:
        sectionError+=1
        msg3+='\nSection-C:\nInsert desired questions in the AutoQuest system'
    



    if sectionError==0:
        global totalMarks
        m1 = marks1*number_of_Ques1
        m2 = marks2*number_of_Ques2
        m3 = marks3*number_of_Ques3
        totalMarks=int(m1+m2+m3)
        cur1.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester1,subject1,marks1,difficultyLevel1,number_of_Ques1))
        global dataA
        dataA = cur1.fetchall()
        cur2.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester1,subject1,marks2,difficultyLevel2,number_of_Ques2))
        global dataB
        dataB = cur2.fetchall()

        cur3.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester1,subject1,marks3,difficultyLevel3,number_of_Ques3))
        global dataC
        dataC = cur3.fetchall()
        cur3.close()
        flash("Question paper generated!","success")
        return render_template('quesPaper.html', username=username,questions1=dataA,questions2=dataB,questions3=dataC, semester=semester1,subject=subject1,subjectCode=subjectCode,duration=duration,totalMarks=totalMarks,marks1=marks1,marks2=marks2,marks3=marks3,date=dat,getPdf=getPdf)

    else:
        #root = tkinter.Tk()
        #root.withdraw()
        #messagebox.showinfo("Title", "Message")
        #win32api.MessageBox(0, 'hello', 'title')
        #pag.alert(text=msg, title="Couldn't generate question paper")
        if msg1!='':
            flash(msg1, 'danger')
        if msg2!='':
            flash(msg2, 'danger')
        if msg3!='':
            flash(msg3, 'danger')
        
        return redirect(url_for('generate',username=username))
    
"""

@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperB(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global semester2
    global subject2
    global marks2
    global difficultyLevel2
    global number_of_Ques2
    global sectionB
    sectionB = 1
    semester2 = int(request.form.get('semester'))

    subject2 = request.form['subject']
    
    marks2 = request.form['marks2']
    difficultyLevel2 = request.form.get('difficultyLevel2')
    number_of_Ques2 = int(request.form['noOfQues2'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester2,subject2,marks2,difficultyLevel2,number_of_Ques2))
    global dataB
    dataB = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))


@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperC(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global sectionC
    sectionC = 1
    
    global semester3
    global subject3
    global marks3
    global difficultyLevel3
    global number_of_Ques3
    semester3 = int(request.form.get('semester'))

    subject3 = request.form['subject']
   
    marks3 = request.form['marks3']
    difficultyLevel3 = request.form.get('difficultyLevel3')
    number_of_Ques3 = int(request.form['noOfQues3'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester3,subject3,marks3,difficultyLevel3,number_of_Ques3))
    global dataC
    dataC = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))
"""

@app.route('/index/<string:username>/generate/question_paper',methods=['POST','GET'])
def questionPaper(username):
    global dat 
    dat = date.today()
    return render_template('quesPaper.html', username=username,questions1=dataA,questions2=dataB,questions3=dataC, semester=semester1,subject=subject1,marks1=marks1,marks2=marks2,marks3=marks3,date=dat)

@app.route('/index/<string:username>/generate/pdf',methods=['POST','GET'])
def PDFOfQuestionPaper(username,**args):
    config = pdf.configuration(wkhtmltopdf="E:/wkhtmltopdf/bin/wkhtmltopdf.exe")
    dat = date.today()
    #global getPdf
    getPdf = 1
    html = render_template('quesPaper.html',questions1=dataA,questions2=dataB,questions3=dataC,semester=semester1,subject=subject1,subjectCode=subjectCode,duration=duration,totalMarks=totalMarks,marks1=marks1,marks2=marks2,marks3=marks3,date=dat,getPdf=getPdf)
    #file_class = Pdf()
    from xhtml2pdf import pisa
    from io import BytesIO
    #FileName = 'semester'+semester1+subject1+'question_paper'
    #from StringIO import StringIO

    PDF = BytesIO()
    

    pisa.CreatePDF(BytesIO(html.encode()),PDF)

    valueOfData =  PDF.getvalue()
    headers = {
        'content-type': 'application.pdf',
        'content-disposition': 'attachment; filename=Question_Paper.pdf'}
    return valueOfData, 200, headers
