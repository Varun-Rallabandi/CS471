#MARVIN LOPEZ BUCKET LIST PYTHON APP

#IMPORT STATEMENTS
from flask import Flask, render_template, json, request, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

#Code for Email Implementation
from email.message import EmailMessage
import ssl
import smtplib

'''email_sender = 'tutorg76@gmail.com'
email_password = 'agmssublzuxxrany'

email_receiver = 'tade2477@kettering.edu'

subject = "WORK ON THE FUCKING PROJECT"
body = """
Every time this email is ignored, its a $10 fine. 
Hugs and Kisses - MyTutor5000 :)

p.s Emily is coming for you >:(

and come to sac meeting - Varun
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
     smtp.login(email_sender, email_password)
     smtp.sendmail(email_sender, email_receiver, em.as_string())
'''

#DEFINING APP
app = Flask(__name__)

#MySQL CONFIGURATIONS
mysql = MySQL()
# MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.secret_key = 'We enjoy life by the help and society of others!'

#Page Routing
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/studentSignup')
def studentSignup():
    return render_template('studentSignup.html')

@app.route('/tutorSignup')
def tutorSignup():
    return render_template('tutorSignup.html')

#tutor sign up

@app.route('/signin')
def showSignin():
    return render_template('signin.html')

@app.route('/userhome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
    
@app.route('/tutorhome')
def tutorHome():
    if session.get('user'):
        return render_template('tutorhome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/managerhome')
def managerHome():
    if session.get('user'):
        return render_template('managerhome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/studenthome')
def studentHome():
    if session.get('user'):
        return render_template('studenthome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/test')
def test():
        return render_template('studentSignup.html')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#DATABASE ACTIONS
@app.route('/api/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        _userType = request.form['user-type']

        #Connect to MySQL
        con = mysql.connect()
        cursor = con.cursor()

        if _userType == "Student":
            cursor.callproc('sp_validateStudentLogin', (_username,))
        elif _userType == "Tutor":
            cursor.callproc('sp_validateTutorLogin', (_username,))
        elif _userType == "Manager":
            cursor.callproc('sp_validateManagerLogin', (_username,))
        else:
            return render_template('error.html',error = 'No User Type Selected.')

        data = cursor.fetchall()

        #Check Login Creds
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                if _userType == "Student":
                    return redirect('/studenthome')
                elif _userType == "Tutor":
                    return redirect('/tutorhome')
                elif _userType == "Manager":
                    return redirect('/managerhome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
    
    #Exception Handling
    except Exception as e:
        return render_template('error.html',error = str(e))
    
    #Housekeeping
    finally:
        cursor.close()
        con.close()

@app.route('/api/studentSignup',methods=['POST'])
def studentSignUp():
     # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _class1 = request.form['class1']
    _class2 = request.form['class2']
    _class3 = request.form['class3']
    _class4 = request.form['class4']
    _time1 = request.form['time1']
    _time2 = request.form['time2']
    _time3 = request.form['time3']
    _time4 = request.form['time4']
    _repeat = request.form['repeat']
    

     # validate the received values
    if _name and _email and _password and _class1 and _class2 and _class3 and _class4 and _time1 and _time2 and _time3 and _time4 and _repeat:

        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        #return json.dumps({'message':len(_hashed_password)})
        cursor.callproc('sp_createStudent',(_name, _email, _hashed_password, _class1, _class2, _class3, _class4, _time1, _time2, _time3, _time4, _repeat))
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()