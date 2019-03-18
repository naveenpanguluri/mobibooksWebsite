
class BooksException(Exception):
 
    def __init__(self,code,message):
        self.code = code
        self.message = message

class BooksPathException(Exception):
 
    def __init__(self,code,message,path):
        self.code = code
        self.message = message
        self.path = path

class MandatoryFieldException(Exception):
 
    def __init__(self,code,message):
        self.code = code
        self.message = message

class IdNotMatchedException(Exception):
    
    def __init__(self,code,message):
        self.code = code
        self.message = message
                                    

class StoreVoucherException(Exception):
    
    def __init__(self,code,message):
        self.code = code
        self.message = message

class NoDataReceivedException(Exception):
    def __init__(self,code,message):
        self.code = code
        self.message = message

class GlSlDeletedException(Exception):
    def __init__(self,code,message,gl_id,sl_id):
        self.code = code
        self.message = message
        self.gl_id = gl_id
        self.sl_id = sl_id

"""
class NodataslException(Exception):
    def __init__(self,code,message,gl_id):
        self.code=code
        self.message = message
        self.gl_id=gl_id

class NodataglException(Exception):
    def __init__(self,code,message,sl_id):
        self.code=code
        self.message = message
        self.sl_id=sl_id
class DeletedException(Exception):
    def __init__(self,code,message,gl_id,sl_id):
        self.code = code
        self.message = message
        self.gl_id = gl_id
        self.sl_id = sl_id
"""
