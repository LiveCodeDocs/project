import sys
import StringIO
import subprocess

def main():
	return


def runCode(stringCode):
	
	with open('tempFile.py', 'w') as tempFile:
		
		print stringCode
		tempFile.write(stringCode)
		# create file-like string to capture output
		codeOut = StringIO.StringIO()
		codeErr = StringIO.StringIO()

		# capture output and errors
		sys.stdout = codeOut
		sys.stderr = codeErr

		#subprocess.call("sudo -u nobody python tempFile.py", shell=True)		
		exec stringCode		

		# restore stdout and stderr
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

		s = codeErr.getvalue()

		print "error:\n%s\n" % s

		s = codeOut.getvalue()

		print "output:\n%s" % s

		codeOut.close()
		codeErr.close()
		return s
	

if  __name__ == "__main__":
	main()
