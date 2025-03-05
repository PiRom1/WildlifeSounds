from django.shortcuts import render
from wildlife_sounds.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
import json

# Create your views here.


# Utils

def get_available_species_name(liste): # Renvoie le nom des espèces non présentes dans la liste
    list_species = SpecieForList.objects.filter(list = liste)
    available_species = Specie.objects.exclude(vernacular_name__in=[specie.specie.vernacular_name for specie in list_species])
    available_names = list(available_species.values_list('vernacular_name', flat=True)) + list(available_species.values_list('scientific_name', flat=True))
    return available_names




@login_required
def all_sounds(request):

    url = "wildlife_sounds/sounds/all_sounds.html"

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


@login_required
def user_lists(request):

    lists = List.objects.filter(user = request.user)



    url = "wildlife_sounds/sounds/user_lists.html"

    context = {"lists" : lists}

    return render(request, url, context)


@login_required
def detail_list(request, pk = None):
    liste = List.objects.get(id=pk)
    list_species = SpecieForList.objects.filter(list = liste)
    
    list_species = [list_specie.specie for list_specie in list_species]

    available_names = get_available_species_name(liste)

    url = "wildlife_sounds/sounds/detail_list.html"

    context = {'pk' : pk,
               'liste' : liste,
               'list_species' : list_species,
               'available_species' : json.dumps(available_names)}

    return render(request, url, context)


@login_required
def add_sound_to_list(request):

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    data = json.loads(request.body)    
    print("data : ", data)
    

    specie = Specie.objects.filter(Q(vernacular_name=data.get('specie')) | Q(scientific_name=data.get('specie')))
    liste = List.objects.get(id=data.get('pk_list'))

    if len(specie) > 1:
        return JsonResponse({'success' : False, 'error': "Le nom de l'espèce sélectionnée est ambigüe."}, status=400)
    elif len(specie) == 0:
        return JsonResponse({'success' : False, 'error': "L'espèce sélectionnée n'a pas été trouvée."}, status=400)
    
    specie = specie.first()


    species_list = SpecieForList.objects.filter(list=liste)
    if specie in species_list:
        return JsonResponse({'success' : False, 'error': "L'espèce sélectionnée est déjà dans votre liste."}, status=400)
    
    # Ajouter l'espèce à la liste
    SpecieForList.objects.create(list = liste, specie = specie)

    available_names = get_available_species_name(liste)

    


    return JsonResponse({'success' : True,
                         'message': 'Succes',
                         'available_names' : json.dumps(available_names)},
                         status=200)


@login_required
def test_list(request, pk=None):

    liste = List.objects.get(id=pk)

    sounds = []

    species = SpecieForList.objects.filter(list=liste).order_by('?')

    for specie in species:
        specie_sounds = SpecieSound.objects.filter(specie = specie.specie)

        if specie_sounds:
            
            list_sounds = [specie_sound.sound.url for specie_sound in specie_sounds]
            sounds.append({'specie' : specie.specie.vernacular_name,
                           'sounds' : json.dumps(list_sounds)})

        


    url = "wildlife_sounds/sounds/test_list.html"

    context = {'pk' : pk,
               'liste' : liste,
               'species' : species,
               'sounds' : sounds}

    return render(request, url, context)