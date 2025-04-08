from wildlife_sounds.models import User, Score, List, SpecieForList
import random as rd
from datetime import datetime, timedelta

USER = User.objects.get(username='romain')

# Fonction pour générer une date aléatoire cette année
def random_date_this_year():
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    random_days = rd.randint(0, delta.days)
    random_seconds = rd.randint(0, 86400)
    return start_date + timedelta(days=random_days, seconds=random_seconds)



def run():
    scores = []
    for _ in range(500):
        liste = List.objects.all().order_by('?').first()
        nb_birds = SpecieForList.objects.filter(list = liste).count()
        max_score = nb_birds * 3
        nb_scientific = rd.randint(0, nb_birds)
        nb_vernacular = rd.randint(0, nb_birds - nb_scientific)
        nb_error = nb_birds - (nb_scientific + nb_vernacular)
        score = nb_vernacular + nb_scientific*3
        score = Score(score = score, 
                      max_score = max_score,
                      nb_vernacular = nb_vernacular,
                      nb_scientific = nb_scientific,
                      nb_error = nb_error,
                      user = USER, 
                      list = liste,
                      date = random_date_this_year())
        
        scores.append(score)
    
    Score.objects.bulk_create(scores)
        


