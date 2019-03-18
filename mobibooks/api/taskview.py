


from api.headers import *
from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import datetime
from bookslib import validations
from bookslib.exceptions import *
from api.models import *


#logger info
import logging
_logger = logging.getLogger('gst')


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Task
        fields= ('id','mobile','phone','email','output_url','feedback')


class TaskViewSet(CompactViewSet):
    
    queryset= Task.objects.all()
    serializer_class = TaskSerializer
    


    def list(self,request):
        try:
            queryset= Task.objects.all()
            u = TaskSerializer(queryset,many = True)
            return Response(u.data,status=status.HTTP_200_OK)
        except:
            raise


   
    def create(self,request,**kwargs):

        try:
            o = Task()
            resp = o.create(request.data)
            return Response(resp,status=status.HTTP_200_OK)
        except BooksException as e:
            resp = {"error":{"code":e.code,"message":e.message}}
            return Response(resp,status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({'error':{'code':5000,'message':'Key Error-{0}'.format(e)}},status=status.HTTP_200_OK) 
        except Exception as e:
            #raise
            return Response({'error':{'code':5000,'message':'System Failure-{0}'.format(e)}},status=status.HTTP_200_OK) 
            
