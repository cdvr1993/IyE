__author__ = 'cristian'

import json

from django.contrib.auth import authenticate, login as login_user,\
    logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from django.db.models import ObjectDoesNotExist, Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


from IyE import settings
from IyE.models import Cart, CartDetail, Color, ColorKind, Product, ProductDetail, ProductKind, UserDetail
from IyE.utils import PostData, is_empty_elements_dict


def index(req):
    """ Returns the site's homepage
    """
    res = dict()
    # We obtain the new products, and present the newest
    prods = Product.objects.filter(new=True)
    res['products'] = prods[0:40]
    return render_to_response('index.html', res, RequestContext(req))


def login(req):
    """ It displays the login and registration forms
    We use another url to make the POST of the registration form
    """

    # To check if the user is trying to access it after he login
    if req.user.is_authenticated():
        return HttpResponseRedirect('/')
    res = dict()

    # When the user tries to login
    if req.method == 'POST':
        with PostData(req) as d:
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
                    # If the server has to redirect to another page
                    if 'next' in d:
                        return HttpResponseRedirect(d['next'])
                    return HttpResponseRedirect('/')
                else:
                    res['msg'] = 'Cuenta desactivada'

    return render_to_response('login.html', res, RequestContext(req))


def logout(req):
    """ It closes the user's session
    """
    if req.method == 'POST':
        try:
            logout_user(req)
            return redirect('/')
        except Exception as e:
            res = dict()
            res['msg_type'] = 'error'
            res['redirect'] = '/'
            return render_to_response('msg.html', res, RequestContext(req))
    raise Http404


def register(req):
    """ Handler of the POSTs emitted by the registration form
    """
    res = dict()
    if req.method == 'POST':
        with PostData(req) as d:
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
    """ It displays the contact form
    """
    if req.method == 'GET':
        return render_to_response('contact.html', RequestContext(req))
    else:
        with PostData(req) as d:
            error = is_empty_elements_dict(d, 'name', 'email', 'email_msg')
            res = dict()
            if error is not None:
                res['msg'], res['msg_type'] = (error, 'error')
                res.update(d)
            else:
                try:
                    send_mail('Contacto Maui Geek',
                              'From: {0}\n{1}'.format(d['email'],
                                                      d['email_msg']),
                              settings.EMAIL_HOST_USER,
                              [settings.EMAIL_HOST_USER])
                    res['msg'], res['msg_type'] = ('Éxito enviando el mensaje',
                                                   'success')
                except Exception as e:
                    res['msg'], res['msg_type'] = (
                        'Ocurrió un error durante el envío', 'error')
                    res.update(d)

            return render_to_response('contact.html', res, RequestContext(req))


def about(req):
    """ It displays information about us
    TODO:
        Maybe will be a good idea to check the actual content of this section
    """
    return render_to_response('about.html', RequestContext(req))


def _delete_from_cart(user, key):
    try:
        detail = Cart.objects.get(user=user).details.get(id=key)
        detail.delete()
        return {
            'id': key,
            'info': 'Éxito al eliminar el producto',
            'type': 'success'
        }
    except Exception as e:
        print(e)
        return {
            'id': key,
            'info': 'Ocurrió un error al tratar de eliminar el producto',
            'type': 'error'
        }


def _update_qty_in_cart(user, key, qty):
    try:
        detail = Cart.objects.get(user=user).details.get(id=key)
        detail.qty = qty
        detail.save()
        return {
            'id': key,
            'info': 'Éxito al actualizar la cantidad',
            'type': 'success'
        }
    except Exception as e:
        return {
            'id': key,
            'info': 'No se puede actualizar la cantidad',
            'type': 'error'
        }


def _update_cart(req):
    with PostData(req) as d:
        json_res = list()
        data = json.loads(d.get('data', '{}'))
        print(data)
        if len(data) == 0:
            json_res.append({
                'info': 'No hay información para actualizar',
                'type': 'error'})
        else:
            for key, val in data.items():
                if val.get('delete', False):
                    json_res.append(_delete_from_cart(req.user, key))
                elif 'qty' in val:
                    json_res.append(_update_qty_in_cart(req.user, key, val['qty']))
        return HttpResponse(json.dumps(json_res),
                            content_type='application/json')


@login_required
def cart_show(req):
    """ Currently doesn't work, it only presents the HTML
    """
    res = {'IVA': settings.IVA}
    try:
        res['total'] = 0.0
        res['cart'] = Cart.objects.get(user=req.user)
        for detail in res['cart'].details.all():
            res['total'] += detail.kind.price * detail.qty
    except Exception as e:
        res['msg'], res['msg_type'] = ('No hay productos en el carro', 'error')
    if req.method == 'POST':
        return _update_cart(req)
    return render_to_response('cart.html', res, RequestContext(req))


