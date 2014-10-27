__author__ = 'cristian'

from json import dumps

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import ObjectDoesNotExist

from IyE.models import UserDetail


def index(req):
    """ Returns the site's homepage
    """
    return render_to_response('index.html', RequestContext(req))


def login(req):
    """ It presents the login and registration forms
    We use another url to make the POST of the registration form
    """
    res = dict()
    if req.method == 'POST':
        d = req.POST
        user = d.get('user', None)
        passw = d.get('pass', None)
        if user is None or passw is None:
            res['msg'] = 'Faltan campos para loguearse'
        else:
            user = authenticate(username=user, password=passw)
            if user is None:
                res['msg'] = 'Usuario y/o contraseña incorrecto'
            elif user.is_active:
                login_user(req, user)
                return HttpResponseRedirect('/')
            else:
                res['msg'] = 'Cuenta desactivada'
    return render_to_response('login.html', res, RequestContext(req))


def register(req):
    """ Handler of the POSTs from the registration form
    """
    res = dict()
    if req.method == 'POST':
        d = req.POST
        user = d.get('user', None)
        passw = d.get('pass', None)
        email = d.get('email', None)
        res['msg_type'] = 'error'
        res['redirect'] = '/user/login'
        if user is None or passw is None or email is None:
            res['msg'] = 'Falta uno de los campos para completar el registro'
        else:
            user = User.objects.create_user(user, email, passw)
            if user is None:
                res['msg'] = 'No fue posible registrar al usuario'
            else:
                res['msg'] = 'Usuario registrado con éxito'
                res['msg_type'] = 'success'
        return render_to_response('msg.html', res, RequestContext(req))
    return Http404()


def contact(req):
    """ It presents the contact form
    TODO:
        We have to append the message and send it to our mail ->
            d[name]     ==  user's fullname
            d[email]    ==  user's email
            d[msg]      ==  user's message
    """
    if req.method == 'GET':
        return render_to_response('contact.html')
    else:
        d = req.POST
        res = dict()
        res['msg'] = 'Éxito enviando el mensaje'
        res['msg_type'] = 'success'
        res['redirect'] = '/contact'
        return render_to_response('msg.html', res)


def about(req):
    """ It presents information about us
    TODO:
        Maybe will be a good idea to check the actual content of this section
    """
    return render_to_response('about.html', RequestContext(req))


def cart(req):
    """ Currently doesn't work, it only presents the HTML
    """
    return render_to_response('cart.html')


def user_info(req):
    res = dict()
    if req.method == 'POST':
        d = req.POST
        try:
            detail = UserDetail.objects.get(user=req.user)
        except ObjectDoesNotExist as e:
            detail = UserDetail(user=req.user)
        try:
            detail.fullname = d.get('fullname', '')
            detail.number_exterior = d.get('num-ext', '')
            detail.number_interior = d.get('num-int', '')
            detail.street = d.get('street', '')
            detail.colony = d.get('colony', '')
            cp = d.get('cp', 0)
            detail.cp = 0 if not str(cp).isdigit() else int(cp)
            detail.city = d.get('city', '')
            detail.state = d.get('state', '')
            detail.country = d.get('country', '')
            detail.save()
            res['msg_type'] = 'success'
            res['msg_data'] = 'Éxito al guardar'
            res['detail'] = detail
        except Exception as e:
            res['msg_type'] = 'error'
            res['msg_data'] = 'Ocurrió un error al guardar la información'
        return render_to_response('user_info.html', res, RequestContext(req))

    try:
        res['detail'] = UserDetail.objects.get(user=req.user)
    except ObjectDoesNotExist as e:
        res['detail'] = None
    return render_to_response('user_info.html', res, RequestContext(req))