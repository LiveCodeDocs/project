
from flask import Flask, render_template, url_for, session, request
import mysql.connector
import sys
import requests
import json

from flask.ext.cors import CORS
app = Flask(__name__)
cors = CORS(app)

app.debug = True

@app.route('/')
def main():
    return render_template("HomePage.html")

@app.route('/login', methods = ['POST'])
def handlelogin():
	#packet structure - { accesstype : <0 for login 1 for register>, username: <username>, password: <password>
	if  request.method == 'POST':
		#config = {'user': 'root', 'password' : 'LiveCodeDocs', 'host' : 'http://livecodedocs.csse.rose-hulman.edu', 'database' : 'LiveCodeDocs')
		cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
		access_type = request.json[0]['accesstype']
		username = request.json[0]['username']
		password = request.json[0]['password']
		cursor = cnx.cursor()
		args = [username]
		cursor.callproc('AddNewUser', args)
		cnx.commit()
		cnx.close()
	return "success"

		

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

