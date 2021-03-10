# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import copy
import datetime
import json
import logging
from datetime import timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
# from rest_framework import status
from rest_framework.decorators import permission_classes
# from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from railguns.django.generics import WebView
from ..articles.models import Article, UploadImage
from ..articles.tools import *

from django.conf import settings
dj_logger = logging.getLogger('django')


@permission_classes([AllowAny])
class TrourismHome(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'tourism-index.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Blog(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'blog.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class ConnectsUs(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'contact.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Tours(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'tours.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class AbountUs(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'about-us.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Register(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'register.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Faq(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'faq.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Login(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'login.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class DestinationDetail(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'destination-details.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Destination(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'destinations.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Booking(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'booking.html'
        return render(request, template_name, locals())


@permission_classes([AllowAny])
class Team(WebView):

    def get(self, request, *args, **kwargs):

        template_name = 'team.html'
        return render(request, template_name, locals())


class Dog(object):
    def __init__(self, index, gender, month, status, start_mon=0):
        self.id = index
        self.gender = gender
        self.month = month
        self.status = status
        self.start_mon = start_mon
        
        


@permission_classes([AllowAny])
class TestFactoryDog(APIView):

    def get(self, request, *args, **kwargs):
        return Response({})


def dogpre(start_dog_num, total_len):
    def gender_sum(testdata):
        gnum = 0
        bnum = 0
        if testdata:
            for m in testdata:
                if m.gender == 'girl':
                    gnum += 1
                else:
                    bnum += 1
            return [gnum, bnum]
        return [gnum, bnum]
    def process(dogs):
        sum_result = {'girl': {}, 'boy': {}}
        for item in dogs:
            if item.month in sum_result[item.gender].keys():
                sum_result[item.gender][item.month] += 1
            else:
                sum_result[item.gender][item.month] = 1
        return sum_result
    gstatus = ['born', 'young', 'grouping', 'preging', 'monther-5',]
    bstatus = ['born', 'young', 'cell']
    dogs = []
    sells = []
    for i in range(start_dog_num):
        # 头一批全部都是用13mon
        dogs.append(Dog(i, 'girl', 13, gstatus[2], ))
    i = 0
    total_count = start_dog_num
    wait_sell_num = 0
    rise_cost = 0
    while i < total_len:
        newdogs = []
        wait_sell = []
        for curdog in dogs:
            curdog.month += 1
            curdog.start_mon += 1
            if curdog.gender == 'girl':
                # o
                if curdog.status == gstatus[0]:
                    if curdog.start_mon == 5:
                        curdog.status = gstatus[1]
                        curdog.start_mon = 0
                        ds = 0
                        for k, v in process(dogs).get('girl').items():
                            if k >= 5:
                                ds += v
                        if ds > 20:
                            wait_sell.append(curdog)
                if curdog.status == gstatus[1]:
                    if curdog.start_mon == random.choice([10, 11, 12]) or curdog.start_mon == 12:
                        curdog.status = gstatus[2]
                        curdog.start_mon = 0
                if curdog.status == gstatus[2]:
                    # 准备期
                    if curdog.start_mon == random.choice([1, 2, 3]) or curdog.start_mon == 3:
                        curdog.status = gstatus[3]
                        curdog.start_mon = 0
                if curdog.status == gstatus[3]:
                    if curdog.start_mon == 2:
                        curdog.status = gstatus[4]
                        newnum = random.choice([3, 4, 5, 6, 7])
                        for v in range(newnum):
                            gender = random.choice(['girl', 'boy'])
                            newdogs.append(Dog(total_count, gender, 0, 'born'))
                            total_count += 1
                        print('mother-{}.old={}. chir={}'.format(curdog.id, curdog.month, newnum))
                        curdog.start_mon = 0
                if curdog.status == gstatus[4]:
                    if curdog.start_mon == random.choice([3, 4,]) or curdog.start_mon==4:
                        curdog.start_mon = 0
                        curdog.status = gstatus[2]
            else:
                if curdog.month == 5:
                    curdog.status = bstatus[1]
                    curdog.status = bstatus[2]
                    wait_sell.append(curdog)
        rise_cost += 30*len(dogs)
        gnum, bnum = gender_sum(newdogs)
        print('when i={}; born--{}; girl={}. bog={}'.format(i, len(newdogs), gnum, bnum ))
        dogs.extend(newdogs)
        for k in wait_sell:
            dogs.remove(k)
        print(i, len(dogs), len(wait_sell))
        i += 1
        wait_sell_num += len(wait_sell)
    return len(dogs), wait_sell_num, process(dogs), rise_cost, wait_sell_num*500-rise_cost-50*total_count-500*start_dog_num, total_count-5



def do_ex():
    i = 0
    rise = 0
    money = 0
    while i < 50:
        v = dogpre(30, 36)
        rise += v[5]
        money += v[4]
        i += 1
    ava_money = money/50
    ave_rise = rise/50
    return ava_money, ave_rise


