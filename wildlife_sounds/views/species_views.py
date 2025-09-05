from django.shortcuts import render
from wildlife_sounds.models import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404


# def fetch_get_scores(request):
    
#     if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
#         return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
#     query = json.loads(request.body)
#     query['user'] = request.user.username

#     score_dates, score_values, score_labels = get_scores(query = query)

#     return JsonResponse({'success' : True, 'score_dates' : score_dates, 'score_values' : score_values, 'score_labels' : score_labels})
    

def specie_detail(request, id):

    specie = get_object_or_404(Specie, pk=id)
    sounds = SpecieSound.objects.filter(specie=specie)
    
    url = "wildlife_sounds/species/specie_detail.html"

    context = {'specie' : specie,
               'sounds' : sounds}

    return render(request, url, context)


