import networkx as nx

class QuanticEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._initialiser_modele()

    def _initialiser_modele(self):
        """
        Initialise la structure du graphe quantique avec les phases et signaux typiques d'une dynamique d'emprise.
        """
        noeuds = [
            "Approche séductrice",
            "Compliments excessifs",
            "Mise en confiance",
            "Isolation progressive",
            "Emprise psychologique",
            "Messages culpabilisants",
            "Rupture / Domination",
            "Menaces implicites",
            "Contrôle financier"
        ]

        for noeud in noeuds:
            self.graph.add_node(noeud)

        liaisons = [
            ("Approche séductrice", "Compliments excessifs", 1.0),
            ("Compliments excessifs", "Mise en confiance", 1.0),
            ("Mise en confiance", "Isolation progressive", 1.0),
            ("Isolation progressive", "Emprise psychologique", 1.2),
            ("Emprise psychologique", "Messages culpabilisants", 1.5),
            ("Messages culpabilisants", "Rupture / Domination", 1.5),
            ("Isolation progressive", "Contrôle financier", 0.8),
            ("Contrôle financier", "Rupture / Domination", 1.0),
            ("Emprise psychologique", "Menaces implicites", 1.3),
            ("Menaces implicites", "Rupture / Domination", 1.6)
        ]

        for source, cible, poids in liaisons:
            self.graph.add_edge(source, cible, weight=poids)

        # Calculer le score maximum théorique pour le contrôle coercitif
        self.max_score = 6.1  # Chemin le plus grave : 1.0 + 1.0 + 1.0 + 1.2 + 1.3 + 1.6

    def analyser_signaux(self, chemin):
        """
        Analyse un chemin hypothétique dans le graphe pour évaluer le degré d'alerte et la probabilité de contrôle coercitif.
        chemin : liste de noeuds correspondant à des événements observés.
        Retourne un score cumulé, une alerte, et une probabilité en pourcentage.
        """
        score = 0
        for i in range(len(chemin) - 1):
            if self.graph.has_edge(chemin[i], chemin[i+1]):
                poids = self.graph[chemin[i]][chemin[i+1]]["weight"]
                score += poids
        
        # Calculer la probabilité en pourcentage
        probability = (score / self.max_score) * 100
        probability = min(probability, 100.0)  # S'assurer que la probabilité ne dépasse pas 100%

        alerte = "Alerte critique" if score >= 5 else "Sous surveillance"
        return {"score": score, "alerte": alerte, "probability": round(probability, 2)}

    def exporter_graphe(self):
        """Retourne le graphe pour visualisation externe (NetworkX)."""
        return self.graph