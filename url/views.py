from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views import View
from models import Url
from utils import parseURL,shortenURL
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect



class TinyView(View):

    def get(self, request, *args, **kwargs):
        actualUrl = kwargs.get('url')
        if actualUrl:
            shortURL = parseURL(actualUrl)
            urls = Url.objects.filter(shortURL=shortURL)
        else:
            urls = Url.objects.all()
        urlList = []
        for url in urls:
            urlList.append({
                "shortURL" : url.shortURL,
                "actualUrl" : url.actualUrl
            })
        return JsonResponse(urlList, safe=False)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        actualUrl = request.POST.get('url')
        created, shortURL = shortenURL(actualUrl)
        
        response = {
            "actualUrl":actualUrl,
            "shortURL":shortURL,
            "created" : created
        }
        return JsonResponse(response)
    
    def delete(self, request, *args, **kwargs):
        shortURL = kwargs.get('url')        
        try:
            objUrl = Url.objects.get(shortURL=shortURL)
            objUrl.delete()
            deleted = True
        except Url.DoesNotExist:        
            deleted = False
        
        response = {
            "deleted" : deleted
        }
        return JsonResponse(response)


def redirectURL(request, *args, **kwargs):
    shortURL = kwargs.get('shortURL')
    objURL = get_object_or_404(Url, shortURL=shortURL)
    if 'http' not in objURL.actualUrl:
        objURL.actualUrl = 'http://' + objURL.actualUrl
    return redirect(objURL.actualUrl)