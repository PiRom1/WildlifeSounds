from django.urls import path

from .views import sound_views, login_views, load_data_views

urlpatterns = [
            # LOGIN
               path("deconnexion", login_views.deconnexion, name="deconnexion"),
               path("login", login_views.connexion, name="login"),
            
            # SOUNDS
               path("all", sound_views.all_sounds, name="list"),
               path("add_sound", sound_views.add_sound, name="add_sound"),
               path("add_sound_fetch", sound_views.add_sound_fetch, name="add_sound_fetch"),

               path("lists", sound_views.user_lists, name = "user_lists"),
               path("lists/<int:pk>", sound_views.detail_list, name = "user_lists"),
               path("list/add_specie_to_list", sound_views.add_sound_to_list, name = "add_sound_to_list"),
            
            # LOAD DATA
               path('load_data', load_data_views.load_data, name = 'load_data'),
               path('load_data_xeno_canto', load_data_views.load_data_xeno_canto, name = 'load_data_xenocanto'),


               ]