import streamlit as st
from io import BytesIO
from fpdf import FPDF
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from newspaper import Article
import pandas as pd
import unicodedata
import os
import tempfile

# Fonction enrichie pour l'analyse de tonalité
def analyse_tonalite(text):
    text_lower = text.lower()
    
    # Listes de mots-clés pour différentes tonalités
    aggressive_keywords = ["nulle", "honte", "pathétique", "inutile", "idiot", "stupide", "tarée", "débile", "conne", "imbécile", "ridicule"]
    culpabilisation_keywords = ["peine", "ignore", "pourquoi", "plus de nouvelles", "si tu", "à cause de toi", "par ta faute"]
    menace_keywords = ["verras", "sais", "passer", "bien", "attention", "gare à toi", "regarde"]
    soutien_keywords = ["là pour", "incroyable", "fier", "bravo", "génial", "super", "formidable"]
    seduction_keywords = ["moitié", "rien sans", "amour", "chéri", "adorable", "beau", "belle", "merveilleuse"]
    moquerie_keywords = ["pauvre", "pitoyable", "misérable", "ridicule", "haha", "lol", "c’est ça"]
    
    # Modificateurs d'intensité
    intensite_eleve = ["très", "vraiment", "toujours", "jamais", "tellement", "complètement", "totalement", "absolument"]
    intensite_subtile = ["un peu", "légèrement", "peut-être", "à peine"]
    
    # Détection de l'intensité
    intensite = "Modérée"
    for mot in intensite_eleve:
        if mot in text_lower:
            intensite = "Élevée"
            break
    for mot in intensite_subtile:
        if mot in text_lower:
            intensite = "Subtile"
            break
    
    # Détection des tonalités
    tonalite_principale = None
    tonalite_secondaire = None
    
    # Vérification des tonalités principales
    if any(keyword in text_lower for keyword in aggressive_keywords):
        tonalite_principale = "Agressive"
    elif any(keyword in text_lower for keyword in culpabilisation_keywords):
        tonalite_principale = "Culpabilisante"
    elif any(keyword in text_lower for keyword in menace_keywords):
        tonalite_principale = "Menaçante"
    elif any(keyword in text_lower for keyword in soutien_keywords):
        tonalite_principale = "Soutenante"
    elif any(keyword in text_lower for keyword in seduction_keywords):
        tonalite_principale = "Seductrice"
    else:
        tonalite_principale = "Neutre"
    
    # Vérification de la tonalité secondaire (Moquerie)
    if any(keyword in text_lower for keyword in moquerie_keywords):
        if tonalite_principale != "Neutre":
            tonalite_secondaire = "Moqueuse"
        else:
            tonalite_principale = "Moqueuse"
    
    # Construction de la tonalité finale
    if tonalite_principale == "Neutre":
        return "Neutre"
    elif tonalite_secondaire:
        return f"{tonalite_principale} et {tonalite_secondaire} ({intensite})"
    else:
        return f"{tonalite_principale} ({intensite})"

# Placeholder pour l'analyse OSINT ciblée sur une personne (simulé)
def analyse_osint_personne(nom, pseudo):
    # Simulation d'une recherche OSINT (à remplacer par une vraie implémentation)
    result = {
        "Nom": nom,
        "Pseudo": pseudo,
        "Résumé": "Analyse simulée : Recherche de données publiques sur les réseaux sociaux.",
        "Signaux": [
            {"Signal": "Culpabilisation douce", "Contenu": "Post sur Twitter : 'Pourquoi tu m'ignores ?'", "Effet": "Doute sur soi", "Juridique": "Art. 222-33-2-2"},
            {"Signal": "Menace implicite", "Contenu": "Commentaire sur LinkedIn : 'Tu verras bien...'", "Effet": "Peur intériorisée", "Juridique": "Harcèlement"}
        ]
    }
    return result

