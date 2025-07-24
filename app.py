# app.py - Version avec correction Excel
import streamlit as st
import pandas as pd
import os
from evaluation import evaluer_eleve
from utils import generer_eleves

st.set_page_config("Évaluation Capacités Motrices", layout="wide")

# Créer le dossier outputs s'il n'existe pas
os.makedirs("outputs", exist_ok=True)

# CSS pour améliorer l'apparence
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stExpander {
        border: 1px solid #e6e6e6;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

try:
    # Charger les données d'établissement avec différents engines
    df = None
    excel_path = "/Users/mac/Documents/les_projets_de_stage_PFA/evaluation_motrice_hosting/data/etab.xlsx"
    
    # Vérifier si le fichier existe
    if not os.path.exists(excel_path):
        st.error(f"❌ Fichier '{excel_path}' introuvable.")
        st.info("📋 Veuillez vous assurer que le fichier 'etab.xlsx' est dans le dossier 'data/'")
        st.stop()
    
    # Essayer différents engines
    engines_to_try = ['openpyxl', 'xlrd', None]
    
    for engine in engines_to_try:
        try:
            if engine:
                df = pd.read_excel(excel_path, engine=engine)
                st.success(f"✅ Fichier Excel chargé avec l'engine '{engine}'")
            else:
                df = pd.read_excel(excel_path)
                st.success(f"✅ Fichier Excel chargé avec l'engine par défaut")
            break
        except Exception as e:
            if engine == engines_to_try[-1]:  # Dernier engine
                raise e
            continue
    
    # Vérifier que les colonnes nécessaires existent
    required_columns = ["ll_reg", "ll_prov", "ll_com", "cd_etab"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Colonnes manquantes dans le fichier Excel: {missing_columns}")
        st.info("📋 Colonnes disponibles:", list(df.columns))
        st.stop()
    
    # Sélection hiérarchique
    st.sidebar.header("🏫 Sélection de l'établissement")
    
    # Afficher des infos sur les données
    st.sidebar.info(f"📊 {len(df)} établissements chargés")
    region = st.sidebar.selectbox("Région", sorted(df["ll_reg"].unique()))
    prov_df = df[df["ll_reg"] == region]
    
    province = st.sidebar.selectbox("Province", sorted(prov_df["ll_prov"].unique()))
    comm_df = prov_df[prov_df["ll_prov"] == province]
    
    commune = st.sidebar.selectbox("Commune", sorted(comm_df["ll_com"].unique()))
    etab_df = comm_df[comm_df["ll_com"] == commune]
    
    etab = st.sidebar.selectbox("Établissement", sorted(etab_df["cd_etab"]))
    niveau = st.sidebar.selectbox("Niveau", ["1A", "2A", "3A", "4A", "5A", "6A"])
    
    # Nombre d'élèves
    nb_eleves = st.sidebar.slider("Nombre d'élèves", 5, 50, 20)
    
except Exception as e:
    st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
    
    # Diagnostics détaillés
    st.subheader("🔍 Diagnostic du problème")
    
    if os.path.exists("data/etab.xlsx"):
        file_size = os.path.getsize("data/etab.xlsx")
        st.write(f"📁 Fichier trouvé, taille: {file_size} octets")
        
        if file_size == 0:
            st.warning("⚠️ Le fichier est vide !")
        elif file_size < 100:
            st.warning("⚠️ Le fichier semble très petit, il pourrait être corrompu.")
    else:
        st.write("📁 Fichier 'data/etab.xlsx' introuvable")
    
    st.subheader("🛠️ Solutions proposées")
    st.write("""
    1. **Vérifiez le fichier Excel:**
       - Le fichier existe-t-il dans le dossier 'data/' ?
       - Le fichier n'est-il pas corrompu ?
       - Essayez d'ouvrir le fichier dans Excel/LibreOffice
    
    2. **Installez les dépendances:**
       
bash
       pip install openpyxl xlrd

    
    3. **Vérifiez les colonnes du fichier:**
       - ll_reg (région)
       - ll_prov (province) 
       - ll_com (commune)
       - cd_etab (code établissement)
    """)
    st.stop()

# Interface principale
st.title(f"📊 Évaluation Motrice - {etab}")
st.markdown(f"**Niveau:** {niveau} | **Région:** {region} | **Province:** {province}")

# Générer les élèves
if "eleves_generes" not in st.session_state:
    st.session_state.eleves_generes = generer_eleves(nb_eleves)

eleves = st.session_state.eleves_generes

# État de session pour stockage
if "evals" not in st.session_state:
    st.session_state.evals = []

# Bouton pour régénérer les élèves
if st.button("🔄 Régénérer la liste des élèves"):
    st.session_state.eleves_generes = generer_eleves(nb_eleves)
    st.session_state.evals = []
    st.rerun()

# Saisie des performances
st.header("📝 Saisie des évaluations")

for i, eleve in enumerate(eleves):
    with st.expander(f"🧑‍🎓 {i+1}. {eleve['nom']}", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤸 Tests de souplesse")
            souplesse_tronc = st.selectbox("Souplesse Tronc", ["5", "4", "3", "2", "1"], key=f"tronc_{i}")
            souplesse_epaule = st.selectbox("Souplesse Épaule", ["5", "4", "3", "2", "1"], key=f"epa_{i}")
            equilibre = st.slider("Équilibre (sec)", 0, 40, 15, key=f"eq_{i}")
        
        with col2:
            st.subheader("🏃 Tests de force")
            saut_cm = st.number_input("Saut Vertical (cm)", 0, 100, 30, key=f"saut_{i}")
            lancer_cm = st.number_input("Lancer BB (cm)", 0, 1000, 200, key=f"lancer_{i}")
            coord_desc = st.selectbox("Coord. Dynamiques", ["3", "2", "1", "0"], key=f"cd_{i}")
        st.subheader("⚖️ Mesures anthropométriques")
        col_anthro_1, col_anthro_2 = st.columns(2)
        with col_anthro_1:
            poids = st.number_input("Poids (kg)", 10.0, 150.0, 35.0, key=f"poids_{i}")
        with col_anthro_2:
            taille = st.number_input("Taille (cm)", 80.0, 210.0, 140.0, key=f"taille_{i}")

        
        # Orientation spatiale
        st.subheader("🧭 Orientation spatiale")
        orientation_cols = st.columns(6)
        orientation = []
        for j in range(6):
            with orientation_cols[j]:
                orientation.append(st.checkbox(f"Mvt {j+1}", key=f"or_{i}_{j}"))
        
        eleve.update({
            "souplesse_tronc": souplesse_tronc,
            "souplesse_epaule": souplesse_epaule,
            "poids": poids,
            "taille": taille,
            "equilibre_sec": equilibre,
            "saut_cm": saut_cm,
            "lancer_cm": lancer_cm,
            "orientation": [int(v) for v in orientation],
            "coord_desc": coord_desc
        })

# Calculer les évaluations automatiquement
st.session_state.evals = [evaluer_eleve(eleve) for eleve in eleves]

# Afficher les résultats
if st.session_state.evals:
    st.header("📈 Résultats")
    df_results = pd.DataFrame(st.session_state.evals)
    st.dataframe(df_results, use_container_width=True)
    
    # Statistiques rapides
    col1, col2, col3 = st.columns(3)
    with col1:
        if "Score Total" in df_results.columns:
            st.metric("📊 Score moyen", f"{df_results['Score Total'].mean():.1f}")
    with col2:
        if "Score Total" in df_results.columns:
            st.metric("🏆 Score max", df_results['Score Total'].max())
    with col3:
        if "Score Total" in df_results.columns:
            st.metric("📉 Score min", df_results['Score Total'].min())
    
    # Export
    if st.button("📤 Exporter les résultats en Excel"):
        try:
            filename = f"outputs/evaluation_{etab}_{niveau}.xlsx"
            df_results.to_excel(filename, index=False, engine='openpyxl')
            st.success(f"✅ Fichier enregistré : {filename}")
            
            # Proposer le téléchargement
            with open(filename, "rb") as file:
                st.download_button(
                    label="⬇️ Télécharger le fichier Excel",
                    data=file.read(),
                    file_name=f"evaluation_{etab}_{niveau}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"❌ Erreur lors de l'export : {str(e)}")

# Guide d'évaluation dans la sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Guide d'évaluation")
st.sidebar.markdown("""
**Souplesse (1-5):**
- 5:Flexibilité très élevée
- 4: Flexibilité élevée
- 3: Flexibilité moyenne
- 2: Flexibilité Faible
- 1: Flexibilité très faible


**Équilibre:**
- 30s+ : 3 points
- 25-29s : 2 points  
- 20-24s : 1 point
- <20s : 0 point

**Orientation:** Nombre de mouvements réussis (0-6)
- mainG–ŒilD
- main D – Oreille G 
- main D – Œil G
- main G – Oreille G 
- main D – Œil G
- main G – Oreille D
- Évaluation : 1 point par réponse juste : Total = 6 points.
**Coordination (0-3):**
- Sauts continus = 3
- Sauts avec 1 interruption = 2
- Sauts avec 2 interruptions = 1
- Sauts avec plus de 2 interruptions = 0

                    
""")