@login_required
def checkout(req):
    if req.method == 'POST' and req.is_ajax():
        item_body = (
'''
User ID: {0}
Username: {1}
Product ID: {2}
Product name: {3}
Kind: {4}
Color: {5}
Quantity: {6}
Gender: {7}
''')
        try:
            cart = Cart.objects.get(user=req.user)
            body_list = [item_body.format(req.user.id, req.user.username,
                                          d.product.id, d.product.name,
                                          d.kind.name, d.color.name,
                                          d.qty, d.gender)
                         for d in cart.details.all()]
            send_mail('Contacto Maui Geek', '\n\n'.join(body_list),
                      settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            cart.delete()
            return HttpResponse('True')
        except Exception as e:
            print(e)
            return HttpResponse('Error levantando el pedido')
    raise Http404


@login_required
def user_info(req):
    """ It displays and updates the user's info
    This info will be used to send the products
    """
    res = dict()
    if req.method == 'POST':
        with PostData(req) as d:
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
            return render_to_response('user_info.html', res,
                                      RequestContext(req))

    try:
        res['detail'] = UserDetail.objects.get(user=req.user)
    except ObjectDoesNotExist as e:
        res['detail'] = None
    return render_to_response('user_info.html', res, RequestContext(req))


def _check_if_exist_in_cart(d, res, cart):
    gender = 'u' if ProductKind.objects.get(id=d['kind']).unisex else d['gender'][0]
    if len(CartDetail.objects.filter(product_id=d['product-id'], color_id=d['color'], gender=gender, kind_id=d['kind'])) > 0:
        res['msg'] = 'Ese producto ya esta en su cesta'
        return False

    detail = CartDetail(product_id=d['product-id'], qty=d['qty'], color_id=d['color'], gender=gender, kind_id=d['kind'])
    detail.save()
    # Finally we append the product to the cart
    cart.details.add(detail)
    return True


def _cart_add(req):
    """ It tries to add the product to the user cart
    """
    with PostData(req) as d:
        res = {'msg': 'Ocurrio un error al añadir el producto',
               'msg_type': 'error'}

        try:
            # If the user already has a cart
            cart = Cart.objects.get(user=req.user)
        except ObjectDoesNotExist:
            try:
                # If the user doesn't have a cart yet
                cart = Cart(user=req.user)
            except Exception:
                res['msg'] = 'No se pudo crear un nueva cesta'
                return res
        except Exception as e:
            res['msg'] = 'No se pudo obtener su cesta'
            return res

        try:
            # First we need to save the cart, if not it raises an Exception
            cart.save()
            if not _check_if_exist_in_cart(d, res, cart):
                return res
        except Exception as e:
            print(e)
            res['msg'] = 'No se pudo añadir el producto a su cesta'
            return res

        return {'msg': 'Producto añadido con éxito',
                'msg_type': 'success'}


def get_colors(req):
    if req.method == 'GET' and req.is_ajax():
        gender = req.GET.get('gender', '')
        kind = req.GET.get('kind', '')
        if kind != '':
            try:
                if ProductKind.objects.get(id=kind).unisex:
                    query_kind = Q(kind_id=kind)
                elif gender == 'male' or gender == 'female':
                    query_kind = Q(kind_id=kind) & Q(gender=gender[0])
                result = ColorKind.objects.filter(query_kind)
                ids = [Q(id=item.color_id) for item in result]
                query = ids.pop()
                for item in ids:
                    query |= item
                colors = Color.objects.filter(query)
                return HttpResponse(serializers.serialize('json', colors), content_type='application/json')
            except ObjectDoesNotExist:
                pass
            except Exception as e:
                print(e.args)
    raise Http404


def product_detail(req):
    """ It displays the detailed information of a product
    """
    res = dict()
    if req.method == 'POST':
        if not req.user.is_authenticated():
            raise Http404
        res.update(_cart_add(req))
    prod_id = req.GET.get('product', None)
    if prod_id is None:
        return alert_error('Debe especificar el producto')
    try:
        res['product'] = Product.objects.get(id=prod_id)
        res['kinds'] = ProductKind.objects.all()
        try:
            res['product_d'] = ProductDetail.objects.\
                get(id=res['product'].id)
        except ObjectDoesNotExist as e:
            pass
        return render_to_response('product_detail.html',
                                  res,
                                  RequestContext(req))
    except ObjectDoesNotExist as e:
        return alert_error('No existe el producto')


def alert_error(msg, redirect_to='/'):
    """ It displays a page that only shows an error message
    """
    res = dict()
    res['msg'] = msg
    res['msg_type'] = 'error'
    res['redirect'] = redirect_to
    return render_to_response('msg.html', res)