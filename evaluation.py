# evaluation.py
"""
Module d'évaluation des capacités motrices des élèves
"""

def evaluer_souplesse_tronc(val: str) -> int:
    """Évalue la souplesse du tronc selon l'échelle 1-5"""
    scores = {"5": 5, "4": 4, "3": 3, "2": 2, "1": 1}
    return scores.get(str(val), 0)

def evaluer_souplesse_epaule(val: str) -> int:
    """Évalue la souplesse de l'épaule selon l'échelle 1-5"""
    scores = {"5": 5, "4": 4, "3": 3, "2": 2, "1": 1}
    return scores.get(str(val), 0)

def evaluer_equilibre(val: int) -> int:
    """Évalue l'équilibre selon le temps en secondes"""
    if val >= 30:
        return 3
    elif val >= 25:
        return 2
    elif val >= 20:
        return 1
    return 0

def evaluer_orientation(lst: list) -> int:
    """Évalue l'orientation spatiale (somme des réussites)"""
    return sum(int(x) for x in lst if x is not None)

def evaluer_coord_dynamique(desc: str) -> int:
    """Évalue la coordination dynamique"""
    scores = {"3": 3, "2": 2, "1": 1, "0": 0}
    return scores.get(str(desc), 0)

def calculer_imc(poids, taille_cm):
    try:
        taille_m = taille_cm / 100
        return round(poids / (taille_m ** 2), 1)
    except:
        return None

def calculer_score_total(eleve_eval: dict) -> dict:
    """Calcule le score total et ajoute des statistiques"""
    score_total = (
        eleve_eval.get("Souplesse Tronc (pts)", 0) +
        eleve_eval.get("Souplesse Épaule (pts)", 0) +
        eleve_eval.get("Équilibre (pts)", 0) +
        eleve_eval.get("Orientation Spatiale (pts)", 0) +
        eleve_eval.get("Coord. Dynamiques (pts)", 0)
    )
    
    # Ajouter le score total
    eleve_eval["Score Total"] = score_total
    
    # Niveau de performance
    if score_total >= 20:
        niveau = "Excellent"
    elif score_total >= 15:
        niveau = "Bon"
    elif score_total >= 10:
        niveau = "Moyen"
    else:
        niveau = "À améliorer"
    
    eleve_eval["Niveau"] = niveau
    
    return eleve_eval

def evaluer_eleve(eleve: dict) -> dict:
    """Évalue un élève et retourne ses scores"""
    evaluation = {
        "Nom": eleve.get("nom", ""),
        "Souplesse Tronc (pts)": evaluer_souplesse_tronc(eleve.get("souplesse_tronc", "1")),
        "Souplesse Épaule (pts)": evaluer_souplesse_epaule(eleve.get("souplesse_epaule", "1")),
        "Équilibre (pts)": evaluer_equilibre(eleve.get("equilibre_sec", 0)),
        "Saut Vertical (cm)": eleve.get("saut_cm", 0),
        "Lancer BB (cm)": eleve.get("lancer_cm", 0),
        "Orientation Spatiale (pts)": evaluer_orientation(eleve.get("orientation", [])),
        "Coord. Dynamiques (pts)": evaluer_coord_dynamique(eleve.get("coord_desc", "0")),
        "Poids (kg)": eleve.get("poids", 0),
        "Taille (cm)": eleve.get("taille", 0),
        "IMC": calculer_imc(eleve.get("poids", 0), eleve.get("taille", 0))


    }
    
    # Ajouter le score total et le niveau
    evaluation = calculer_score_total(evaluation)
    
    return evaluation

def generer_rapport_classe(evaluations: list) -> dict:
    """Génère un rapport statistique pour la classe"""
    if not evaluations:
        return {}
    
    scores_totaux = [e.get("Score Total", 0) for e in evaluations]
    
    rapport = {
        "nombre_eleves": len(evaluations),
        "score_moyen": sum(scores_totaux) / len(scores_totaux),
        "score_max": max(scores_totaux),
        "score_min": min(scores_totaux),
        "repartition_niveaux": {}
    }
    
    # Compter les niveaux
    niveaux = [e.get("Niveau", "") for e in evaluations]
    for niveau in ["Excellent", "Bon", "Moyen", "À améliorer"]:
        rapport["repartition_niveaux"][niveau] = niveaux.count(niveau)
    
    return rapport

# Test des fonctions si le fichier est exécuté directement
if __name__ == "__main__":
    # Test d'évaluation
    eleve_test = {
        "nom": "Test Élève",
        "souplesse_tronc": "4",
        "souplesse_epaule": "3",
        "equilibre_sec": 28,
        "saut_cm": 45,
        "lancer_cm": 350,
        "poids": 60,
        "taille": 160,
        "orientation": [1, 1, 0, 1, 1, 0],
        "coord_desc": "2"
    }
    
    result = evaluer_eleve(eleve_test)
    print("Test d'évaluation d'élève:")
    for key, value in result.items():
        print(f"- {key}: {value}")
