from bottle import *
import argparse
import os
import sys
import subprocess
import multiprocessing
import time

__version__ = '0.1.0'
port = 8142
username = None
password = None
fileName = None
filePath = None

#Get the working directory for either a frozen app or dev app
if getattr(sys, 'frozen', False):
    #Set the path to the directory where the executable is located
    dir_path = sys._MEIPASS + os.sep
else:
    #Set the path the the directory where the script is located
    dir_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

#HTML routes
@get('/') 
def login():
    return template(dir_path + 'static/login.html',file_name=fileName,failed='hidden')

@post('/') 
def do_login():
    in_username = request.forms.get('uname')
    in_password = request.forms.get('pwd')

    if in_username == username and in_password == password:
        return static_file(fileName, root=filePath, download=fileName)
    else:
        return template(dir_path + 'static/login.html',file_name=fileName,failed='visible')

#Make command line arguments
def makeArgs():
     parser =  argparse.ArgumentParser('webFile FILENAME',
             formatter_class=argparse.RawTextHelpFormatter)
     parser.add_argument('filename',metavar='FILENAME',type=str,nargs=1,help='File to transfer')
     parser.add_argument('-u','--username',metavar='',type=str,nargs=1,help='username for login')
     parser.add_argument('-p','--password',metavar='',type=str,nargs=1,help='password for login')
     parser.add_argument('-v','--version',action='version',
             version='webFile version {}'.format(__version__),help='Display program version')
     return parser

def runServer():

    #Start server
    run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':

    #Make command line options
    parser = makeArgs()

    #Check input argument count
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    #Check if username password is required
    arguments = vars(parser.parse_args())
    if arguments['username'] != None and arguments['password'] == None or \
        arguments['username'] == None and arguments['password'] != None:
        print('Error: Must specify both username and password')
        sys.exit()
    elif arguments['username'] == None or arguments['password'] == None:
        print('Error: Need to specify a username and password')
        sys.exit()
    else:
        username = arguments['username'][0]
        password = arguments['password'][0]

    #Check input file exists
    if not os.path.exists(os.path.abspath(arguments['filename'][0])):
        print('Error: File {} does not exist'.format(arguments['filename'][0]))
        sys.exit()

    #Get file info
    filePath = os.path.dirname(os.path.abspath(arguments['filename'][0]))
    fileName = os.path.basename(arguments['filename'][0])

    #Start server
    server = multiprocessing.Process(target=runServer)
    server.start()
    
    #Start web tunnel
    subprocess.call(['ssh','-R', '80:localhost:{}'.format(port),'serveo.net'])

    #Program waits here for ctrl-c before continuing

    #Kill server
    server.terminate()

    #Done
    sys.exit()

