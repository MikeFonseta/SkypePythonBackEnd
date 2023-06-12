from flask import Flask
from flask import request
from response import ResponseBody,ResponseType
from skype_api import loginSkyeAPI
from skype_api import sendMessageToList
from skype_api import sendMessageToAll
from skype_api import getContacts
from datetime import datetime

app = Flask(__name__)

@app.route('/skype/login', methods=['POST'])
def login():
    # try:
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        if 'email' in data and 'password' in data:
            result = loginSkyeAPI(data['email'],data['password'])
            if result:
                return ResponseBody(ResponseType.OK,"Authentication successful")
            else:
                return ResponseBody(ResponseType.FAILED,"Authentication failed")
        return ResponseBody(ResponseType.FAILED,"Skype email or passowrd is missing")
    else:
        return ResponseBody(ResponseType.FAILED,"Content-Type not supported")
    # except Exception as e:
    #     writeLOG(request.remote_addr, e)
    #     return ResponseBody(ResponseType.ERROR,"Authentication failed")

@app.route('/skype/contacts', methods=['POST'])
def contacts():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
            if 'email' in data and 'password' in data:
                result = getContacts(data['email'],data['password'])
                if result['status']:
                    if result['contacts'] != []:
                        return ResponseBody(ResponseType.OK,contacts=result['contacts'])
                    else:
                        return ResponseBody(ResponseType.OK,"No contacts found")
                else:
                    return ResponseBody(ResponseType.FAILED,"Error during contact retrieval")
            return ResponseBody(ResponseType.FAILED,"Skype email or passowrd is missing")
        else:
            return ResponseBody(ResponseType.FAILED,"Content-Type not supported")
    except Exception as e:
        writeLOG(request.remote_addr, e)
        return ResponseBody(ResponseType.ERROR,"Error during the processing of the request, check entered parameters")

@app.route('/skype/sendMessage/list', methods=['POST'])
def sendMessageList():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
            if 'skype' in data:
                if 'email' in data['skype'] and 'password' in data['skype']:
                    if 'recipients' in data and 'message' in data:
                        if len(data['recipients']) > 0 and len(data['message'].strip()):
                            result = sendMessageToList(data['skype']['email'],data['skype']['password'],data['message'],data['recipients'])

                            if result['status']:
                                return ResponseBody(ResponseType.OK,"Message sent to " + str(result['messageSent']) + " contacts")
                            else:
                                return ResponseBody(ResponseType.NOT_SENT_TO_ALL,"Message not sent to all recipients", result['notFoundAccount'])
                        elif not len(data['message'].strip()):
                            return  ResponseBody(ResponseType.FAILED,"Invalid message")
                        else:
                            return ResponseBody(ResponseType.FAILED,"Enter at least one recipient")
                    return ResponseBody(ResponseType.FAILED,"Message or recipients is missing") 
                return ResponseBody(ResponseType.FAILED,"Skype email or passowrd is missing")
            return ResponseBody(ResponseType.FAILED,"Skype param is missing") 
        else:
            return ResponseBody(ResponseType.FAILED,"Content-Type not supported")
    except Exception as e:
        writeLOG(request.remote_addr, e)
        return ResponseBody(ResponseType.ERROR,"Error during the processing of the request, check entered parameters")

@app.route('/skype/sendMessage/all', methods=['POST'])
def sendMessageAll():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
            if 'skype' in data:
                if 'email' in data['skype'] and 'password' in data['skype']:
                    if 'message' in data:
                        if len(data['message'].strip()):
                            result = sendMessageToAll(data['skype']['email'],data['skype']['password'],data['message'])
                            if result['status']:
                                return ResponseBody(ResponseType.OK,"Message sent to "+ str(result['messageSent']) + " contacts")
                            else:
                                return ResponseBody(ResponseType.FAILED,"Error while sending message")
                        elif not len(data['message'].strip()):
                            return  ResponseBody(ResponseType.FAILED,"Invalid message")
                    return ResponseBody(ResponseType.FAILED,"Message is missing") 
                return ResponseBody(ResponseType.FAILED,"Skype email or passowrd is missing")
        else:
            return ResponseBody(ResponseType.FAILED,"Content-Type not supported")
    except Exception as e:
        writeLOG(request.remote_addr, e)
        return ResponseBody(ResponseType.ERROR,"Error during the processing of the request, check entered parameters")

def writeLOG(ip, message,filename="log"):
    f = open(filename, "a")
    f.write("[" + ip + datetime.now().strftime(" - %d/%m/%Y %H:%M:%S]") + " " + str(message) +"\n")
    f.close()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)