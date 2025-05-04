from dotenv import load_dotenv
import os


# 🔍 Analyse de la tonalité psychologique
def analyse_tonalite(message):
    prompt = f"""
Analyse la tonalité de ce message et réponds uniquement par un JSON avec les champs :
- "tonalite" : neutre, culpabilisant, moqueur, passif-agressif, menaçant, etc.
- "confiance" : un score entre 0 et 1

Message : "{message}"
"""
    response = client.chat.completions.create(
        model="gpt-4o",  # ✅ modèle disponible sur ton compte
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# ⚠️ Détection d’ambiguïtés ou chantages implicites
def detecte_ambiguites(message):
    prompt = f"""
Ce message contient-il une ambiguïté, une menace implicite, un chantage émotionnel ?
Message : "{message}"

Réponds uniquement par un JSON avec les champs :
- "ambiguite" : oui/non
- "type" : s’il y en a
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# 📝 Résumé conversation (max 2 phrases)
def resume_conversation(messages):
    joint = "\n".join(messages)
    prompt = f"""
Voici une conversation entre deux personnes. Résume-la en 2 phrases maximum :
Conversation :
{joint}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
