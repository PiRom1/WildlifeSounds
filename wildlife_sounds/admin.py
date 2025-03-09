from django.contrib import admin
from .models import Specie, SpecieSound, Order, Genus, Family, Taxon, User, List, SpecieForList, Score, UnknownSpecie


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_superuser")


@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = ("vernacular_name", "scientific_name", "order", "family", "genus", "taxon", "description")
    search_fields = ("vernacular_name", "scientific_name")
    list_filter = ("order", "family", "genus", "taxon")


@admin.register(SpecieSound)
class SpecieSoundAdmin(admin.ModelAdmin):
    list_display = ("specie", "type", "country", "sound")
    search_fields = ("specie__vernacular_name", "specie__scientific_name", "country")
    list_filter = ("type", "country")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_name", "description")
    search_fields = ("order_name",)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("family_name", "description")
    search_fields = ("family_name",)


@admin.register(Genus)
class GenusAdmin(admin.ModelAdmin):
    list_display = ("genus_name", "description")
    search_fields = ("genus_name",)


@admin.register(Taxon)
class TaxonAdmin(admin.ModelAdmin):
    list_display = ("taxon_name", "description")
    search_fields = ("taxon_name",)



@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "user")

@admin.register(SpecieForList)
class SpecieForListAdmin(admin.ModelAdmin):
    list_display = ("list", "specie")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("score", "user", "list", "date")


@admin.register(UnknownSpecie)
class UnknownSpecieAdmin(admin.ModelAdmin):
    list_display = ("scientific_name",)