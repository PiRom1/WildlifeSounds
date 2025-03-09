from wildlife_sounds.utils.get_data import load_data_from_xeno_canto, load_data_specific_bird_xenocanto
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

@login_required
def load_data(request):

    # load_data_from_xeno_canto()

    context = {}
    url = "wildlife_sounds/load_data/load_data.html"
    return(render(request, url, context))


def load_data_xeno_canto(request):

    load_data_from_xeno_canto()

    return JsonResponse({'success' : True})



def load_bird(request, name = None):
    print(name)
    load_data_specific_bird_xenocanto(name)

    
    context = {}
    url = "wildlife_sounds/load_data/load_data.html"
    return(render(request, url, context))