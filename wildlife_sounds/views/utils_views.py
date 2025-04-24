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
from django.contrib.auth import logout

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
    print("data : ", data)
    score = data.get('score')
    nb_species = int(data.get('nb_species'))
    nb_vernacular = data.get('nb_vernacular')
    nb_scientific = data.get('nb_scientific')
    nb_error = data.get('nb_error')
    pk = data.get('pk')

    liste = List.objects.get(id=pk)

    new_score = Score.objects.create(score = score,
                                     max_score = nb_species * 3,
                                     nb_vernacular = nb_vernacular,
                                     nb_scientific = nb_scientific,
                                     nb_error = nb_error,
                                     user = request.user,
                                     list = liste)
    
    if new_score:
        return JsonResponse({'success' : True})

    return JsonResponse({'success' : False})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login")
