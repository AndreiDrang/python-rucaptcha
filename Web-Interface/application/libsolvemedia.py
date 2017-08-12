import requests


# solvemedia servers:
VERIFY_ANSWER_SERVER = "http://verify.solvemedia.com/papi/verify"


class SolveMedia:
    def __init__( self, ckey, vkey, hkey ):
        self.c_key = "xv5l9hrk6f2BGcEjj8nfKJopiM.WbuFO"
        self.v_key = "BRtLwz8cGCixeyIwd8Zz1W4WJ-7or5.y"
        self.h_key = "8vAvw0ginF2UoQmfGOkLVrmmS9zc3K4L"

    def answer_handler(self, user_answer, question):
        result = requests.post(VERIFY_ANSWER_SERVER,
                               data={
                                   "privatekey":self.v_key,
                                   "challenge":question,
                                   "response":user_answer
                               })
        print(result)
