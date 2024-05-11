from flask import Flask,render_template,redirect,redirect,url_for,make_response,session
app=Flask(__name__)
from urls import *
app.secret_key="affan"

if(__name__=="__main__"):
    app.run(debug=True)