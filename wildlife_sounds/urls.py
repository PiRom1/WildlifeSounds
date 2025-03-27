from django.urls import path

from .views import sound_views, login_views, load_data_views, utils_views

urlpatterns = [
            # LOGIN
               path("deconnexion", login_views.deconnexion, name="deconnexion"),
               path("login", login_views.connexion, name="login"),

            # UTILS
               path("", utils_views.home, name="home"),
               path("record_score", utils_views.record_score, name="record_score"),
            
            # SOUNDS
               path("all", sound_views.all_sounds, name="list"),
               path("add_sound", sound_views.add_sound, name="add_sound"),
               path("add_sound_fetch", sound_views.add_sound_fetch, name="add_sound_fetch"),

               path("lists", sound_views.user_lists, name = "user_lists"),
               path("lists/<int:pk>", sound_views.detail_list, name = "user_lists"),
               path("lists/<int:pk>/train", sound_views.train_list, name = "train_list"),
               path("lists/<int:pk>/test", sound_views.test_list, name = "test_list"),
               path("list/add_specie_to_list", sound_views.add_specie_to_list, name = "add_specie_to_list"),
               path("list/remove_specie_from_list", sound_views.remove_specie_from_list, name = "remove_specie_from_list"),

               path("create_list", sound_views.create_list, name = "create_list"),
               path("delete_list", sound_views.delete_list, name = "delete_list"),
               path("train", sound_views.train, name="train"),
               path("test", sound_views.test, name="test"),

            # LOAD DATA
               path('load_data', load_data_views.load_data, name = 'load_data'),
               path('load_data_xeno_canto', load_data_views.load_data_xeno_canto, name = 'load_data_xenocanto'),
               path('load_data/<str:name>', load_data_views.load_bird, name = 'load_bird')

               ]