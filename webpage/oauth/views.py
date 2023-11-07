from django.shortcuts import render, redirect, HttpResponse, HttpResponsePermanentRedirect
from core.settings import env
from urllib.parse import urlencode, urlunsplit
#import requests

# Create your views here.

def oauth42(req):
    print(req)
    base_url = "https://api.intra.42.fr/oauth/authorize"
    params = {
        "client_id": env['APP42_UID'],
        "request_uri": env['APP42_OAUTH_REDIRECT']
    }

    full_url = urlunsplit(('https', 'api.intra.42.fr', '/oauth/authorize', urlencode(params), None))
    print("base_url : ", base_url)
    print("params : ", params)
    print('full_url : ', full_url)

    return (HttpResponsePermanentRedirect())#redirect(base_url, ))
    resp = requests.get(base_url, params=params)
    print("resp : ", resp)
    print("resp.text : ", resp.text)
    return (HttpResponse(resp.text))
    #return (HttpResponse("oauth endpoint reached."))


def oauth42_receive_code(req):
    print("oauth42 token stage reached")
    print(req)
    print("request body : ", req.body)
    code = req.body.decode('utf8')
    print("received code : ", code)

    base_url = "https://api.intra.42.fr/oauth/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": env['APP42_UID'],
        "client_secret": env['APP42_SECRET'],
        "request_uri": env['APP42_OAUTH_CONFIRM'],
        "code": code
    }

#    uri = "https://api.intra.42.fr/oauth/token"\
#         + "?"\
#         + "grant_type=authorization_code"\
#         + f"client_id={env['APP42_UID']}"\
#         + f"client_secret={env['APP42_SECRET']}"\
#         + f"redirect_uri={env['APP42_OAUTH_CONFIRM']}"\
#         + f"code={code}"
    print(uri)
    resp = requests.get(base_url, params=params)
    print("resp : ", resp)
    print("resp.text : ", resp.text)
    return (HttpResponse(resp.text))
    #return (HttpResponse("oauth endpoint reached."))


def oauth42_confirm_user(req):
    print("oauth42 confirm stage reached")
    print(req)
    print(req.text)
    return (HttpResponse("oauth : User successfully authenticated."))
