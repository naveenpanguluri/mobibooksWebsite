import json
from http.cookiejar import CookieJar
from urllib.request import urlopen,build_opener,install_opener,Request
from urllib.request import HTTPCookieProcessor
import traceback
import urllib.request
import time
import traceback
import urllib.error
import sys
#from LedgerGroup import LedgerGroup

class Mobibooks:

    def __init__(self,host,user,password,location,cust=None):

        if host is None or user is None or password is None:
            raise Exception("host,user,password can't be nulls")
        self.host = host
        self.url = 'http://' + host +'/act/api/'
        self.base_url = 'http://' + host + '/act/'
        self.user = user
        self.password = password
        self.is_logged_in = False
        self.auth_denied = False
        self.location = location
        self.location_id = None
        self.cust = cust

    def login(self):
        if self.is_logged_in:
            return True
        # Store the cookies and create an opener that will hold them
        cj = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))

        # Add our headers
        opener.addheaders = [('Content-Type','application/json; charset=UTF-8')]

        # Install our opener (note that this changes the global opener to the one
        # we just made, but you can also just call opener.open() if you want)
        install_opener(opener)

        # The action/ target from the form
        authentication_url = self.url + 'login/'

        # Input parameters we are going to send
        payload = json.dumps({ 'mobile': self.user,
            'password': self.password,'device_id':'11111111'}).encode('utf-8')

        # Use urllib to encode the payload
        # data = urllib.urlencode(payload)
        data = payload

        # Build our Request object (supplying 'data' makes it a POST)
        req = Request(authentication_url,
                data,{'Content-Type': 'application/json'})

        # Make the request and read the response
        try:
            cookies_set = False
            resp = urlopen(req)
            contents = resp.read()
            #print(contents)
            res = contents.decode('utf-8')
            o = json.loads(res)
            #import pprint
            #pprint.pprint(o)

            if 'tenant' in o and len(o['tenant']) > 1:
                #print ('Multi-tenant Access, Sent Location Access Request for {0} Location'.format(self.cust))
                for c in cj:
                    if c.name == 'csrftoken':
                        opener.addheaders = [('X-CSRFToken', c.value)]
                o = self.post('second_lg/',{'tenant_name':self.cust,'device_id':'11111111'})
                cookies_set = True
            locs = o['location']
            for l in locs:
                if self.location == l['display_name']:
                    self.location_id = l['id']
            if self.location_id is None:
                msg = 'ERROR: You are not allowed to Use the location {0}, Your locations are:'.format(self.location)
                i = 1
                for l in locs:
                    msg +=  "\t\t{0}. {1}".format(i,l['display_name'])
                    i +=1
                raise Exception(msg)
            self.is_logged_in = True
            self.user = o
            # set CSRF header
            if not cookies_set:
                for c in cj:
                    if c.name == 'csrftoken':
                        opener.addheaders = [('X-CSRFToken', c.value)]
                    cookies_set = True
        except urllib.error.HTTPError as e:
            if e.code == 401:
                self.auth_denied = True
            raise Exception('Authentication Failure, Reason[{0}]'.format(e.reason))
        except urllib.error.URLError as e:
            raise Exception('Authentication Failure, Reason[{0}]'.format(e.reason))
        except Exception as e:
            #traceback.print_exc()
            raise

    def post(self,url,payload,module='api'):
        url = self.base_url + module + '/' + url
        data = json.dumps(payload).encode('utf-8')
        #print (data)
        #print ('POST:',url)
        req = Request(url,data,{'Content-Type': 'application/json'})
        resp = urlopen(req)
        contents = resp.read()
        #print(contents)
        res = contents.decode('utf-8')
        if res is None or res == '':
            return ''
        else:
            o = json.loads(res)
            if 'error' in o: #Error Condition
                if o['error']['code'] == 5002:
                    return o
                else:
                    raise Exception('ERROR {0}, Reason:{1}'.format(o['error']['code'],o['error']['message']))
            return o


    def upload(self, url, fname):
        url = self.base_url + url

        with open(fname, 'rb') as f:
            data = f.read()
        print (type(data))
        req = Request(url, data,
                {'Content-Type': '*/*',
                'Content-Disposition':'attachment; filename={0}'.format(fname)})
        resp = urlopen(req)
        contents = resp.read()
        # print(contents)
        res = contents.decode('utf-8')
        if res is None or res == '':
            return ''
        else:
            o = json.loads(res)
            if 'error' in o:  # Error Condition
                raise Exception('ERROR {0}, Reason:{1}'.format(o['error']['code'], o['error']['message']))
            return o

    def get(self,url,payload,module='api'):
        url = self.base_url + module + '/' + url
        first_arg = True
        for key,val in payload.items():
            if first_arg:
                sep = '?'
                first_arg = False
            else:
                sep = '&'
            url += '{0}{1}={2}'.format(sep,key,val)
        print('GET ',url)
        req = Request(url,None,{'Content-Type': 'application/json'})
        try:
            resp = urlopen(req)
            contents = resp.read()
            #print(contents)
            res = contents.decode('utf-8')
            #print(res)
            return res
        except:
            traceback.print_exc()

    def test_avro(self,url,payload,module='api'):
        url = self.base_url + module + '/' + url
        data = json.dumps(payload).encode('utf-8')
        #print (data)
        #print ('POST:',url)
        req = Request(url,data,{'Content-Type': 'application/json'})
        resp = urlopen(req)
        contents = resp.read()
        #print(contents)

        #res = contents.decode('utf-8')
        res = contents
        if res is None or res == '':
            return ''
        else:
            #o = json.loads(res)
            #if 'error' in o:  # Error Condition
            #raise Exception('ERROR {0}, Reason:{1}'.format(o['error']['code'], o['error']['message']))
            return res




import unittest
class BooksTestCase(unittest.TestCase):

    def setUp(self):
        from config import HOST,USER,PASSWORD,CUSTOMER,LOCATION
        self.server = Mobibooks(HOST,USER,PASSWORD,LOCATION,CUSTOMER)
        self.server.login()
        print('-'*80)
        print("{0:4} {1:50} {2:6} {3}".format(' # ','TEST CASE NAME','RESULT','COMMENTS'))
        print('-'*80)
        self.tc_num = 0

    def print_report(self,tc_name,result,cmts):
        self.tc_num += 1
        print("{0:4} {1:50} {2:6} {3}".format(self.tc_num,tc_name,result,cmts))
