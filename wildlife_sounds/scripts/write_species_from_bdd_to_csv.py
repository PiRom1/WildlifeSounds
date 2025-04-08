from wildlife_sounds.models import Specie
import csv

# Write every species from databse to a csv file stored in /data
# This scripts aims to be used once the database is clean (names changed, description, add more species, ... )
# Thus it can be cleanly exported on another machine with the script 'write_species_from_csv_to_ddb.py'

PATH_TO_CSV = "data/species.csv"

def run():

    with open(PATH_TO_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        first_row = ["vernacular_name", "scientific_name", "description", "family", "genus", "order", "taxon"]
        writer.writerow(first_row)

        for specie in Specie.objects.all():
            row = [specie.vernacular_name, specie.scientific_name, specie.description, specie.family, specie.genus, specie.order, specie.taxon]
            writer.writerow(row)
        
            
