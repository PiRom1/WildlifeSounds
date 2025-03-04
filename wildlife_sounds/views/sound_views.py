from django.shortcuts import render
from wildlife_sounds.models import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect


# Create your views here.



@login_required
def list_sounds(request):

    url = "wildlife_sounds/sounds/list_sounds.html"

    sounds = SpecieSound.objects.all()

    context = {"sounds" : sounds}
    return render(request, url, context)


@login_required
def add_sound(request):
    url = "wildlife_sounds/sounds/add_sound.html"

    species = Specie.objects.all()
    scientific_names = list(species.values_list('scientific_name', flat = True))
    vernacular_names = list(species.values_list('vernacular_name', flat = True))
    all_names = list(set(scientific_names + vernacular_names))

    context = {'all_names' : json.dumps(all_names)}

    return render(request, url, context)


def add_sound_fetch(request):
    print('ici')
    # if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
    #     return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    print("data : ", request.POST)

    name = request.POST.get('name')
    type = request.POST.get('type')
    country = request.POST.get('country')
    sound_file = request.FILES.get('sound')  # Récupérer le fichier de l'input 'sound'

    if not name:
        return JsonResponse({'success' : False, 'error' :"Renseignez le nom de l'espèce"})
    
    if not sound_file:
        return JsonResponse({'success' : False, 'error': 'Aucun fichier reçu'}, status=400)
    
    specie = Specie.objects.filter(vernacular_name=name)
    if not specie:
        specie = Specie.objects.filter(scientific_name=name)
        if not specie:
            return JsonResponse({'success' : False, 'error' :"Cette espèce n'existe pas"})
    


    print("son : ", request.FILES)


    SpecieSound.objects.create(sound = sound_file,
                               specie = specie.first(),
                               type = type,
                               country = country)


    return JsonResponse({'success' : True})
