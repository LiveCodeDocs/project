from codeChanges import *
import json
from flask import jsonify
import mysql.connector
from Queue import Queue
import time
from threading import Thread

codeStructures = {}


def requestCode(fileid):
	codeStructures[fileid]['request_queue'].put(1)
	done = False
	while not done:
		if not codeStructures[fileid]['out_queue'].empty():
			done = True
	code = codeStructures[fileid]['out_queue'].get()
	print code
	return code

def commitTimer(fileid):
	while True:    
		time.sleep(5)
   		exportCode(fileid)

#will check if the requested file ID is already open as a Code obejct.
#if so, returns fetches the code from the open object
#if not fetches the code from the database, opens a new code project with that code, and returns the code

def checkOrMakeCodeStructure(fileid): #assumed fileid is an int
	if fileid in codeStructures.keys():
		codeBody = requestCode(fileid)
		return jsonify({'code': codeBody})

	cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
        cursor = cnx.cursor()
        cursor.callproc('GetFileContent', [fileid])
	fileText = ""
        for result in cursor.stored_results():
                fileJSON = result.fetchall()
		fileText = fileJSON[0][1]
        cnx.commit()
	cnx.close()

	codeObjectDict = {}
	codeChangeQueue = Queue()
	codeRequestQueue = Queue()
	codeOutQueue = Queue()
	newCodeObject = Code(codeChangeQueue, codeRequestQueue, codeOutQueue, fileText, fileid)
	codeObjectDict['change_queue'] = codeChangeQueue
	codeObjectDict['request_queue'] = codeRequestQueue
	codeObjectDict['out_queue'] = codeOutQueue
	codeObjectDict['code_object'] = newCodeObject
	codeStructures[fileid] = codeObjectDict
	codeStructures[fileid]['code_object'].start()
	t = Thread(target = commitTimer, args = (fileid,))
	t.start()
	return jsonify(fileJSON)

def pullCodeChanges(fileid):
	if fileid not in codeStructures.keys():
		print 'code object not open for that file'
		return False		
	thecode = requestCode(fileid)
	return thecode[0:len(thecode) - 1]

#fileid - int of the file id
#codeChanges
def setCodeChanges(fileid, codeChanges):
	if fileid not in codeStructures.keys():
		return False #shouldnt be sending code changes to a file that is not currently open - something probably broke
	for change in codeChanges:
		#print json.dumps(change)
		changeDict = parseRawChange(json.dumps(change))
		changeList = setupChangeObject(changeDict)
		if len(changeList) == 3:
			codeStructures[fileid]['change_queue'].put(Change(changeList[0], changeList[1], changeList[2]))
		else:
			codeStructures[fileid]['change_queue'].put(Change(changeList[0], changeList[1], changeList[2], changeList[3])) 

def exportCode(fileid):
    codeBody = requestCode(fileid) 
    cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
    cursor = cnx.cursor()
    cursor.callproc('UpdateFileContent', [fileid, codeBody])
    cnx.commit()
    cnx.close()	

def parseRawChange(dump):
    parsedChangeDict = {}
    lineList = []
    indexList = []

    cleaned = dump
    cleanedList = cleanList(cleaned)
    for item in cleanedList:
        changeList = item.split(':', 1)
        stripped = changeList[0].lstrip().rstrip()
        changeList[0] = stripped[1:len(stripped) - 1]
     	#print changeList
        if changeList[0] == 'origin':
            parsedChangeDict['change_type'] = changeList[1][3: len(changeList[1]) - 1]
        if changeList[0] == 'line':
            lineList.insert(0, int(changeList[1]))
        if changeList[0] == 'ch':
	    if changeList[1][-1:] == '}':
		changeList[1] = changeList[1][:-1]
            indexList.insert(0, int(changeList[1]))
        if changeList[0] == 'text':
            textList = changeList[1].split(',')
            textList = textList[len(textList) - 1]
            textList = textList.lstrip()
            textList = textList[1 : len(textList) - 1]
            if textList:
                textList = textList[1:]
            parsedChangeDict['inserted_text'] = textList
        if changeList[0] == 'to':
            newSplit = changeList[1].split(':')
            newSplit[0] = newSplit[0].lstrip()
            newSplit[0] = newSplit[0].rstrip()
            word = newSplit[0][2: len(newSplit[0]) - 1]
            if word == 'line':
                lineno = newSplit[1]
                lineList.insert(0, int(lineno))
        if changeList[0] ==  'from':
            newSplit = changeList[1].split(':')
            newSplit[0] = newSplit[0].lstrip()
            newSplit[0] = newSplit[0].rstrip()
            if changeList[1] == 'line':
                lineno = newSplit[1]
                lineList.insert(0, int(lineno))

    parsedChangeDict['line_range'] = lineList
    parsedChangeDict['index_range'] = indexList
    return parsedChangeDict

def setupChangeObject(parsedChangeDict):
    changeObjectList = []
    if parsedChangeDict['change_type'] == 'delete':
        changeObjectList = [[], '', []]
        changeObjectList[1] = Change.delete
	for lnum in parsedChangeDict['line_range']:
		changeObjectList[0].append(lnum)
	for inum in parsedChangeDict['index_range']:
		changeObjectList[2].append(inum)
        #changeObjectList[0] = (parsedChangeDict['line_range'][0], parsedChangeDict['line_range'][1])
        #changeObjectList[2] = (parsedChangeDict['index_range'][0], parsedChangeDict['index_range'][1])
    if parsedChangeDict['change_type'] == 'input':
        if parsedChangeDict['inserted_text'] == '':
            changeObjectList = ['', '', '']
            changeObjectList[1] = Change.newLine

        else:
            changeObjectList = ['', '', '', '']
            changeObjectList[1] = Change.insert
            changeObjectList[3] = parsedChangeDict['inserted_text']

        changeObjectList[0] = int(parsedChangeDict['line_range'][0])
        changeObjectList[2] = parsedChangeDict['index_range'][0]

    return changeObjectList

def cleanList(dump):
    commano = commaCount(dump)
    if commano > 8:
	myDump = dump.split(',', commano)
    else:
    	myDump = dump.split(',' , 8)
    parsedDump = []
    for i in range (0, len(myDump)):  
         if i == 0:
                parsedDump.insert(0, myDump[0][2:])
                
         elif i == (len(myDump) - 1):
                parsedDump.insert(i, myDump[i][0:len(myDump[i]) - 3])
                
         else:
                parsedDump.insert(i, myDump[i])

    return parsedDump

def commaCount(dump):
    count = 0
    for c in dump:
	if c == ',':
	    count += 1
    return count
if __name__ == "__main__":
	main()
