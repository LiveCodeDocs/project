import sys
import StringIO
import subprocess
import os
import threading

def main():
	return


def runCode(stringCode):
	
	tempFile = open('a.py', 'w')
	tempFile.write(stringCode)
	tempFile.close()
		# create file-like string to capture output
		#codeOut = StringIO.StringIO()
		#codeErr = StringIO.StringIO()

		# capture output and errors
		#sys.stdout = codeOut
		#sys.stderr = codeErr

		#subprocess.call("sudo -u nobody python tempFile.py", shell=True)		
	
	proc = subprocess.Popen('sudo -u nobody python a.py', shell=True, stdout=subprocess.PIPE)	
	out_iter = iter(proc.stdout.readline, b"")
	userOut = ""
	for line in out_iter:
		print line	
		userOut += line

	proc.wait()
	return userOut
	#	# restore stdout and stderr
		#sys.stdout = sys.__stdout__
		#sys.stderr = sys.__stderr__
		#s = codeErr.getvalue()

		#print "error:\n%s\n" % s

		#s = codeOut.getvalue()

		#print "output:\n%s" % s

		#codeOut.close()
		#codeErr.close()
		#return s
	

if  __name__ == "__main__":
	main()
