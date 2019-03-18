from api.models import Idgen

def get_id(db):
    i = None
    while 1:
        id_gen = Idgen.objects.using(db).all()[0]
        i = id_gen.id
        resp = id_gen.delete()
        if i != None and resp[0]==1:
            break
    return i


