__author__ = 'cristian'

from json import dumps

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginD
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(req):
    print(req.user)
    return render_to_response('index.html', dict(), RequestContext(req))


def login(req):
    res = dict()
    if req.method == 'POST':
        d = req.POST
        print(d)
        user = d.get('user', None)
        passw = d.get('pass', None)
        if user is None or passw is None:
            res['msg'] = 'Faltan campos para loguearse'
        else:
            user = authenticate(username=user, password=passw)
            if user is None:
                res['msg'] = 'Usuario y/o contraseña incorrecto'
            elif user.is_active:
                loginD(req, user)
                return HttpResponseRedirect('/')
            else:
                res['msg'] = 'Cuenta desactivada'
    return render_to_response('login.html', res, RequestContext(req))


def register(req):
    res = dict()
    if req.method == 'POST':
        d = req.POST
        user = d.get('user', None)
        passw = d.get('pass', None)
        email = d.get('email', None)
        print(d)
        if user is None or passw is None or email is None:
            res['msg_reg'] = 'Falta uno de los campos para completar el registro'
        else:
            user = User.objects.create_user(user, email, passw)
            if user is None:
                res['msg_reg'] = 'No fue posible registrar al usuario'
            else:
                res['success_reg'] = 'Usuario registrado con éxito'
        return render_to_response('login.html', res, RequestContext(req))
    return Http404()