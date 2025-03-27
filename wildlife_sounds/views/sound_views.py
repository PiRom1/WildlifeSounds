from django.shortcuts import render
from wildlife_sounds.models import *
from wildlife_sounds.forms import Listform
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
import json
from wildlife_sounds.utils.get_data import load_data_specific_bird_xenocanto


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

    sounds = SpecieSound.objects.all()[0:50]

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
def add_specie_to_list(request):

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

    print("chargement des sons ... ")
    # load_data_specific_bird_xenocanto(specie.scientific_name)
    
    return JsonResponse({'success' : True,
                         'message': 'Succes',
                         'available_names' : json.dumps(available_names),
                         'specie_id' : specie.id},
                         status=200)



@login_required
def remove_specie_from_list(request):

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    data = json.loads(request.body)    
    print("data : ", data)

    id_list = data.get('pk_list')
    id_bird = data.get('bird_id')

    if not id_list:
        return JsonResponse({'success' : False, 'error' : 'ID list is not in data'})

    if not id_bird:
        return JsonResponse({'success' : False, 'error' : 'ID bird is not in data'})
    
    liste = List.objects.get(pk=id_list)
    specie = Specie.objects.get(pk=id_bird)

    SpecieForList.objects.filter(list_id = id_list, specie_id = id_bird).delete()


    return JsonResponse({'success' : True})
    


@login_required
def train_list(request, pk=None):

    liste = List.objects.get(id=pk)

    sounds = []

    species = SpecieForList.objects.filter(list=liste).order_by('?')

    for specie in species:
        specie_sounds = SpecieSound.objects.filter(specie = specie.specie)
        
        if specie_sounds:
            
            list_sounds = [specie_sound.sound.url for specie_sound in specie_sounds]
            sounds.append({'specie' : specie.specie.vernacular_name,
                           'sounds' : json.dumps(list_sounds)})


    url = "wildlife_sounds/sounds/train_list.html"

    context = {'pk' : pk,
               'liste' : liste,
               'sounds' : sounds,
               'nb_species' : len(sounds)}

    return render(request, url, context)



@login_required
def test_list(request, pk=None):

    liste = List.objects.get(id=pk)

    sounds = []

    species = SpecieForList.objects.filter(list=liste).order_by('?')

    for specie in species:
        specie_sounds = SpecieSound.objects.filter(specie = specie.specie)
        
        if specie_sounds:
            
            list_sounds = [specie_sound.sound.url for specie_sound in specie_sounds]
            sounds.append({'vernacular_specie' : specie.specie.vernacular_name, 
                           'scientific_specie' : specie.specie.scientific_name,
                           'sounds' : json.dumps(list_sounds)})
        print([sound['vernacular_specie'] for sound in sounds])


    url = "wildlife_sounds/sounds/test_list.html"

    context = {'pk' : pk,
               'liste' : liste,
               'sounds' : sounds,
               'nb_species' : len(sounds)}

    return render(request, url, context)



@login_required
def create_list(request):
    print(request.POST)
    if request.method == 'GET': # Affichage
        list_form = Listform()

    elif request.method == 'POST':
        list_form = Listform(request.POST)
        form = list_form.save(commit=False)
        form.user = request.user
        form.save()
        return HttpResponseRedirect(f'/lists/{form.id}')


    url = "wildlife_sounds/sounds/create_list.html"

    context = {'form' : list_form}

    return render(request, url, context)


@login_required
def train(request):

    
    url = "wildlife_sounds/sounds/train_or_test.html"

    context = {'lists' : List.objects.filter(user=request.user),
               'method' : 'train'}

    return render(request, url, context)



@login_required
def test(request):

    
    url = "wildlife_sounds/sounds/train_or_test.html"

    context = {'lists' : List.objects.filter(user=request.user),
               'method' : 'test'}

    return render(request, url, context)




@login_required
def delete_list(request):

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    data = json.loads(request.body)    
    
    
    pk = data.get('pk_list')

    if not pk:
        return JsonResponse({'success' : False, 'error' : "L'id de la liste n'est pas fourni."})

    delete_list = List.objects.get(pk = pk)
    name_list = delete_list.name
    delete_list.delete()

    return JsonResponse({'success' : True, 'name_list' : name_list})