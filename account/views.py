"""
login and logout
"""
# from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login(request):
    """
    return empty json, apikey,here sessionid, is sent through cookies
    """
    if request.method == 'POST':
        email = request.POST.get('username',None)
        password = request.POST.get('password',None)
        user = authenticate(username= email,password=password)
        if user is not None :
            auth_login(request,user)
            return JsonResponse(data={})
    response = JsonResponse(data={})
    response.status_code = 401
    return response

@csrf_exempt
def logout(request):
    """
    return empty json
    """
    if request.method == 'POST':
        if request.user.is_authenticated :
            auth_logout(request)
            return JsonResponse(data={})
    response = JsonResponse(data={})
    response.status_code = 401
    return response

@csrf_exempt
def raise_except(request):
    return None
