from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import ApiKey, Price
from coinmena.settings import API_KEY
import requests
import secrets
import string
from django.contrib.auth.hashers import make_password as hash_key
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def GenerateApiKey(request):
    apikey = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(15))
    ApiKey.objects.create(hashed_key = HashApiKey(apikey))
    return JsonResponse({'apikey' : apikey})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def Quotes(request):
    if request.method == 'GET':
        apiKey = request.GET.get('apikey', None)
    elif request.method == 'POST':
        apiKey = request.POST.get('apikey', None)
    if(HandleAuth(apiKey)):
        if request.method == 'GET':
            res = Price.objects.filter()
            if(res):
                return JsonResponse({"price" : res.latest('created').value})
            else:
                return HttpResponse("Exchange Price Not Avaiable At The Moment")
        elif request.method == 'POST':
            price = FetchPrice()
            if price:
                return JsonResponse({"price" : price})
            else:
                return HttpResponse("Service Unavailable: alphavantage was unable to process the request, please try again later")
    else:
        return HttpResponse("Authentication Faliure: Kindly include a valid api key or generate a new one")

def HandleAuth(obtainedKey):
    if(not obtainedKey):
        return False
    exists = ApiKey.objects.filter(hashed_key = HashApiKey(obtainedKey), invalid = False).exists()
    return exists

def FetchPrice():
    url = 'https://www.alphavantage.co/query?function=%s&from_currency=%s&to_currency=%s&apikey=%s' % ('CURRENCY_EXCHANGE_RATE', 'BTC', "USD", "API_KEY")
    request = requests.get(url)
    data = request.json()
    if "Realtime Currency Exchange Rate" in data.keys():
        currVal = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        Price.objects.create(pair = "BTC/USD", value = currVal)
        return currVal
    else:
        return False

def HashApiKey(apiKey):
    enc = hashlib.sha256()
    enc.update(apiKey.encode('utf-8'))
    return str(enc.digest())