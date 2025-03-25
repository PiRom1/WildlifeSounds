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
puis initialisez la base de données : 
```bash 
python manage.py migrate
```

- Enfin, lancez l'application avec la commande suivante : 
```bash
python manage.py runserver
```