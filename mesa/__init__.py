from flask import Flask
# from mesapro.models import dataconnector

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba999'

from mesa import routes
