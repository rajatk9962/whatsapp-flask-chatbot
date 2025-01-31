from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_pymongo import PyMongo
import bcrypt
from train import get_response
from flask_mail import Mail, Message
import xml.etree.ElementTree as et 
import glob 
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import nltk 
nltk.download('punkt')

app = Flask(__name__)
mail= Mail(app)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'mysecret'

# Enter your database connection details below
app.config['MONGO_DBNAME'] = 'mongologin'
app.config['MONGO_URI'] = ''

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'treedetectlandscape@gmail.com'
app.config['MAIL_PASSWORD'] = 'Password@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Intialize MySQL
mongo = PyMongo(app)
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})
        # Fetch one record and return result
        
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                #session['_id'] = login_user.get('_id')
                session['username'] = login_user['username']
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   #session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})
        # If account exists show error and validation checks
        if existing_user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username':request.form['username'], 'password': hashpass, 'email': request.form['email']})
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        users = mongo.db.users
        existing_user = users.find_one({'username' : session['username']})
        account = existing_user
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    lst = re.findall('\S+@\S+', userText)
    if lst:
        for email in lst:
            mailList=[]
            for name in glob.glob('Files/*.xml'): 
                xtree = et.parse(name)
                xroot = xtree.getroot() 

                for child in xroot.findall('./Transaction/Recipient'):
                    
                    s_mail = child.find("Email").text
                    mailList.append(s_mail)

                for child in xroot.findall('./Package'):

                    s_mail = child.find("Email").text
                    mailList.append(s_mail)
            
            if email in mailList:
                msg='Message to the recipients sent'
                mailbody = Message('Whatsapp bot join code', sender = 'treedetectlandscape@gmail.com', recipients = [email])
                mailbody.body = "To join whatsapp bot and recieve the pdf, please send the following text message to +14155238886 \n \n \n join greatly-bend \n \n After you have send the first text and recieved an add response copy and send the following text \n \n \n send 1.pdf"
                mail.send(mailbody)
            else:
                msg= "Email not present in database"    
    elif 'pdf' in userText:
        lst = re.findall('\d{4}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{15}[-\.\s]??\d{4}', userText)
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)
        print(lst)
        for phoneno in lst:
            message = client.messages \
                .create(
                    media_url=['https://drive.google.com/uc?export=download&id=15gRZAuVFEk1MHtWKMvho6MN4lLIOsc1H'],
                    from_='whatsapp:+14155238886',
                    body="Sample",
                    to='whatsapp:+{}'.format(str(phoneno))
                )
            msg='Message over whatsapp sent'    
    else:    
        msg= get_response(userText)  
    return str(msg)



@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    print(msg)
    # Create reply
    resp = MessagingResponse()

    if 'pdf' in msg:
        msg = resp.message()
        msg.media('https://drive.google.com/uc?export=download&id=15gRZAuVFEk1MHtWKMvho6MN4lLIOsc1H')
    
    else:
        reply=get_response(msg)
        resp.message("Solution: {}".format(reply))
    return str(resp)



@app.route("/sendmedia", methods=['POST'])
def send_media():
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            media_url=['https://drive.google.com/uc?export=download&id=15gRZAuVFEk1MHtWKMvho6MN4lLIOsc1H'],
            from_='whatsapp:+1',
            body="Sample",
            to='whatsapp:+91'
        )

    print(message.sid)
    return str(message)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
