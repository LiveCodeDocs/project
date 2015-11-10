from codeChanges import *
import json
from flask import jsonify
import mysql.connector

codeStructures = {}

#will check if the requested file ID is already open as a Code obejct.
#if so, returns fetches the code from the open object
#if not fetches the code from the database, opens a new code project with that code, and returns the code

def checkOrMakeCodeStructure(fileid): #assumed fileid is an int
	if fileid in codeStructures.keys():
		codeBody = codeStructures[fileid].getCode()
		return jsonify({'code': codeBody})
	cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
        cursor = cnx.cursor()
        cursor.callproc('GetFileContent', [fileid])
	fileText = ""
        for result in cursor.stored_results():
                fileJSON = result.fetchall()
		print fileJSON
		fileText = fileJSON[0][1]
        cnx.commit()
	cnx.close()
	newCodeObject = Code(fileText, fileid)
	codeStructures[fileid] = newCodeObject
	return jsonify(fileJSON)

def pullCodeChanges(fileid):
	if fileid not in codeStructures.keys():
		print 'code object not open for that file'
		return False		
	return codeStructures[fileid].getCode()

#fileid - int of the file id
#codeChanges
def setCodeChanges(fileid, codeChanges):
	if fileid not in codeStructures.keys():
		return False #shouldnt be sending code changes to a file that is not currently open - something probably broke
	for change in codeChanges:
		#print change
		changeDict = parseRawChange(str(change))
		changeList = setupChangeObject(changeDict)
		if len(changeList) == 3:
			print changeList
			#codeStructures[fileid].enqueueChange(Change(changeList[0], changeList[1], changeList[2]))
		else:
			print changeList
			#codeStructures[fileid].enqueueChange(Change(changeList[0], changeList[1], changeList[2], changeList[3]))
	#codeStructures[fileid].handleChanges()
	
def parseRawChange(dump):
    parsedChangeDict = {}
    lineList = []
    indexList = []

    cleaned = dump[1:len(dump) - 1]
    cleaned = cleaned.replace('{', '')
    cleaned = cleaned.replace('}', '')
    cleaned = cleaned.replace(' ', '')
    cleanedList = cleaned.split(',')
    for item in cleanedList:
        item = item.replace('"', '')
        changeList = item.split(':')
#        print changeList
        if changeList[0] == 'u\'origin\'':
            parsedChangeDict['change_type'] = changeList[1][3: len(changeList[1]) - 1]
        if changeList[0] == 'u\'line\'':
            lineList.insert(0, int(changeList[1]))
        if changeList[0] == 'u\'ch\'':
            indexList.insert(0, int(changeList[1]))
#         not needed now - keeping the code in case this is necessary later
#         if changeList[0] == 'removed':
#             removed_text = changeList[1].replace('[', '')
#             removed_text = removed_text.replace(']', '')
#             parsedChangeDict['removed_text'] = removed_text
        if changeList[0] == 'u\'text\'':
            inserted_text = changeList[1][3: len(changeList[1]) - 2]
            parsedChangeDict['inserted_text'] = inserted_text
        if changeList[0] == 'u\'to\'':
            if changeList[1] == 'u\'line\'':
                lineList.insert(0, int(changeList[2]))
        if changeList[0] ==  'u\'from\'':
	    if changeList[1] == 'u\'line\'':
		lineList.insert(0, int(changeList[2]))

    parsedChangeDict['line_range'] = lineList
    parsedChangeDict['index_range'] = indexList
    return parsedChangeDict

def setupChangeObject(parsedChangeDict):
    changeObjectList = []
    if parsedChangeDict['change_type'] == 'delete':
        changeObjectList = ['', '', '']
        changeObjectList[1] = Change.delete
        changeObjectList[0] = (parsedChangeDict['line_range'][0], parsedChangeDict['line_range'][1])
        changeObjectList[2] = (parsedChangeDict['index_range'][0], parsedChangeDict['index_range'][1])
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
    

if __name__ == "__main__":
	main()
