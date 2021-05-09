from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
from pprint import pprint
from user_agent import generate_user_agent

app_id = '1b5de0ab1bb24acd8f0d5fa416e64125'
app_key = '-yJtQSEZp1JPO-A8LZAGGsDrqPE'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
def crawl(addr):
    a = Auth(app_id, app_key)
    response = request('get', addr,  headers= a.get_auth_header())
    return response


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$top=30&$format=JSON',  headers= a.get_auth_header())
    print(a.get_auth_header())
    for i in range(0,30):
        print(response.json()[i]["StopName"]["Zh_tw"])