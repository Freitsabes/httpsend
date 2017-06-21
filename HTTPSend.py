import httplib
import time
import sys

https = 0
quiet = 0

# Benutzung:
#
# python HTTPSend.py [-s] [-q] filename.http [filename1.http] ...
# Arbeitet die Files ab in der genannten Reihenfolge
# Falls -s gegeben ist, dann https, sonst http
# Falls -q gegeben ist, dann keine output der response in der shell.
#
# sebastian.freitag@vispiron.de
#
# Zukuenftige Verbesserungen:
#  - Auch Ordner angeben, requests dann in alphabetischer Reihenfolge
#  - Besseres Error-Handling

current_milli_time = lambda: int(round(time.time() * 1000))


def setOptionHttps():
    global https
    https = 1

def setOptionQuiet():
    global quiet
    quiet = 1

class Request:
    def __init__(self):
        self.host = ''
        self.port = ''
        self.target = ''
        self.headers = {}
        self.body = ''
        self.method = ''
        self.httpVersion = ''


def readRequest(filename):
    global https
    myFile = open(filename, 'rb')
    returnRequest = Request()
    while True:
        fieldName = ''
        fieldValue = ''
        line = myFile.readline()
        if line == '\r\n':
            break
        if line == '':
            break
        headerField = line.split(':', 1)
        if len(headerField) < 2:
            # this is either the start line
            # or
            # we have a bad header field
            startLine = line.split(' ')
            if len(startLine) == 3:
                returnRequest.method = startLine[0]
                returnRequest.target = startLine[1]
                returnRequest.httpVersion = startLine[2].strip()
            else:
                print 'WARNING! INVALID HEADER LINE FOUND'
                print startLine[0]
            continue
        else:
            if headerField[0] == 'Content-Length':
                # we ignore this because httplib sets it automatically
                print 'WARNING! Content-Length IS IGNORED'
                print 'HTTPLIB WILL SET IT AUTOMATICALLY'
                continue
            else:
                fieldName = headerField[0]
                fieldValue = headerField[1].strip()
        if fieldName == 'Host':
            # set all the connection stuff
            hostList = fieldValue.split(':')            
            returnRequest.host = hostList[0]
            if len(hostList) == 2:
                returnRequest.port = hostList[1]
        returnRequest.headers[fieldName] = fieldValue
        
    returnRequest.body = myFile.read()
    myFile.close()
    
    if https == 1 and returnRequest.port == '':
        print 'WARNING! NO PORT GIVEN WITH HTTPS FLAG (-s)'
        print 'I SET PORT TO 443'
        returnRequest.port = '443'
    if https == 0 and returnRequest.port == '':
        print 'WARNING! NO PORT GIVEN'
        print 'I SET PORT TO 80'
        returnRequest.port = '80'
    
    return returnRequest

    
def readArgs(args):
    returnArray = []
    options = {'-s': setOptionHttps, '-q': setOptionQuiet}
    for arg in args[1:]:
        if arg[:1] == '-':
            options[arg]()
        else:
            thisrequest = readRequest(arg)
            returnArray.append(thisrequest)
    return returnArray


myArgs = sys.argv
myRequests = readArgs(myArgs)
for request in myRequests:
    startTime = current_milli_time()
    myHost = ':'.join([request.host, request.port])
    if https == 0:
        myConnection = httplib.HTTPConnection(myHost)
    else:
        myConnection = httplib.HTTPSConnection(myHost)
    if len(request.body) == 0:
        myConnection.request(request.method,
                             request.target,
                             headers=request.headers)
    else:
        myConnection.request(request.method,
                             request.target,
                             request.body,
                             request.headers)
    myResponse = myConnection.getresponse()

#    print len(myResponse.read())
    if not quiet:
        print 'Response:'
        print ''
        print myResponse.read()
    print ''
    print 'It took time to perform this request:'
    print str(current_milli_time() - startTime) + ' milliseconds!'    
    myConnection.close()
