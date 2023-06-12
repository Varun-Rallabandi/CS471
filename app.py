#MARVIN LOPEZ BUCKET LIST PYTHON APP

#IMPORT STATEMENTS
from flask import Flask, render_template, json, request, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

#Code for Email Implementation
from email.message import EmailMessage
import ssl
import smtplib

# globalUsername = ""
# globalUserType = ""

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

@app.route('/managerSignup')
def managerSignup():
    return render_template('managerSignup.html')

@app.route('/signin')
def showSignin():
    return render_template('signin.html')

@app.route('/success')
def showSuccess():
    return render_template('successPage.html')

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
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT tutor_name, tutor_username, student_name, student_username, tutor_class, session_time FROM tbl_tutorsessions"
        cursor.execute(query)
        sessionList = cursor.fetchall()
        cursor.close()
        return render_template('managerhome.html', sessions = sessionList)
    else:
        return render_template('error.html',error = 'Unauthorized Access')
    
@app.route('/managerViewUsers')
def managerViewUserLists():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT user_name, user_username FROM tbl_studentuser"
        cursor.execute(query)
        studentList = cursor.fetchall()
        cursor.close()
        cursor = con.cursor()
        query = "SELECT user_name, user_username FROM tbl_tutoruser"
        cursor.execute(query)
        tutorList = cursor.fetchall()
        cursor.close()
        return render_template('managerViewUsers.html', students = studentList, tutors = tutorList)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/tutorRequests')
def tutorRequests():
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT req_name, req_username, req_tutor_name, req_tutor_username, req_description FROM tbl_tutorrequest"
        cursor.execute(query)
        requestList = cursor.fetchall()
        cursor.close()
        return render_template('tutorRequests.html', requests=requestList)


@app.route('/studenthome')
def studentHome():
    if session.get('user'):
        return render_template('studenthome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/whiteboard')
def whiteBoard():
        return render_template('whiteBoard.html')

@app.route('/videoconference')
def videoConference():
        return render_template('videocon.html')

@app.route('/studentRating')
def studentRating():
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT student_name, rating_value, review_text, tutored_class FROM tbl_studentratings"
        cursor.execute(query)
        ratingsList = cursor.fetchall()
        cursor.close()
        return render_template('createStudentRating.html', ratings=ratingsList)

@app.route('/tutorRating')
def tutorRating():
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT tutor_name, rating_value, review_text, tutored_class FROM tbl_tutorratings"
        cursor.execute(query)
        ratingsList = cursor.fetchall()
        cursor.close()
        return render_template('createTutorRating.html', ratings = ratingsList)

@app.route('/tutorInfo')
def tutorSelection():
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT user_name, user_username, qualifications FROM tbl_tutoruser"
        cursor.execute(query)
        tutorsList = cursor.fetchall()
        cursor.close()
        return render_template('tutorSelection.html', tutors=tutorsList)

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
               # globalUsername = _username
               # globalUserType = _userType
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

@app.route('/api/studentSignup', methods=['POST'])
def studentSignUp():
    try:
        # read the posted values from the UI 
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _time1 = (request.form['inputTime1']).upper()
        _time2 = (request.form['inputTime2']).upper()
        _time3 = (request.form['inputTime3']).upper()
        _class1 = (request.form['inputClass1']).upper()
        _class2 = (request.form['inputClass2']).upper()
        _class3 = (request.form['inputClass3']).upper()
        _repeat = request.form['inputRepeat']

        # validate the received values
        if _name and _email and _password and _time1 and _time2 and _time3 and _class1 and _class2 and _class3 and _repeat:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createStudent',(_name, _email, _hashed_password, _time1, _time2, _time3, _class1, _class2, _class3, _repeat))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    

@app.route('/api/tutorSignup', methods=['POST'])
def tutorSignUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _time1 = (request.form['inputTime1']).upper()
        _time2 = (request.form['inputTime2']).upper()
        _time3 = (request.form['inputTime3']).upper()
        _class1 = (request.form['inputClass1']).upper()
        _class2 = (request.form['inputClass2']).upper()
        _class3 = (request.form['inputClass3']).upper()
        _qualifications = request.form['qualifications']
        # validate the received values
        if _name and _email and _password and _time1 and _time2 and _time3 and _class1 and _class2 and _class3 and _qualifications:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createTutor', (_name, _email, _hashed_password, _time1, _time2, _time3, _class1, _class2, _class3, _qualifications))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    

@app.route('/api/managerSignup', methods=['POST'])
def managerSignUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createManager', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    



@app.route('/api/inputStudentRating', methods=['POST'])
def inputStudentRating():
    try:
        # read the posted values from the UI 
        _name = request.form['inputName']
        _rating = request.form['inputRating']
        _review = request.form['inputReview']
        _class = request.form['inputClass']

        # validate the received values
        if _name and _rating and _review and _class:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createStudentRating',(_name, _rating, _review, _class,))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'Student Rating created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    

@app.route('/api/inputTutorRating', methods=['POST'])
def inputTutorRating():
    try:
        # read the posted values from the UI 
        _name = request.form['inputName']
        _rating = request.form['inputRating']
        _review = request.form['inputReview']
        _class = request.form['inputClass']

        # validate the received values
        if _name and _rating and _review and _class:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createTutorRating',(_name, _rating, _review, _class,))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'Tutor Rating created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    

@app.route('/api/tutorRequest', methods=['POST'])
def tutorRequest():
    try:
        # read the posted values from the UI 
        _name = request.form['inputName']
        _username = request.form['inputUsername']
        _tutorName = request.form['inputTutorName']
        _tutorUsername = request.form['inputTutorUsername']
        _requestDescription = request.form['inputRequest']

        # validate the received values
        if _name and _username and _requestDescription:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createTutorRequest',(_name, _username, _tutorName, _tutorUsername, _requestDescription))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'Tutor Request submitted successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    


@app.route('/api/inputTutorSession', methods=['POST'])
def inputTutorSession():
    try:
        # read the posted values from the UI 
        _tutor_name = request.form['inputTutorName']
        _tutor_username = request.form['inputTutorUsername']
        _student_name = request.form['inputStudentName']
        _student_username = request.form['inputStudentUsername']
        _class = request.form['inputClass']
        _time = request.form['inputTime']

        # validate the received values
        if _tutor_name and _tutor_username and _student_name and _student_username and _class and _time:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createTutorSession',(_tutor_name, _tutor_username, _student_name, _student_username, _class, _time))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'Tutor Session created successfully !'})
            else:
                return json.dumps({'error': 'Database error: ' + str(data[0])}), 400  # 400 means 'Bad Request'
        else:
            return json.dumps({'error': 'Enter the required fields'}), 400
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()    

if __name__ == "__main__":
    app.run()