# Lexique comportemental enrichi avec les mots-clés de analyse_tonalite
LEXICON = {
    "culpabilisation": {
        "description": "Fait peser subtilement la faute sur l’autre, en se victimisant.",
        "formulations": ["tu me fais de la peine", "pourquoi tu m'ignores", "plus de nouvelles", "à cause de toi", "par ta faute"],
        "keywords": ["peine", "ignore", "pourquoi", "plus de nouvelles", "si tu", "à cause de toi", "par ta faute"],
        "effet": "Doute sur soi, repli affectif",
        "juridique": "Art. 222-33-2-2 (harcèlement moral)"
    },
    "dévalorisation": {
        "description": "Rabaissement psychologique.",
        "formulations": ["tu ne vaux rien", "tu me fais honte", "tu es folle", "je suis folle", "elle est folle", "il est fou"],
        "keywords": ["nulle", "honte", "pathétique", "inutile", "idiot", "stupide", "tarée", "débile", "conne", "imbécile", "ridicule"],
        "effet": "Perte de confiance, repli",
        "juridique": "Art. 222-33-2-2 (harcèlement moral)"
    },
    "double contrainte": {
        "description": "Injonctions contradictoires.",
        "formulations": ["fais ça mais pas comme ça", "tu dois mais tu ne peux pas"],
        "keywords": ["fais ça", "tu dois", "tu ne peux pas"],
        "effet": "Confusion, blocage",
        "juridique": "Stratégie coercitive"
    },
    "isolement": {
        "description": "Tentative de couper les liens.",
        "formulations": ["ne parle à personne", "tu n’as besoin de personne"],
        "keywords": ["ne parle", "besoin de personne"],
        "effet": "Dépendance, isolement social",
        "juridique": "Stratégie coercitive"
    },
    "menace implicite": {
        "description": "Provoque la peur ou l’angoisse sans menace directe.",
        "formulations": ["tu verras bien", "tu sais ce qu’il va se passer"],
        "keywords": ["verras", "sais", "passer", "bien", "attention", "gare à toi", "regarde"],
        "effet": "Peur intériorisée, blocage",
        "juridique": "Harcèlement / pression psychologique"
    },
    "dénégation de réalité": {
        "description": "Nie ce que l’autre vit ou ressent comme vrai.",
        "formulations": ["tu inventes encore", "tu dramatises tout", "tu es folle", "je suis folle", "elle est folle", "il est fou"],
        "keywords": ["inventes", "dramatises", "folle", "fou"],
        "effet": "Gaslighting, perte de repères",
        "juridique": "Altération du discernement"
    },
    "moquerie": {
        "description": "Ton sarcastique ou de dérision.",
        "formulations": ["pauvre", "pitoyable", "misérable", "ridicule", "haha", "lol", "c’est ça"],
        "keywords": ["pauvre", "pitoyable", "misérable", "ridicule", "haha", "lol", "c’est ça"],
        "effet": "Humiliation, perte de confiance",
        "juridique": "Art. 222-33-2-2 (harcèlement moral)"
    }
}

# Fonction pour analyser un message et détecter les signaux faibles
def detect_signals(message):
    signals = []
    message_lower = message.lower()
    for signal, details in LEXICON.items():
        # Recherche des mots-clés individuels
        for keyword in details["keywords"]:
            if keyword in message_lower:
                signals.append({
                    "signal": signal,
                    "description": details["description"],
                    "formulation": keyword,  # On utilise le mot-clé détecté comme formulation
                    "effet": details["effet"],
                    "juridique": details["juridique"]
                })
                break  # Évite de dupliquer si plusieurs mots-clés de la même catégorie sont détectés
        # Recherche de correspondance exacte pour les formulations (pour maintenir la compatibilité)
        for formulation in details["formulations"]:
            if formulation in message_lower:
                signals.append({
                    "signal": signal,
                    "description": details["description"],
                    "formulation": formulation,
                    "effet": details["effet"],
                    "juridique": details["juridique"]
                })
                break
    return signals

# Fonction pour nettoyer les chaînes et gérer les caractères non pris en charge
def clean_text_for_pdf(text):
    # Normaliser la chaîne pour décomposer les caractères Unicode (par exemple, "\u2013" -> "-")
    text = unicodedata.normalize('NFKD', text)
    # Remplacer les caractères non pris en charge par des équivalents compatibles
    text = text.encode('latin-1', 'replace').decode('latin-1')
    return text

# === CONFIGURATION ===
st.set_page_config(page_title="TruthX Analyzer", layout="wide")

