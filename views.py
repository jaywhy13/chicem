from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
    return HttpResponse("Chicem v1")


def map(request):
	return render_to_response('map/ChineseCemetery.html', locals())
