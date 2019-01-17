from flask_wtf import Form
from wtforms import TextField

class clsContactfrm(Form):
   name = TextField("Name Of Student")