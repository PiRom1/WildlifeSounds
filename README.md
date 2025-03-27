<h1>Wildlife Sounds</h1>
<h2>Une application pour s'entraîner à reconnaître les sons des animaux, basée sur les données de XenoCanto</h2>

- Cloner le dépôt avec :
```bash
git clone https://github.com/PiRom1/WildlifeSounds.git
```

- Créez un environnement virtuel, sourcez le et installez les librairies nécessaires avec :
```bash
python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
```

- Lors du premier lancement, créez un superadmin : 
```bash
python manage.py createsuperuser
```
Puis initialisez la base de données : 
```bash 
python manage.py migrate
```

- Enfin, lancez l'application avec la commande suivante : 
```bash
python manage.py runserver
```

_______________________________________
_______________________________________


- Pour enregistrer toutes les espèces en base de données, lancez la commande suivante
```bash
python manage.py runscript load_all_species
```
(à ce stade, vous n'aurez encore aucun son, les espèces seront seulement sauvegardées en base de données)



Prochain stade : 
Soit tout télécharger de xenocanto (avec limite à n sons par espèce) soit télécharger quand des espèces sont dans une liste.
+ chaque jour récupérer les sons de la veille et ajouter si les espèces sont dans la liste en supprimant n sons à la place. 