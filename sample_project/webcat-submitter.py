import argparse
import subprocess
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("assignment")
parser.add_argument("files", default=[], nargs='*')

args   = parser.parse_args()

target_url="https://web-cat.cs.vt.edu/Web-CAT/WebObjects/Web-CAT.woa/wa/assignments/eclipse?institution=ChristopherNewport" # VT's web-cat
#target_url="http://wc.pcs.cnu.edu:8080/Web-CAT/WebObjects/Web-CAT.woa/wa/assignments/eclipse?institution=CNU" # CNU's web-cat
submitter ="webcat-submitter-1.0.4.jar"
login_info="login.txt"  # This file built by CI file using WCUSER/WCPASS environment variables

valid_files = []
invalid_files=[]

source_dirs = ['./exam', './src'] # alternate: 'src'+args.program] for multiple separate submissions on exams
print("  Uploading ",source_dirs," to ",args.assignment," ...")

with open(login_info) as creds:
	temp = []
	for line in creds:
		temp.append(line.strip())
	(username,password) = tuple(temp)

runme = ['java', '-jar', submitter, '-t', target_url, '-u', username, '-p', password, '-a', args.assignment]
runme.extend(source_dirs)


#print(" runme<"+str(runme)+">")
o = ''
try:
	o = subprocess.run(runme, check=True, stdout=subprocess.PIPE).stdout.strip()
except subprocess.CalledProcessError as e:
	print('Something went wrong.')
	print(e.output)
	sys.exit(1)

if 'Your login information could not be validated' in str(o):
	sys.exit('Your login information (%s:%s) is incorrect' % (username, password) )
else:
	if ("The submission was successful" in str(o)):
		print('Submission Success!')
	else:
		print(" Submission failure :-( ")
		print(o)
		sys.exit(2)
