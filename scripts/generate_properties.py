import os
import sys
import django
import random
from faker import Faker
from django.core.files import File
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

# Configurez Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_backend.settings')
django.setup()

from properties.models import Property

def generate_properties(num_properties=20):
    fake = Faker(['fr_FR'])  # Utiliser le locale français
    
    # Données plus réalistes pour le Bénin
    cities = ['Cotonou', 'Porto-Novo', 'Abomey-Calavi', 'Parakou', 'Djougou', 
              'Bohicon', 'Natitingou', 'Ouidah', 'Sakété', 'Lokossa']
    
    property_types = ['house', 'apartment', 'land']
    
    # Chemin vers le dossier des images de test
    image_dir = Path(__file__).resolve().parent / 'test_images'
    test_images = list(image_dir.glob('*.jpg'))  # Assurez-vous d'avoir des images test

    for i in range(num_properties):
        title = f"Belle {fake.word()} à {random.choice(cities)}"
        description = fake.text(max_nb_chars=500)
        property_type = random.choice(property_types)
        
        # Prix plus réalistes pour le Bénin (en FCFA)
        if property_type == 'house':
            price = random.randint(25000000, 150000000)
        elif property_type == 'apartment':
            price = random.randint(15000000, 50000000)
        else:  # land
            price = random.randint(5000000, 30000000)

        location = random.choice(cities)
        
        # Caractéristiques selon le type de bien
        if property_type != 'land':
            bedrooms = random.randint(1, 5)
            bathrooms = random.randint(1, 3)
            area = round(random.uniform(50.0, 300.0), 2)
        else:
            bedrooms = 0
            bathrooms = 0
            area = round(random.uniform(200.0, 1000.0), 2)

        # Création de la propriété
        property = Property.objects.create(
            title=title,
            description=description,
            property_type=property_type,
            price=price,
            location=location,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area
        )

        # Ajout d'une image si disponible
        if test_images:
            with open(random.choice(test_images), 'rb') as img_file:
                property.image.save(
                    f'property_{i}.jpg',
                    File(img_file),
                    save=True
                )

        print(f"Créé: {property.title}")

if __name__ == '__main__':
    print("Génération des propriétés de test...")
    Property.objects.all().delete()  # Attention: supprime toutes les propriétés existantes
    generate_properties()
    print("Terminé!")