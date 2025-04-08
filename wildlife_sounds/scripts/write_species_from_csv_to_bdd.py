from wildlife_sounds.models import Specie, Family, Genus, Order, Taxon
import pandas as pd

PATH_TO_CSV = "data/species.csv"

def run():

    csv = pd.read_csv(PATH_TO_CSV, sep=";")

    for i,row in csv.iterrows():
        
        taxon = row["taxon"]
        order = row["order"]
        genus = row["genus"]
        family = row["family"]
        
        if taxon:
            taxon, created = Taxon.objects.get_or_create(taxon_name = row['taxon'])
        if order:
            order, created = Order.objects.get_or_create(order_name = row['order'])
        if genus:
            genus, created = Genus.objects.get_or_create(genus_name = row['genus'])
        if family:
            family, created = Family.objects.get_or_create(family_name = row['family'])

        specie, created = Specie.objects.get_or_create(vernacular_name = row["vernacular_name"])

        specie.scientific_name = row["scientific_name"]
        specie.description = row["description"]
        specie.family = family
        specie.genus = genus
        specie.order = order
        specie.taxon = taxon

        specie.save()
        