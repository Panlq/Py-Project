from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse, HttpResponse

from .models import HostLoginInof


def user_info(request):
    id_addr = request.META('REMOTE_ADDR')
    user_ua = request.META('HTTP_USER_AGENT')

    user_obj = User
