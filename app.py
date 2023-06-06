#MARVIN LOPEZ BUCKET LIST PYTHON APP

#IMPORT STATEMENTS
from flask import Flask, render_template, json, request, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

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
    #if session.get('user'):
        return render_template('tutorhome.html')
   # else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/managerhome')
def managerHome():
    #if session.get('user'):
        return render_template('managerhome.html')
   # else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/studenthome')
def studentHome():
    #if session.get('user'):
        return render_template('studenthome.html')
   # else:
        return render_template('error.html',error = 'Unauthorized Access')

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

        #Connect to MySQL
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        #Check Login Creds
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userhome')
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

@app.route('/api/signup',methods=['POST'])
def signUp():
     # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

     # validate the received values
    if _name and _email and _password:

        
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        #return json.dumps({'message':len(_hashed_password)})
        cursor.callproc('sp_createUser',(_name, _email, _hashed_password))
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