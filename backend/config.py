import os

MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME','19bcs2420@gmail.com')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD','Qwertyuiop@7')

MONGODB_URI = os.environ.get("mongodb://parminder13dev:UkVI4Ta89fgdVGEe@localhost:27017/inventory")