# === STYLES CSS ===
st.markdown("""
<style>
body { 
    background-color: #141C26 !important; 
    color: #FFFFFF !important; 
    font-family: 'Roboto', sans-serif !important; 
}
div.stApp {
    background-color: #141C26 !important;
}
div.stApp > div {
    background-color: #141C26 !important;
}
.sidebar .sidebar-content {
    background: #1E2A38 !important;
    padding: 20px;
    border-right: 1px solid #2A3B4D;
}
.block { 
    background: #1E2A38 !important; 
    padding: 30px; 
    border-radius: 12px; 
    margin-bottom: 30px; 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); 
    border-left: 4px solid #FF6F61; 
    transition: transform 0.3s ease, box-shadow 0.3s ease; 
}
.block:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}
.title { 
    color: #FFFFFF !important; 
    font-size: 28px; 
    font-weight: 600; 
    margin-bottom: 15px; 
    display: flex; 
    align-items: center; 
}
.title svg { 
    margin-right: 12px; 
    stroke: #FF6F61 !important; 
}
.subtitle { 
    color: #B0BEC5 !important; 
    font-size: 16px; 
    line-height: 1.8; 
    margin-bottom: 20px; 
}
.subtitle ul, .subtitle li {
    color: #B0BEC5 !important;
    margin-bottom: 10px;
}
.button { 
    background-color: #FF6F61; 
    color: white; 
    padding: 0.75em 1.5em; 
    border: none; 
    border-radius: 8px; 
    font-weight: 500; 
    transition: background-color 0.3s ease; 
}
.button:hover { 
    background-color: #E65A50; 
}
.report-list li:nth-child(1) { 
    color: #4CAF50 !important; 
} /* Vert */
.report-list li:nth-child(2) { 
    color: #FFCA28 !important; 
} /* Jaune */
.report-list li:nth-child(3) { 
    color: #EF5350 !important; 
} /* Rouge clair */
.subtitle strong { 
    color: #FFFFFF !important; 
}
.badge { 
    background-color: #FF6F61; 
    color: white; 
    padding: 5px 10px; 
    border-radius: 12px; 
    font-size: 14px; 
    margin-right: 5px; 
}
.sidebar-title {
    color: #FF6F61 !important;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
    text-align: center;
}
.nav-item { 
    display: flex; 
    align-items: center; 
    padding: 8px 12px; 
    border-radius: 6px; 
    margin-bottom: 8px; 
    transition: background 0.3s ease; 
}
.nav-item:hover { 
    background: #2A3B4D; 
}
.nav-item svg { 
    margin-right: 10px; 
    stroke: #FF6F61 !important; 
}
.quantum-section {
    border-left: 6px solid #FF6F61;
    padding-left: 15px;
}
.stSelectbox > div > div > div {
    background: #1E2A38 !important;
    color: #FFFFFF !important;
    border: 1px solid #FF6F61;
    border-radius: 8px;
    position: relative;
    padding-right: 30px; /* Espace pour la flèche */
}
/* Cacher le conteneur séparé de la flèche par défaut */
.stSelectbox > div > div > div > div[data-baseweb="select"] > div:last-child {
    display: none !important;
}
/* Ajouter une flèche personnalisée à l'intérieur du rectangle principal */
.stSelectbox > div > div > div > div[data-baseweb="select"]::after {
    content: '';
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
}
.stSelectbox > div > div > div > div:hover {
    background: #2A3B4D !important;
}
/* Ajuster la couleur des labels des champs de saisie */
div.stTextInput > label,
div.stTextArea > label,
div.stFileUploader > label {
    color: #FFFFFF !important;
    font-weight: 500;
}
/* Nouvelle règle CSS pour "Résultat de l’analyse" */
.result-title {
    color: #FFFFFF !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    margin-bottom: 10px !important;
}
/* Nouvelle règle CSS pour "Tonalité détectée" */
.tonality {
    color: #FFFFFF !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# Utilisation de st.session_state pour stocker le buffer
if 'buffer' not in st.session_state:
    st.session_state.buffer = None

# === SIDEBAR ===
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>TruthX Analyzer</h2>", unsafe_allow_html=True)
    page = st.selectbox("Navigation", 
                        ["Accueil", "Analyse de Fichier", "Détection de Signaux", "Moteur Quantique", "OSINT - Lien Public", "OSINT - Article", "OSINT - Profil Individuel", "Cadre Légal & Sécurité", "Limites et Responsabilités"],
                        key="nav_selectbox")

# === PAGE D’ACCUEIL ===
if page == "Accueil":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M12 2a10 10 0 0 0-10 10c0 5.52 4.48 10 10 10s10-4.48 10-10a10 10 0 0 0-10-10z'/>
                <path d='M12 6v6l4 2'/>
            </svg>
            TruthX Analyzer - Analyse Forensique et Comportementale
        </div>
        <div class='subtitle'>
            TruthX est une solution d’intelligence artificielle avancée conçue pour détecter et analyser les dynamiques complexes d’infiltrations, de manipulations, d’espionnage, de contrôle coercitif et de surveillance. Développée pour les magistrats, avocats, juges, ainsi que les professionnels des ressources humaines, de la compliance et de la cybersécurité, TruthX fournit des insights juridiques et comportementaux exploitables.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z'/>
            </svg>
            Détection des Dynamiques Complexes
        </div>
        <div class='subtitle'>
            TruthX excelle dans l’identification des signaux faibles et des dynamiques comportementales complexes, offrant des analyses approfondies pour :
            <ul>
                <li><strong>Infiltrations non documentées</strong> : Détection de schémas d’influence ou d’intrusion dans des communications.</li>
                <li><strong>Manipulations et espionnage</strong> : Analyse des tentatives de contrôle ou d’extraction d’informations sensibles.</li>
                <li><strong>Contrôle coercitif</strong> : Identification des pressions psychologiques et des dynamiques de pouvoir dans les échanges.</li>
                <li><strong>Surveillance illégale</strong> : Repérage des traces de filatures ou de captations non autorisées.</li>
                <li><strong>Compliance et cybersécurité</strong> : Évaluation des risques internes et externes pour les entreprises.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === SECTION MOTEURS D’ANALYSE ===
    st.markdown("""
    <div class='block quantum-section'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M12 2a10 10 0 0 0-10 10c0 5.52 4.48 10 10 10s10-4.48 10-10a10 10 0 0 0-10-10z'/>
                <path d='M12 6v6l4 2'/>
            </svg>
            Moteurs d’Analyse Avancés de TruthX
        </div>
        <div class='subtitle'>
            TruthX intègre des technologies de pointe pour répondre aux besoins des professionnels :
            <ul>
                <li><strong>Moteur Forensique</strong> : Extraction et analyse de contenus textuels (PDF, PNG, .txt) pour identifier les signaux faibles et produire des rapports probatoires juridiquement recevables.</li>
                <li><strong>Moteur Quantique</strong> : Analyse des dynamiques comportementales temporelles pour anticiper les risques et cartographier les interactions complexes.</li>
                <li><strong>OSINT (Open-Source Intelligence)</strong> : Investigation de sources publiques pour détecter manipulations narratives, violences implicites et influences externes.</li>
                <li><strong>Analyse Juridique Intégrée</strong> : Alignement avec les cadres légaux (ex. Articles 313-1, 223-1, 434-1 du Code pénal) pour qualifier les dynamiques détectées.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === BLOCS JURIDIQUES ===
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M3 10h18M3 6h18M3 14h18M3 18h18'/>
            </svg>
            Fondements Juridiques de TruthX
        </div>
        <div class='subtitle'>
            TruthX repose sur un socle juridique robuste pour qualifier les dynamiques détectées :
            <ul>
                <li>Article 313-1 - Escroquerie (manoeuvres frauduleuses)</li>
                <li>Article 223-1 - Mise en danger délibérée</li>
                <li>Article 434-1 - Obstacle à la manifestation de la vérité</li>
            </ul>
            <details>
                <summary style='color: #FF6F61; cursor: pointer;'>En savoir plus</summary>
                <ul>
                    <li>Articles 226-1 à 226-4 - Atteinte à la vie privée (filatures, captations, intrusion)</li>
                    <li>Article 121-7 - Complicité par instigation ou fourniture de moyens</li>
                    <li>Articles 321-1 et suivants - Recel, blanchiment</li>
                    <li>Code de procédure pénale, article 40 - Obligation de signalement</li>
                    <li>Convention EDH - Art. 6 (procès équitable), Art. 3 (traitements inhumains)</li>
                </ul>
            </details>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === ENCADRÉ POUR TÉLÉCHARGER LE RAPPORT ===
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M12 15V3M9 12l3 3 3-3M5 19h14'/>
            </svg>
            Télécharger le Rapport TruthX Complet
        </div>
        <div class='subtitle'>
            Ce rapport a été généré automatiquement à partir de votre analyse :
            <ul class="report-list">
                <li>Signaux faibles détectés</li>
                <li>Tonalité comportementale</li>
                <li>Références juridiques associées</li>
            </ul>
            Vous pouvez le télécharger ou le transmettre pour une analyse juridique approfondie.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.buffer is not None and st.session_state.buffer.getvalue():
        st.download_button(
            label="Télécharger le Rapport TruthX au Format PDF",
            data=st.session_state.buffer,
            file_name="rapport truthx.pdf",
            mime="application/pdf")
    else:
        st.warning("Aucun rapport disponible. Veuillez lancer une analyse pour générer un rapport.")

# === UPLOAD ET ANALYSE FICHIER ===
if page == "Analyse de Fichier":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/>
                <path d='M14 2v6h6'/>
            </svg>
            Analyse de Fichier - Module Forensique
        </div>
        <div class='subtitle'>
            Téléchargez un fichier texte, PDF ou PNG contenant des échanges ou des données sensibles. TruthX extrait le contenu et détecte les signaux de manipulation, contrôle coercitif ou surveillance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choisissez un fichier (.txt, .pdf ou .png)", type=['txt', 'pdf', 'png'])
    if uploaded_file:
        st.success(f"Fichier chargé : {uploaded_file.name}")
        # Ajouter un message de débogage pour vérifier le type de fichier
        st.info(f"Type de fichier détecté : {uploaded_file.type}")

    if st.button("Lancer l’Analyse Forensique", key="analyse_fichier"):
        if not uploaded_file:
            st.warning("Veuillez d'abord téléverser un fichier.")
        else:
            try:
                # Vérifier la taille du fichier (limite à 10 Mo pour éviter les problèmes de performance)
                file_size = uploaded_file.size / (1024 * 1024)  # Taille en Mo
                if file_size > 10:
                    st.error("Le fichier est trop volumineux (limite : 10 Mo). Veuillez utiliser un fichier plus petit.")
                else:
                    # Extraction du contenu selon le type de fichier
                    contenu = ""
                    # Lire le contenu du fichier une seule fois et le stocker
                    file_content = uploaded_file.read()
                    # Vérifier l'extension du fichier pour une détection plus robuste
                    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                    if file_extension == ".pdf" or uploaded_file.type == "application/pdf":
                        try:
                            # Écrire le contenu dans un fichier temporaire
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                                temp_file.write(file_content)
                                temp_file_path = temp_file.name
                            # Utiliser PyPDF2 avec le chemin du fichier temporaire
                            with open(temp_file_path, 'rb') as f:
                                reader = PdfReader(f)
                                contenu = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                            # Supprimer le fichier temporaire
                            os.unlink(temp_file_path)
                            if not contenu:
                                st.warning("Aucun texte extrait du PDF. Assurez-vous que le PDF contient du texte et non des images.")
                        except Exception as e:
                            st.error(f"Erreur lors de l'extraction du texte du PDF : {str(e)}. Essayez de convertir le PDF en texte ou de vérifier qu'il n'est pas scanné.")
                    elif file_extension in [".png", ".jpg", ".jpeg"] or uploaded_file.type.startswith("image/"):
                        try:
                            # Recréer un BytesIO à partir du contenu lu pour PIL
                            file_stream = BytesIO(file_content)
                            image = Image.open(file_stream)
                            # Écrire temporairement l'image sur le disque pour pytesseract
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                                image.save(temp_file.name)
                                contenu = pytesseract.image_to_string(temp_file.name, lang='eng')
                            # Supprimer le fichier temporaire
                            os.unlink(temp_file.name)
                            if not contenu:
                                st.warning("Aucun texte extrait de l'image. Assurez-vous que l'image est de bonne qualité et contient du texte lisible.")
                        except Exception as e:
                            st.error(f"Erreur lors de l'extraction du texte de l'image : {str(e)}. Vérifiez que Tesseract OCR est correctement installé et que l'image contient du texte lisible.")
                    elif file_extension == ".txt" or uploaded_file.type == "text/plain":
                        try:
                            contenu = file_content.decode("utf-8")
                        except Exception as e:
                            st.error(f"Erreur lors de la lecture du fichier texte : {str(e)}. Assurez-vous que le fichier est au format UTF-8.")
                    else:
                        st.error("Type de fichier non pris en charge. Veuillez utiliser un fichier .txt, .pdf ou .png.")

                    if contenu:
                        # Afficher le contenu extrait
                        st.markdown("<div class='result-title'>Contenu Extrait :</div>", unsafe_allow_html=True)
                        st.text_area("Aperçu brut", contenu[:1500] if contenu else "Aucun contenu extrait.", height=250)

                        # Analyse des signaux faibles
                        messages = contenu.split("\n")
                        analysis_results = []
                        for msg in messages:
                            if msg.strip():
                                signals = detect_signals(msg)
                                if signals:
                                    for signal in signals:
                                        analysis_results.append({
                                            "Message": msg,
                                            "Signal Détecté": signal["signal"].capitalize(),
                                            "Description": signal["description"],
                                            "Formulation": signal["formulation"],
                                            "Effet Psychologique": signal["effet"],
                                            "Référence Juridique": signal["juridique"]
                                        })

                        # Afficher les résultats sous forme de tableau
                        if analysis_results:
                            st.error("Signaux Détectés :")
                            df = pd.DataFrame(analysis_results)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.success("Aucun signal faible détecté dans cet extrait.")

                        # Génération du PDF
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        # Nettoyer le titre statique avant de l'utiliser
                        pdf_title = clean_text_for_pdf("Rapport TruthX - Signaux Faibles Detectes")
                        pdf.cell(200, 10, pdf_title, ln=True, align='C')
                        pdf.ln(10)

                        pdf.set_font("Arial", 'B', size=10)
                        pdf.cell(200, 10, "Résultats de l'Analyse", ln=True)
                        pdf.set_font("Arial", size=10)
                        for result in analysis_results:
                            # Nettoyer les chaînes avant de les passer à FPDF
                            message = clean_text_for_pdf(result['Message'][:50]) + "..."
                            signal = clean_text_for_pdf(result['Signal Détecté'])
                            description = clean_text_for_pdf(result['Description'])
                            effet = clean_text_for_pdf(result['Effet Psychologique'])
                            juridique = clean_text_for_pdf(result['Référence Juridique'])
                            pdf.cell(200, 10, f"Message: {message}", ln=True)
                            pdf.cell(200, 10, f"Signal: {signal}", ln=True)
                            pdf.cell(200, 10, f"Description: {description}", ln=True)
                            pdf.cell(200, 10, f"Effet: {effet}", ln=True)
                            pdf.cell(200, 10, f"Référence Juridique: {juridique}", ln=True)
                            pdf.ln(5)

                        pdf.ln(10)
                        pdf.set_font("Arial", 'B', size=10)
                        pdf.cell(200, 10, "Lexique Comportemental", ln=True)
                        pdf.set_font("Arial", size=10)
                        for signal, details in LEXICON.items():
                            signal_name = clean_text_for_pdf(signal.capitalize())
                            desc = clean_text_for_pdf(details['description'])
                            effet = clean_text_for_pdf(details['effet'])
                            juridique = clean_text_for_pdf(details['juridique'])
                            pdf.cell(200, 10, f"{signal_name}: {desc}", ln=True)
                            pdf.cell(200, 10, f"Effet: {effet}", ln=True)
                            pdf.cell(200, 10, f"Référence: {juridique}", ln=True)
                            pdf.ln(5)

                        buffer = BytesIO()
                        pdf.output(buffer)
                        buffer.seek(0)
                        st.session_state.buffer = buffer

                        st.markdown("""
                        <div class='block'>
                            <div class='title'>
                                <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                                    <path d='M12 15V3M9 12l3 3 3-3M5 19h14'/>
                                </svg>
                                Télécharger le Rapport TruthX Complet
                            </div>
                            <div class='subtitle'>
                                Ce rapport a été généré automatiquement à partir de votre analyse :
                                <ul class="report-list">
                                    <li>Signaux faibles détectés</li>
                                    <li>Tonalité comportementale</li>
                                    <li>Références juridiques associées</li>
                                </ul>
                                Vous pouvez le télécharger ou le transmettre pour une analyse juridique approfondie.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.download_button(
                            label="Télécharger le Rapport TruthX au Format PDF",
                            data=st.session_state.buffer,
                            file_name="rapport truthx.pdf",
                            mime="application/pdf")

            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {str(e)}")

# === ANALYSE DE MESSAGE POUR DÉTECTION DE SIGNAUX ===
if page == "Détection de Signaux":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M9 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h4'/>
            </svg>
            Détection de Signaux
        </div>
        <div class='subtitle'>
            Entrez un message libre pour une analyse de tonalité comportementale. TruthX détecte les signaux de manipulation, de pression psychologique ou de contrôle coercitif.
        </div>
    </div>
    """, unsafe_allow_html=True)
    message = st.text_area("Message à analyser :")
    if st.button("Analyser avec Grok", key="analyse_pnl"):
        if not message:
            st.warning("Veuillez entrer un message à analyser.")
        else:
            try:
                tonalite = analyse_tonalite(message)
                signals = detect_signals(message)
                st.markdown("<div class='result-title'>Résultat de l’Analyse</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='tonality'>**Tonalité détectée** : {tonalite}</div>", unsafe_allow_html=True)
                st.text_area("Message analysé :", value=message, height=150)

                if signals:
                    st.error("Signaux Détectés :")
                    analysis_results = []
                    for signal in signals:
                        analysis_results.append({
                            "Message": message,
                            "Signal Détecté": signal["signal"].capitalize(),
                            "Description": signal["description"],
                            "Formulation": signal["formulation"],
                            "Effet Psychologique": signal["effet"],
                            "Référence Juridique": signal["juridique"]
                        })
                    df = pd.DataFrame(analysis_results)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.success("Aucun signal faible détecté dans ce message.")

            except Exception as e:
                st.error(f"Erreur lors de l’analyse : {str(e)}")

# === MODULE OSINT COMPORTEMENTAL — LIEN PUBLIC ===
if page == "OSINT - Lien Public":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 /working_directory/TruthX_Analyzer/streamlit_app.py24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'/>
                <path d='M15 3h6v6'/>
                <path d='M10 14L21 3'/>
            </svg>
            OSINT Comportemental - Analyse de Source Ouverte
        </div>
        <div class='subtitle'>
            Collez un lien vers une source publique (tweet, article, profil LinkedIn, etc.). TruthX analyse le contenu pour détecter des signaux de manipulation, d’espionnage ou de surveillance.
        </div>
    </div>
    """, unsafe_allow_html=True)
    url = st.text_input("Entrez un lien public (ex : tweet, article, profil LinkedIn, etc.)")
    if st.button("Lancer l’Analyse OSINT", key="osint_lien"):
        if url:
            try:
                article = Article(url)
                article.download()
                article.parse()
                contenu = article.text[:1500] if article.text else "Impossible d'extraire le contenu."
                tonalite = analyse_tonalite(contenu)
                signals = detect_signals(contenu)
                st.markdown("<div class='result-title'>Résultat OSINT</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='tonality'>**Tonalité détectée** : {tonalite}</div>", unsafe_allow_html=True)
                st.text_area("Contenu analysé :", value=contenu, height=150)

                if signals:
                    st.error("Signaux Détectés :")
                    analysis_results = []
                    for signal in signals:
                        analysis_results.append({
                            "Contenu": contenu[:50] + "...",
                            "Signal Détecté": signal["signal"].capitalize(),
                            "Description": signal["description"],
                            "Formulation": signal["formulation"],
                            "Effet Psychologique": signal["effet"],
                            "Référence Juridique": signal["juridique"]
                        })
                    df = pd.DataFrame(analysis_results)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.success("Aucun signal faible critique détecté.")

            except Exception as e:
                st.error(f"Erreur lors de l’analyse : {str(e)}")
        else:
            st.warning("Veuillez coller un lien valide.")

# === MODULE OSINT COMPORTEMENTAL — ARTICLE DE PRESSE ===
if page == "OSINT - Article":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M3 4h18M3 8h18M3 12h18M3 16h18M3 20h18'/>
            </svg>
            OSINT - Analyse d’Article de Presse
        </div>
        <div class='subtitle'>
            Collez une URL d’article de presse. TruthX extrait le contenu et détecte les signaux faibles liés à l’influence, la manipulation ou la surveillance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    url_article = st.text_input("URL de l’article à analyser")
    if st.button("Analyser l’Article", key="osint_article"):
        if not url_article:
            st.warning("Merci d’entrer une URL valide.")
        else:
            try:
                article = Article(url_article)
                article.download()
                article.parse()
                contenu_article = article.text[:1500] if article.text else "Impossible d'extraire le contenu."
                titre_article = article.title if article.title else "Titre indisponible"

                st.success(f"Article chargé : {titre_article}")
                st.text_area("Contenu extrait :", value=contenu_article, height=300)

                signals = detect_signals(contenu_article)
                if signals:
                    st.error("Signaux faibles détectés dans l’article :")
                    analysis_results = []
                    for signal in signals:
                        analysis_results.append({
                            "Contenu": contenu_article[:50] + "...",
                            "Signal Détecté": signal["signal"].capitalize(),
                            "Description": signal["description"],
                            "Formulation": signal["formulation"],
                            "Effet Psychologique": signal["effet"],
                            "Référence Juridique": signal["juridique"]
                        })
                    df = pd.DataFrame(analysis_results)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.success("Aucun signal faible critique détecté.")

            except Exception as e:
                st.error(f"Erreur lors de l’analyse : {str(e)}")

# === NOUVEAU MODULE OSINT — PROFIL INDIVIDUEL ===
if page == "OSINT - Profil Individuel":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/>
                <path d='M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8z'/>
            </svg>
            OSINT - Analyse de Profil Individuel
        </div>
        <div class='subtitle'>
            Entrez le nom ou le pseudo d’une personne pour lancer une investigation ciblée sur ses activités publiques (réseaux sociaux, forums, etc.). TruthX détecte les signaux de manipulation, d’espionnage ou de surveillance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    nom = st.text_input("Nom de la personne :")
    pseudo = st.text_input("Pseudo (ex. Twitter, LinkedIn) :")
    if st.button("Lancer l’Investigation OSINT", key="osint_personne"):
        if not nom and not pseudo:
            st.warning("Veuillez entrer un nom ou un pseudo.")
        else:
            try:
                result = analyse_osint_personne(nom, pseudo)
                st.markdown("<div class='result-title'>Résultat de l’Investigation OSINT</div>", unsafe_allow_html=True)
                st.markdown(f"**Nom** : {result['Nom']}")
                st.markdown(f"**Pseudo** : {result['Pseudo']}")
                st.markdown(f"**Résumé** : {result['Résumé']}")

                if result["Signaux"]:
                    st.error("Signaux Détectés :")
                    analysis_results = []
                    for signal in result["Signaux"]:
                        analysis_results.append({
                            "Contenu": signal["Contenu"],
                            "Signal Détecté": signal["Signal"],
                            "Effet Psychologique": signal["Effet"],
                            "Référence Juridique": signal["Juridique"]
                        })
                    df = pd.DataFrame(analysis_results)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.success("Aucun signal faible critique détecté.")

            except Exception as e:
                st.error(f"Erreur lors de l’investigation : {str(e)}")

# === PAGE CADRE LÉGAL & SÉCURITÉ ===
if page == "Cadre Légal & Sécurité":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M3 10h18M3 6h18M3 14h18M3 18h18'/>
            </svg>
            Cadre Légal & Sécurité
        </div>
        <div class='subtitle'>
            TruthX est conçu pour respecter les exigences légales et éthiques dans le traitement des données sensibles :
            <ul>
                <li><strong>Conformité RGPD</strong> : Les fichiers analysés ne sont jamais stockés ; le traitement est effectué en mémoire uniquement. TruthX respecte les principes de finalité, minimisation, et sécurité.</li>
                <li><strong>Contrôle Utilisateur</strong> : Vous gardez un contrôle total sur vos données. Aucun fichier ne transite sur des serveurs externes, et le rapport généré est téléchargeable directement.</li>
                <li><strong>Admissibilité Probatoire</strong> : Les rapports générés sont structurés pour être compatibles avec les exigences du droit de la preuve (art. 427 CPP, art. 9 CPC), avec horodatage et indexation des signaux détectés.</li>
                <li><strong>Transparence</strong> : TruthX est une aide à l’analyse et ne constitue pas une preuve en soi sans contextualisation. Les résultats doivent être interprétés par des professionnels.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === PAGE LIMITES ET RESPONSABILITÉS ===
if page == "Limites et Responsabilités":
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M3 10h18M3 6h18M3 14h18M3 18h18'/>
            </svg>
            Limites et Responsabilités
        </div>
        <div class='subtitle'>
            TruthX est conçu comme un outil d’aide à l’analyse et non comme un substitut à une expertise juridique ou judiciaire :
            <ul>
                <li><strong>Non-substitution au droit</strong> : TruthX n’est pas un avocat. L’interprétation juridique des analyses reste du ressort des magistrats, avocats ou enquêteurs.</li>
                <li><strong>Rôle d’appui</strong> : TruthX peut être utilisé en appui à une procédure judiciaire, mais ne remplace pas une expertise humaine.</li>
                <li><strong>Responsabilité</strong> : Les résultats fournis par TruthX doivent être contextualisés et validés par des professionnels avant toute utilisation dans un cadre juridique.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === MOTEUR QUANTIQUE ===
if page == "Moteur Quantique":
    st.markdown("""
    <div class='block quantum-section'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M12 2a10 10 0 0 0-10 10c0 5.52 4.48 10 10 10s10-4.48 10-10a10 10 0 0 0-10-10z'/>
                <path d='M12 6v6l4 2'/>
            </svg>
            Moteur Quantique TruthX
        </div>
        <div class='subtitle'>
            Le moteur quantique de TruthX analyse les dynamiques comportementales dans le temps pour détecter des patterns complexes liés à l’infiltration, l’espionnage ou la surveillance :
            <ul>
                <li>Analyse probabiliste des évolutions comportementales.</li>
                <li>Anticipation des risques d’influence ou de manipulation.</li>
                <li>Cartographie temporelle des interactions critiques.</li>
            </ul>
            Exemple de résultat (placeholder) :<br>
            <strong>Dynamique détectée :</strong> "Tendance croissante à la pression coercitive sur 3 mois (probabilité : 82%)"
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Analyser la Dynamique", key="moteur_quantique"):
        st.markdown("""
        <div class='block'>
            <div class='subtitle'>
                Analyse comportementale en cours... Résultat simulé : 'Tendance croissante à la pression coercitive sur 3 mois (probabilité : 82%)'.
            </div>
        </div>
        """, unsafe_allow_html=True)

# === BLOC FINAL — ENCADRÉ POUR TÉLÉCHARGER LE RAPPORT ===
# Afficher uniquement si un rapport a été généré
if page in ["Analyse de Fichier", "OSINT - Profil Individuel"] and st.session_state.buffer is not None and st.session_state.buffer.getvalue():
    st.markdown("""
    <div class='block'>
        <div class='title'>
            <svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#FF6F61' stroke-width='2'>
                <path d='M12 15V3M9 12l3 3 3-3M5 19h14'/>
            </svg>
            Télécharger le Rapport TruthX Complet
        </div>
        <div class='subtitle'>
            Ce rapport a été généré automatiquement à partir de votre analyse :
            <ul class="report-list">
                <li>Signaux faibles détectés</li>
                <li>Tonalité comportementale</li>
                <li>Références juridiques associées</li>
            </ul>
            Vous pouvez le télécharger ou le transmettre pour une analyse juridique approfondie.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Télécharger le Rapport TruthX au Format PDF",
        data=st.session_state.buffer,
        file_name="rapport truthx.pdf",
        mime="application/pdf")