from enum import Enum
 
class ResponseType(Enum):
    OK = 'OK'
    FAILED = 'FAILED'
    NOT_SENT_TO_ALL = 'NOT_SENT_TO_ALL'
    ERROR = 'ERROR'


def ResponseBody(responseType: ResponseType , message = "", notFoundAccount = [], contacts = []):

    if responseType == ResponseType.OK:
        if contacts:
                return {'response': ResponseType.OK.value, 'contacts': contacts}
        return {'response': ResponseType.OK.value, 'message': message}
    if responseType == ResponseType.FAILED:
        return {'response': ResponseType.FAILED.value, 'message': message}
    if responseType == ResponseType.NOT_SENT_TO_ALL:
        if notFoundAccount:
                return {'response': ResponseType.NOT_SENT_TO_ALL.value, 'message': message, "not_found_account": notFoundAccount}
    if responseType == ResponseType.ERROR:
        return {'response': ResponseType.ERROR.value, 'message': message}
    
    return {'ERROR', 'Generic error'}
