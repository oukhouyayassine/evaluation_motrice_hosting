# utils.py
import random

# Listes de prénoms et noms marocains
prenoms = [
    "Yassine", "Omar", "Aya", "Sara", "Anas", "Hiba", "Imane", "Mehdi", 
    "Rania", "Hamza", "Fatima", "Mohamed", "Aicha", "Rachid", "Zineb",
    "Karim", "Laila", "Othmane", "Salma", "Abderrahim", "Khadija", "Younes"
]

noms = [
    "El Idrissi", "Benali", "Alaoui", "El Fassi", "El Amrani", "Touhami",
    "Benjelloun", "El Alami", "Berrada", "Cherkaoui", "El Ouafi", "Tazi"
]

def generer_nom_aleatoire():
    """Génère un nom complet aléatoirement"""
    return f"{random.choice(prenoms)} {random.choice(noms)}"

def generer_eleves(n: int = 40):
    """Génère une liste d'élèves avec des noms aléatoires"""
    eleves_generes = []
    noms_utilises = set()
    
    for i in range(n):
        # Éviter les doublons
        nom = generer_nom_aleatoire()
        while nom in noms_utilises:
            nom = generer_nom_aleatoire()
        noms_utilises.add(nom)
        
        eleves_generes.append({
            "nom": nom,
            "id": i + 1
        })
    
    return eleves_generes

# Function helper pour valider les données
def valider_donnees_eleve(eleve_data):
    """Valide les données d'un élève"""
    required_fields = [
        'souplesse_tronc', 'souplesse_epaule', 'equilibre_sec', 
        'saut_cm', 'lancer_cm', 'orientation', 'coord_desc'
    ]
    
    for field in required_fields:
        if field not in eleve_data:
            return False, f"Champ manquant: {field}"
    
    return True, "Données valides"

# Test de la fonction si le fichier est exécuté directement
if __name__ == "__main__":
    # Test de génération d'élèves
    eleves_test = generer_eleves(5)
    print("Test de génération d'élèves:")
    for eleve in eleves_test:
        print(f"- {eleve['nom']} (ID: {eleve['id']})")
