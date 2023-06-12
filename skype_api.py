from skpy import Skype
import os
import hashlib

FOLDER_NAME = "token"

def loginSkyeAPI(email,password):
    fileName = os.path.join(os.path.join(os.getcwd(), FOLDER_NAME),hashlib.sha256((email+password).encode('utf-8')).hexdigest())
    sk = Skype(email, password,fileName)

    if sk: 
        return True
    return False

def sendMessageToList(email,password,message,recipients):

    fileName = os.path.join(os.path.join(os.getcwd(), FOLDER_NAME),hashlib.sha256((email+password).encode('utf-8')).hexdigest())
    sk = Skype(email, password,fileName)
    notFoundContact = []
    messageSent = 0

    if sk:
        for contact in recipients:
            skypeContact = sk.contacts[contact]
            if skypeContact:
                messageSent += 1
                skypeContact.chat.sendMsg(message)
            else:
                notFoundContact.append(contact)
    
        return {"status":True,"messageSent":messageSent,"notFoundContact":notFoundContact}
    return {"status":False}

def sendMessageToAll(email,password,message):

    fileName = os.path.join(os.path.join(os.getcwd(), FOLDER_NAME),hashlib.sha256((email+password).encode('utf-8')).hexdigest())
    sk = Skype(email, password,fileName)
    messageSent = 0

    if sk:
        for skypeContact in sk.contacts:
            if skypeContact:
                skypeContact.chat.sendMsg(message)
                messageSent += 1
        return {"status":True,"messageSent":messageSent}
    return {"status":False}
        
def getContacts(email,password):
    fileName = os.path.join(os.path.join(os.getcwd(), FOLDER_NAME),hashlib.sha256((email+password).encode('utf-8')).hexdigest())
    sk = Skype(email, password,fileName)

    contacts = []

    if sk: 
        for contact in sk.contacts:
            
            new = {}

            print(contact)
            if contact.id != None:
                new['skype_id'] = contact.id

                if contact.name != None:
                    if contact.name.first != None:
                        new['name'] = contact.name.first
                    if contact.name.last != None:
                        new['surname'] = contact.name.last
                if contact.location != None:
                    new['location'] = contact.location.country   
                if contact.language != None:
                    new['language'] = contact.language    
                if contact.phones != None:
                    new['phone'] = contact.phones  

                contacts.append(new)
        
        return {"status":True, "contacts": contacts}
    return {"status":False}
