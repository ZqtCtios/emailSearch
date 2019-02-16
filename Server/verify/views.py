
from django.shortcuts import render
from django.http import HttpResponse
from verify.models import UserMessage
import json
# Create your views here.


def check(userName, passwd):
    print(userName,passwd)
    dict = {}
    users = UserMessage.objects.filter(userId=userName, password=passwd)
    length = len(users)
    print(users)
    if length > 0:
        user = users[0]
        dict['userId'] = user.userId
        dict['userName'] = user.userName
        dict['date'] = str(user.date)
        dict['isVerified'] = user.isVerified
        dict['remainder'] = user.remainder
        dict['loginFlag'] = user.loginFlag
        user.loginFlag=1
        user.save()
    jsonStr = json.dumps(dict, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    return jsonStr


def verifyYes(request):
    userName = request.GET['user']
    passwd = request.GET['passwd']
    jsonstr = check(userName, passwd)
    return HttpResponse(jsonstr)
def quit(request):
    userName = request.GET['user']
    users = UserMessage.objects.filter(userId=userName)
    length=len(users)
    if length > 0:
        user = users[0]
        user.loginFlag=0
        user.save()
    return HttpResponse(user.loginFlag)
