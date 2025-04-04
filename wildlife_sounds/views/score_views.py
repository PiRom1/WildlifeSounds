from django.shortcuts import render
from wildlife_sounds.models import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect

def all_scores(request):

    scores = Score.objects.filter(user=request.user)

    url = "wildlife_sounds/score/all_scores.html"

    context = {'scores' : scores}

    return render(request, url, context)

