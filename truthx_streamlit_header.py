import streamlit as st

# === HAUT DE PAGE TRUTHX ANALYZER ===

st.markdown("<div class='block'>🧠 <span class='title'>TruthX Analyzer – Analyse probatoire et comportementale</span></div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>TruthX est une intelligence artificielle conçue pour révéler les dynamiques invisibles dans les échanges écrits, audios ou publiés : emprise, pression psychologique, manipulation émotionnelle, signaux faibles comportementaux. L’objectif ? Offrir une aide à la décision pour les professionnels du droit, les victimes, les enquêteurs et les magistrats.</div>", unsafe_allow_html=True)

st.markdown("### 🔍 Modules d’analyse disponibles dans cette version MVP")

st.markdown("""
#### 1. Analyse linguistique (PNL)
Détection de tonalité et d’intention émotionnelle dans un message écrit. TruthX identifie par exemple :
- Pression affective (“Tu ne m’aimes plus”)
- Menace implicite (“Je ne répondrai plus si tu continues”)
- Emprise douce (“Je fais tout pour toi…”)
- Injonctions paradoxales

#### 2. Analyse documentaire (Fichiers PDF / PNG / .txt)
Extraction du texte, scan des contenus litigieux, construction d’un rapport PDF avec alertes comportementales détectées.

#### 3. Analyse OSINT (sources ouvertes)
Analyse d’un article ou d’un lien public. TruthX en extrait le texte et détecte les signaux faibles : violence mentionnée, manipulation émotionnelle, humiliation implicite…

#### 4. Moteur Quantic (à venir)
Un moteur expérimental qui identifie des dynamiques subtiles à partir d’une séquence d’événements.

---

### ⚖️ Ce que vous obtenez à la fin :
- 📄 Un rapport d’analyse clair (PDF)
- 🧠 Une restitution des signaux comportementaux
- 🚨 Des alertes juridiques et psychologiques
- 🔐 Une aide à la constitution de preuves recevables en contexte judiciaire
""")

st.markdown("---")
