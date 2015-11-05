from codeChanges import *
import mysql.connector

codeStructures = {}

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
