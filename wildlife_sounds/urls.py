from django.urls import path

from .views import sound_views, login_views

urlpatterns = [
            # LOGIN
               path("deconnexion", login_views.deconnexion, name="deconnexion"),
               path("login", login_views.connexion, name="login"),
            
            # SOUNDS
               path("list", sound_views.list_sounds, name="list"),
               path("add_sound", sound_views.add_sound, name="add_sound"),
               path("add_sound_fetch", sound_views.add_sound_fetch, name="add_sound_fetch"),


               ]