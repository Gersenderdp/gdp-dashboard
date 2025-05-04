from io import BytesIO
from PIL import Image, ImageDraw

def generer_png_en_memoire(contenu, alertes):
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((10, 10), "Rapport PNG – TruthX", fill=(0, 0, 0))

    y = 50
    draw.text((10, y), "🧠 Texte analysé :", fill=(0, 0, 0))
    y += 20
    draw.text((10, y), contenu[:1000].encode('latin-1', 'replace').decode('latin-1'), fill=(0, 0, 0))

    y += 100
    if alertes:
        draw.text((10, y), "🔴 Signaux détectés :", fill=(255, 0, 0))
        y += 20
        for label, code in alertes:
            draw.text((10, y), f"– {label} ({code})", fill=(255, 0, 0))
            y += 20
    else:
        draw.text((10, y), "✅ Aucun signal détecté", fill=(0, 128, 0))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


DETECTEURS = [
    ("tu es folle", "Disqualification mentale", "Article 222-33-2-2"),
    ("plus de nouvelles", "Culpabilisation affective", "Article 222-33-2-2"),
    ("tout est de ta faute", "Renversement de culpabilité", "Article 222-33-2-2"),
    ("tu n’as personne d’autre", "Isolement social", "Article 222-33-2-2"),
    ("je vais me suicider", "Menace suicidaire", "Mise en danger d'autrui"),
    ("c’est pour ton bien", "Justification de domination", "Article 222-33-2-2"),
    ("je suis la seule personne qui t’aime", "Monopole affectif", "Tentative d’isolement"),
]


