__author__ = 'cristian'

from django.shortcuts import render_to_response


def pay(req):
    if req.method == 'GET':
        return render_to_response('payment.html')