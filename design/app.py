
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

@app.route('/project')
def renderProject():
	return render_template("project.html")

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
	
@app.route('/')
def openFile():
	return
	
@app.route('/getProjectFiles', methods = ['GET'])
def getProjectFiles():
	if request.method == 'GET':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		projectID = request.json[0]['projectid']
		cursor = cnx.cursor()
		args = [projectID]
		cursor.callproc('GetProjectFiles', args)
	return jsonify(data=cursor.fetchall())
	
@app.route('/saveFile', methods = ['POST'])
def saveFile():
	if request.method == 'POST':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		
		fileID = request.json[0]['fileid']
		fileText = request.json[0]['fileText']
		cursor = cnx.cursor()
		args = [fileName, fileText]
		cursor.callproc('--', args)
	return "success"
	
@app.route('/newFile', methods = ['POST'])
def createNewFile():
	if request.method == 'POST':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		fileName = request.json[0]['fileName']
		projectID = request.json[0]['projectid']
		cursor = cnx.cursor()
		args = [fileName, projectID]
		cursor.callproc('AddNewFile', args)
	return "success"

@app.route('/addProject', methods = ['POST'])
def addProject():
	if request.method == 'POST':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		projectName = request.json[0]['projectname']
		programingLang = request.json[0]['language']
		userID = request.json[0]['uid']
		cursor = cnx.cursor()
		args = [projectName, programingLang, userID]
		cursor.callproc('AddProject', args)
	return "success"
	
@app.route('/getProject', methods = ['GET'])
def getProjects():
	if request.method == 'GET':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		username = request.json[0]['username']
		cursor = cnx.cursor()
		args = [username]
		cursor.callproc('GetProjects', args)
	return jsonify(data=cursor.fetchall())
	
@app.route('/getUserID', methods = ['GET'])
def getUserID():
	if request.method == 'GET':
		cnx - mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', dataBase = 'LiveCodeDocs')
		username = request.json[0]['username']
		cursor = cnx.cursor()
		args = [username]
		cursor.callproc('GetProjects', args)
	return jsonify(data=cursor.fetchall())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

