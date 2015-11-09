from codeChanges import *
import mysql.connector

codeStructures = {}

#will check if the requested file ID is already open as a Code obejct.
#if so, returns fetches the code from the open object
#if not fetches the code from the database, opens a new code project with that code, and returns the code

def checkOrMakeCodeStructure(fileid): #assumed fileid is an int
	if fileid in codeStructures.keys():
		requestedStruct = codeStructures[fileid]
		return requestedStruct.getCode()
	cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
        cursor = cnx.cursor()
        cursor.callproc('GetFileContent', [fileid])
	fileText = ""
        for result in cursor.stored_results():
                fileJSON = result.fetchall()
		fileText = fileJSON[0][1]
        cnx.commit()
	cnx.close()
	newCodeObject = Code(fileText, fileid)
	codeStructures[fileid] = newCodeObject
	return fileJSON

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
		print change
		#codeStructures[fileid].enqueueChange(change)
	#codeStructures[fileid].handleChanges()
	
if __name__ == "__main__":
	main()
