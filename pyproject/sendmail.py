from threading import Thread
import os
from flask import Flask,render_template
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'makarasumsung@gmail.com'
app.config['MAIL_PASSWORD'] = '123456'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#Create an instance of Mail class.
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)



@app.route("/")
def index():
   msg = Message('Hello', sender = 'makarasumsung@gmail.com', recipients = ['pfpcambo@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Message was Sent to makarasumsung@gmail.com"

if __name__ == '__main__':
   app.run(debug=True)
