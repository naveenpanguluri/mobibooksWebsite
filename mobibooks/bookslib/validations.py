from datetime import datetime
from decimal import Decimal
import datetime
from bookslib.exceptions import *
import logging
import datetime
_logger = logging.getLogger("act")


def mandatory_check( mandatory_fields, dic):
    for field in mandatory_fields:
        if field not in dic:
            raise BooksException(code = 5006, message = "Field-Missing-{0}".format(field))


def get_name(display_name):
    return ''.join(e.upper() for e in display_name if e.isalnum())



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def initprop (key, dic, obj, mandatory = False):
    field = getattr(obj,key)
    if key in dic:
        if field is None:  # Nullable field,req data type takes priority
            if type (dic[key]) == str:
                new_val = str(dic[key].strip())
                if len(new_val) == 0:
                    new_val = None
            else:
                new_val = dic[key]
        elif type(field) == str: 
            new_val = str(dic[key].strip())
            if len(new_val) == 0:
                new_val = None
        elif type(field) == int: 
            new_val = int(dic[key])
        elif type(field) == datetime.datetime:
            new_val = datetime.strptime(dic[key], "%Y-%m-%d")
        elif type(field) == Decimal:
            new_val = Decimal(str(dic[key]))
        elif type(field) == bool:
            new_val = True if  dic[key] in ['Yes', 'True',1,True] else False
        else:
            print(type(key))
            raise Exception ('Unknown Data type {0}->{1}'.format(key,type(field)))
        setattr(obj,key,new_val)
    else:
        if mandatory:
            raise Exception ('Missing Field: {0}'.format(key))


def setprop (key, dic, obj, mandatory = False,history=True,foreign_key=[],db=None):
    h = ''
    field = getattr(obj,key)
    if key in dic:
        if field is None:  # Nullable field,req data type takes priority
            if type (dic[key]) == str:
                new_val = str(dic[key].strip())
                if len(new_val) == 0:
                    new_val = None
            else:
                new_val = dic[key]
        elif type(field) == str:
            _logger.info(dic[key])
            new_val = str(dic[key].strip())
            if len(new_val) == 0:
                new_val = None
        elif type(field) == int: 
            new_val = int(dic[key])
        elif type(field) == datetime.datetime:
            new_val = datetime.datetime.strptime(dic[key], "%Y-%m-%d")
        #adding here
        elif type(field) == datetime.time:
            t= datetime.date.today().strftime("%Y-%m-%d")+' '+dic[key]
            new_val=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M').time()
            #new_val = datetime.datetime.strptime(dic[key],'%H:%M').time()
        elif type(field) == Decimal:
            new_val = Decimal(str(dic[key]))
        elif type(field) == bool:
            new_val = True if  dic[key] in ['Yes', 'True',1,True] else False
        else:
            raise Exception ('Unknown Data type {0}'.format(key))

        if field != new_val: # changed
            obj.is_modified = True
            # Added on 13-12-2016
            if foreign_key != [] and key in foreign_key:
                if history:
                    for one_key in foreign_key:
                        if key == one_key and one_key[-2:] == 'id':
                            key_name = one_key.replace('','')[:-3]
                            if hasattr(getattr(obj,key_name) ,'display_name'):
                                old_name = getattr(obj,key_name).__class__.objects.using(db).get(pk=new_val).display_name
                                h = " {0} : {1} -> {2} ; ".format(key_name,getattr(obj,key_name).display_name,old_name)
                            elif hasattr(getattr(obj,key_name), 'name'):
                                old_name = getattr(obj,key_name).__class__.objects.using(db).get(pk=new_val).name
                                h  = " {0} : {1} -> {2} ; ".format(key_name,getattr(obj,key_name).name,old_name)
            else:
                h =" {0} : {1} -> {2} ; ".format(key,str(field),str(new_val))

            setattr(obj,key,new_val)
    else:
        if mandatory:
            raise Exception ('Missing Field: {0}'.format(key))
    return h



def num_digits(num):
    count = 0
    if num == 0:
        count += 1
    while num > 0 or num < 0:
        if num < 0:
            num = -1 * num
        count += 1
        num = int(num/10)

    return count
