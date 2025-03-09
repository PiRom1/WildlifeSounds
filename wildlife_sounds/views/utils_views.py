from django.shortcuts import render
from wildlife_sounds.models import *
from wildlife_sounds.forms import Listform
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
import json
import os
import random as rd
from django.contrib.staticfiles import finders

@login_required(login_url='login')
def home(request):

    path = finders.find('wildlife_sounds/birds_svg')

    print("path : ", path)

    birds_svg = os.listdir(path)
    print(birds_svg)
    path_birds_svg = ["static/wildlife_sounds/birds_svg/" + bird for bird in birds_svg]
    rd.shuffle(path_birds_svg)
    
    print(path_birds_svg)

    url = "wildlife_sounds/utils/home.html"

    context = {'path' : json.dumps(path_birds_svg),
               'user' : request.user}

    return render(request, url, context)


@login_required
def record_score(request):

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    data = json.loads(request.body)    
    score = data.get('score')
    pk = data.get('pk')
    liste = List.objects.get(id=pk)

    new_score = Score.objects.create(score = score,
                         user = request.user,
                         list = liste)
    
    if new_score:
        return JsonResponse({'success' : True})

    return JsonResponse({'success' : False})