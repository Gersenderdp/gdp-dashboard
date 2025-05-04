# 📁 truthx_legal_interface.py

# ==========================
# 📌 Bloc explicatif juridique
# ==========================
legal_block = """
<div class="legal">
    ⚖️ <b>Fondements juridiques de l’analyse TruthX</b><br><br>
    TruthX repose sur un socle juridique élargi permettant de qualifier les dynamiques complexes :
    <ul>
        <li><b>Article 313-1</b> du Code pénal — Escroquerie (manœuvres frauduleuses)</li>
        <li><b>Article 223-1</b> — Mise en danger délibérée de la personne d’autrui</li>
        <li><b>Article 434-1</b> — Obstacle à la manifestation de la vérité</li>
        <li><b>Articles 226-1 à 226-4</b> — Atteinte à la vie privée (filatures, captations, intrusion)</li>
        <li><b>Article 121-7</b> — Complicité par instigation ou fourniture de moyens</li>
        <li><b>Articles 321-1 et suivants</b> — Recel, blanchiment</li>
        <li><b>Code de procédure pénale, article 40</b> — Obligation de signalement</li>
        <li><b>Convention EDH</b> — Art. 6 (procès équitable), art. 3 (traitements inhumains)</li>
    </ul>
</div>
"""

# ==========================
# 📌 Bloc d'explication de l'interface
# ==========================
interface_block = """
<div class="interface-explained">
    🧠 <b>TruthX Analyzer</b> combine plusieurs couches d'analyse :
    <ul>
        <li><b>1. Analyse linguistique</b> : extraction de signaux faibles, alertes sémantiques, tonalité</li>
        <li><b>2. Analyse comportementale</b> : construction d'une dynamique dans le temps (moteur quantique)</li>
        <li><b>3. Analyse OSINT</b> : vérification des contenus publics, influence, manipulation narrative</li>
        <li><b>4. Cartographie relationnelle</b> : lecture des interactions, ruptures, noeuds critiques</li>
        <li><b>5. Restitution probatoire</b> : PDF automatique, export des preuves, alignement avec les codes</li>
    </ul>
</div>
"""

# ==========================
# 📌 Bloc schéma invisible
# ==========================
invisible_shema_block = """
<div class="invisible-shema">
    🔍 <b>TruthX dévoile ce qui échappe à l'analyse classique :</b><br><br>
    <i>"Un signal faible n'est pas une preuve en soi, mais un point d'accroche. TruthX les accumule, les structure, et les rattache à un cadre juridique et temporel."</i><br><br>
    Cela permet d'objectiver :
    <ul>
        <li>Des infiltrations non documentées</li>
        <li>Des déstabilisations programmées</li>
        <li>Des systèmes relationnels organisés</li>
        <li>Des dissonances narratives ou comportementales</li>
    </ul>
</div>
"""

# ==========================
# 📌 Fonction à injecter dans streamlit_app.py
# ==========================
def afficher_blocs_legaux():
    import streamlit as st
    st.markdown(legal_block, unsafe_allow_html=True)
    st.markdown(interface_block, unsafe_allow_html=True)
    st.markdown(invisible_shema_block, unsafe_allow_html=True)
