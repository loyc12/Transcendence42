# AUTH0_ALEX
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings

from django.shortcuts import render, redirect, HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from core.settings import ENV_FILE
from urllib.parse import urlencode, urlunsplit, quote_plus
import requests

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=ENV_FILE['APP42_UID'],
    client_secret=ENV_FILE['APP42_SECRET'],
    server_metadata_url=f"https://{settings.APP42_DOMAIN}/oauth/authorize",
)

def oauth42_index(request):
    return render(
        request, "Index/index.html",
        context={"session": request.session.get("user"),
                 "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
    
def oauth42_callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index"))
    )

def oauth42_login(request):
    return oauth.auth0.authorize_redirect(
        request,
        redirect_uri=request.build_absolute_uri(reverse("callback"))
    )
    
def oauth42_logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.APP42_DOMAIN}/v2/logout?"
        + urlencode({
            "returnTo": request.build_absolute_uri(reverse("index")),
            "client_id": settings.APP42_UID,
        },
        quote_via=quote_plus,
      ),
    )

# def oauth42(req):
#     print(req)
#     base_url = "https://api.intra.42.fr/oauth/authorize"
#     params = {
#         "client_id": ENV_FILE['APP42_UID'],
#         "request_uri": ENV_FILE['APP42_OAUTH_REDIRECT']
#     }

#     full_url = urlunsplit(('https', 'api.intra.42.fr', '/oauth/authorize', urlencode(params), None))
#     print("base_url : ", base_url)
#     print("params : ", params)
#     print('full_url : ', full_url)

#     return (HttpResponsePermanentRedirect(requests.build_absolute_uri(full_url)))
    # resp = requests.get(base_url, params=params)
    # print("resp : ", resp)
    # print("resp.text : ", resp.text)
    # return (HttpResponse(resp.text))
    # )
    #return (HttpResponse("oauth endpoint reached."))


# def oauth42_receive_code(req):
#     print("oauth42 token stage reached")
#     print(req)
#     print("request body : ", req.body)
#     code = req.body.decode('utf8')
#     print("received code : ", code)

#     base_url = "https://api.intra.42.fr/oauth/token"
#     params = {
#         "grant_type": "authorization_code",
#         "client_id": ENV_FILE['APP42_UID'],
#         "client_secret": ENV_FILE['APP42_SECRET'],
#         "request_uri": ENV_FILE['APP42_OAUTH_CONFIRM'],
#         "code": code
#     }

# #    uri = "https://api.intra.42.fr/oauth/token"\
# #         + "?"\
# #         + "grant_type=authorization_code"\
# #         + f"client_id={ENV_FILE['APP42_UID']}"\
# #         + f"client_secret={ENV_FILE['APP42_SECRET']}"\
# #         + f"redirect_uri={ENV_FILE['APP42_OAUTH_CONFIRM']}"\
# #         + f"code={code}"
#     print(uri)
#     resp = requests.get(base_url, params=params)
#     print("resp : ", resp)
#     print("resp.text : ", resp.text)
#     return (HttpResponse(resp.text))
#     #return (HttpResponse("oauth endpoint reached."))


# def oauth42_confirm_user(req):
#     print("oauth42 confirm stage reached")
#     print(req)
#     print(req.text)
#     return (HttpResponse("oauth : User successfully authenticated."))
