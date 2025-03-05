import requests
from wildlife_sounds.models import Taxon, Order, Genus, Family, Specie, SpecieSound
from django.http import HttpResponse
from django.core.files.base import ContentFile

def load_data_from_xeno_canto():

    API_URL = "https://www.xeno-canto.org/api/2/recordings"
    QUERY = "grp:birds cnt:france"



    # Get n_pages
    r = requests.get(API_URL, params={'query': QUERY})

    if r.status_code == 200:
        json = r.json()
        n_pages = json.get('numPages')

    else:
        return 'Error'


    not_working_species = []
    for n_page in range(n_pages):
        page = n_page + 1
        print(f'requête n°{page}')
        r = requests.get(API_URL, params={'query': QUERY, 'page' : page})
        json = r.json()

        for i,record in enumerate(json.get('recordings')):
            if record.get('type') == 'song':


                name = f"{record.get('gen')} {record.get('sp')}"
                type = record.get('type')
                if name in not_working_species:
                    continue

                if not Specie.objects.filter(scientific_name__icontains=name):
                    print(f"L'espèce {name} n'était pas présente en base de données. \n Ajout en cours ...")

                    specie_data = get_data_from_name(name)

                    if not specie_data: # If no result
                        print("Pas d'informations trouvées sur l'espèce ...")
                        not_working_species.append(name)
                        continue

                    print("data : ", specie_data)

                    order = specie_data.get('order_name')
                    family = specie_data.get('family_name')
                    genus = specie_data.get('genus_name')

                    if order: # If order is returned by the bird API

                        # If order is not present in database
                        if not Order.objects.filter(order_name__icontains=specie_data.get('order_name')):
                                print(f"L'ordre {specie_data.get('order_name')} n'était pas présent en base de données. \n Ajout en cours ...")
                                order = Order.objects.create(order_name = specie_data.get('order_name'))
                        else:
                             order = Order.objects.get(order_name = order)
                    
                    else: # If order is not returned by the bird API
                         order, created =  Order.objects.get_or_create(order_name = 'Unknown')
                    
                    order = specie_data.get('order_name')

                    if family: # If family is returned by the bird API

                        # If family is not present in database
                        if not Family.objects.filter(family_name=specie_data.get('family_name')):
                            print(f"La famille {specie_data.get('family_name')} n'était pas présente en base de données. \n Ajout en cours ...")
                            family = Family.objects.create(family_name = specie_data.get('family_name'))
                        else:
                            family = Family.objects.get(family_name = family)

                    else: # If family is not returned by the bird API
                        family, created = Family.objects.get_or_create(family_name = 'Unknown')

                    if genus: # If genus is returned by the bird API
                        # If genus is not present in database
                        if not Genus.objects.filter(genus_name__icontains=specie_data.get('genus_name')):
                            print(f"Le genre {specie_data.get('genus_name')} n'était pas présent en base de données. \n Ajout en cours ...")
                            genus = Genus.objects.create(genus_name = specie_data.get('genus_name'))
                        else:
                            genus = Genus.objects.get(genus_name = genus)

                    else: # If genus is not returned by the bird API
                        genus, created = Genus.objects.get_or_create(genus_name = 'Unknown')

                    taxon = Taxon.objects.get(taxon_name = 'Oiseau')
                    specie = Specie.objects.create(vernacular_name = specie_data.get('vernacular_name'),
                                          scientific_name = name,
                                          order = order,
                                          family = family,
                                          genus = genus,
                                          taxon = taxon)
                    
                    print(f"L'espèce a bien été ajoutée !")
                else:
                    specie = Specie.objects.get(scientific_name = name)
                

                if not SpecieSound.objects.filter(id__icontains=record.get('id')):

                    # Add sound to database
                    sound = requests.get(record.get('file'))

                    SpecieSound.objects.create(id = record.get('id'),
                                               sound = ContentFile(sound.content, name=name),
                                               specie = specie,
                                               type = 'song',
                                               country = 'France')
                    
                    print("Son ajouté !")
                    
                
                





def get_data_from_name(name):
    TAXREF_URL = f"https://taxref.mnhn.fr/api/taxa/fuzzyMatch?term={'%20'.join(name.split(' '))}"    
    r = requests.get(TAXREF_URL)
    json = r.json()

    if '_embedded' not in json: # If no result
        return None

    data = json.get('_embedded')['taxa'][0]

    res = {'vernacular_name' : data['frenchVernacularName'],
        'order_name' : data['vernacularOrderName'],
        'genus_name' : data['genusName'],
        'family_name' : data['familyName'],
    }

    return res