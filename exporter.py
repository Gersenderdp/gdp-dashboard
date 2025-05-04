import json
import os

def export_signaux_to_json(nom_fichier_source, alertes, dossier_export="exports"):
    os.makedirs(dossier_export, exist_ok=True)
    export = {
        "fichier_source": nom_fichier_source,
        "nb_signaux_detectes": len(alertes),
        "signaux": alertes
    }

    export_path = os.path.join(dossier_export, nom_fichier_source + "_truthx.json")
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=4)

    return export_path
