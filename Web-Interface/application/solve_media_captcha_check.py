import requests
import json
from flask import Response

# solvemedia server:
VERIFY_ANSWER_SERVER = "http://verify.solvemedia.com/papi/verify"


class SolveMedia:
    def __init__( self):
        self.c_key = "xv5l9hrk6f2BGcEjj8nfKJopiM.WbuFO"
        self.v_key = "BRtLwz8cGCixeyIwd8Zz1W4WJ-7or5.y"
        self.h_key = "8vAvw0ginF2UoQmfGOkLVrmmS9zc3K4L"

    def answer_handler(self, user_answer, question, user_ip):
        result = requests.post(VERIFY_ANSWER_SERVER,
                               data={
                                   "privatekey":self.v_key,
                                   "challenge":question,
                                   "response":user_answer,
                                   "remoteip": user_ip
                               }).text.split('\n')
        
        # Оценка ответа юзера
        if result[0] == 'true':
            # Если капча решена верно
            data = {'request': 'OK'}
    
            js = json.dumps(data)
    
            response = Response(js, status=200, mimetype='application/json')
            response.headers['Link'] = 'http://85.255.8.26/'
    
            return response
        else:
            # Если при обработке капчи были проблемы
            # возвращется отказ и описание ошибки
            data = {'request': 'FAIL', 'mistake': result[1]}
    
            js = json.dumps(data)
    
            response = Response(js, status=200, mimetype='application/json')
            response.headers['Link'] = 'http://85.255.8.26/'
    
            return response
