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
	print "not found in dictionary"	
	cnx = mysql.connector.connect(user = 'root', password = 'LiveCodeDocs', host = 'localhost', database = 'LiveCodeDocs')
        cursor = cnx.cursor()
        cursor.callproc('GetFileContent', [fileid])
	fileText = ""
        for result in cursor.stored_results():
                fileText = result.fetchall()
        cnx.close()
	newCodeObject = Code(fileText, fileid)
	codeStructures[fileid] = newCodeObject
	return fileText


def main():
	print checkOrMakeCodeStructure(1)


if __name__ == "__main__":
	main()
