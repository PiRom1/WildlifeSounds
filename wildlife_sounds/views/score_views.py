from django.shortcuts import render
from wildlife_sounds.models import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect


def get_scores(query = None):
    print(query)

    scores = Score.objects.filter(user__username = query['user']).order_by('date')
    
    if query.get('list_name'):
        scores = scores.filter(list__name = query['list_name'])
    
    if query.get('pourcentage'):
        score_values = [score.percent_score * 100 for score in scores]
    
    else:
        score_values = [score.score for score in scores]

    score_labels = [score.list.name for score in scores]

    score_dates = [f"{score.date.day}/{score.date.month}/{score.date.year} - {score.date.hour}h{score.date.minute}mn" for score in scores]
    

    return score_dates, score_values, score_labels

    


def fetch_get_scores(request):
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    query = json.loads(request.body)
    query['user'] = request.user.username

    score_dates, score_values, score_labels = get_scores(query = query)

    return JsonResponse({'success' : True, 'score_dates' : score_dates, 'score_values' : score_values, 'score_labels' : score_labels})
    




def scores(request):

    listes = list(List.objects.all().values_list('name', flat=True))

    url = "wildlife_sounds/scores/scores.html"

    context = {'listes' : json.dumps(listes)}

    return render(request, url, context)

