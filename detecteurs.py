# detecteurs.py

DETECTEURS = [
    {
        "label": "Culpabilisation affective",
        "motifs": [
            "plus de nouvelles",
            "tu m'as abandonné",
            "c’est toujours moi qui fais le premier pas",
            "je suis blessé que tu ne répondes pas"
        ],
        "code": "Article 222-33-2-2"
    },
    {
        "label": "Fusion affective / brouillage émotionnel",
        "motifs": [
            "je t’embrasse fort",
            "tu es tout pour moi",
            "on est liés à jamais",
            "tu es ma moitié"
        ],
        "code": "Signal psychologique"
    },
    {
        "label": "Pression implicite",
        "motifs": [
            "tu ne veux plus me parler",
            "je fais tout pour toi",
            "tu me laisses seul avec ça",
            "si tu m’aimais vraiment"
        ],
        "code": "Tentative de contrôle"
    },
    {
        "label": "Dévalorisation cachée",
        "motifs": [
            "tu te fais des films",
            "tu dramatises tout",
            "t’es trop sensible",
            "t’as encore mal compris"
        ],
        "code": "Gaslighting - Article 222-33-2-2"
    },
    {
        "label": "Menace voilée",
        "motifs": [
            "tu verras ce que ça fait",
            "je vais devoir me protéger",
            "tu sais de quoi je suis capable",
            "tu vas le regretter"
        ],
        "code": "Signal d’alerte rouge"
    }
]
DETECTEURS = [
    {"label": "Gaslighting", "pattern": r"(tu es folle|tu te fais des films|c’est dans ta tête)", "code": "GAS"},
    {"label": "Déresponsabilisation", "pattern": r"(je ne suis pas responsable de tes émotions)", "code": "DERESP"},
    {"label": "Renversement de culpabilité", "pattern": r"(c’est toi qui|comme d’habitude)", "code": "CULP"},
    # à compléter avec d'autres...
]
DETECTEURS = [
    {
        "code": "GAS001",
        "categorie": "Gaslighting",
        "label": "Tu es folle / C’est dans ta tête",
        "definition": "L’auteur fait douter la victime de sa perception de la réalité, en minimisant ou niant les faits.",
        "exemple": "Tu te fais des films, comme d’habitude.",
        "pattern": r"(tu es folle|tu te fais des films|c’est dans ta tête|tu vois bien que|comme d’habitude)"
    },
    {
        "code": "DER001",
        "categorie": "Déresponsabilisation",
        "label": "Refus de responsabilité émotionnelle",
        "definition": "L’auteur nie sa responsabilité dans les émotions qu’il provoque chez l’autre.",
        "exemple": "Je ne suis pas responsable de tes émotions.",
        "pattern": r"(je ne suis pas responsable de tes émotions|je n’y peux rien|c’est toi qui réagis mal)"
    },
    {
        "code": "CULP001",
        "categorie": "Culpabilisation",
        "label": "Tu provoques les conflits",
        "definition": "La victime est rendue responsable des tensions ou violences, comme si elle les avait déclenchées volontairement.",
        "exemple": "Tu me pousses à bout, tu cherches toujours les problèmes.",
        "pattern": r"(tu me pousses à bout|tu provoques toujours les conflits|c’est toi qui as commencé)"
    },
    {
        "code": "MIN001",
        "categorie": "Minimisation",
        "label": "Tu exagères / Ce n’est rien",
        "definition": "L’auteur minimise les faits ou les conséquences pour invalider la réaction de la victime.",
        "exemple": "C’est rien du tout, tu exagères encore une fois.",
        "pattern": r"(c’est rien du tout|tu exagères|tu dramatises toujours)"
    },
    {
        "code": "SIL001",
        "categorie": "Silence punitif",
        "label": "Je ne te parle plus",
        "definition": "Refus délibéré de communication pour punir ou contrôler l’autre.",
        "exemple": "Je ne vais pas te parler, tu ne mérites pas de réponse.",
        "pattern": r"(je ne vais pas te parler|tu ne mérites pas de réponse|tu n’as qu’à réfléchir)"
    },
    {
        "code": "THR001",
        "categorie": "Menace",
        "label": "Tu verras ce qui va t’arriver",
        "definition": "L’auteur utilise la peur pour contrôler ou faire taire la victime.",
        "exemple": "Si tu parles, tu vas le regretter.",
        "pattern": r"(si tu dis ça à quelqu’un|tu verras ce qui va t’arriver|je te préviens)"
    },
    {
        "code": "CTRL001",
        "categorie": "Contrôle affectif",
        "label": "Tu n’as que moi",
        "definition": "L’auteur isole la victime en lui faisant croire qu’elle ne mérite pas d’être aimée par d’autres.",
        "exemple": "Tu ne trouveras jamais mieux que moi.",
        "pattern": r"(tu ne trouveras jamais mieux|tu es rien sans moi|tu devrais me remercier)"
    },
    {
        "code": "INV001",
        "categorie": "Justification inversée",
        "label": "C’est à cause de toi",
        "definition": "L’auteur inverse les responsabilités en justifiant ses actes violents par les comportements supposés de la victime.",
        "exemple": "Si je crie, c’est parce que tu m’énerves.",
        "pattern": r"(je t’aime mais tu me rends fou|si je crie, c’est parce que tu m’énerves|tu me forces à faire ça)"
    }
]
DETECTEURS = [
    {
        "code": "GAS001",
        "categorie": "Manipulation cognitive",
        "label": "Gaslighting — Doute sur la réalité",
        "definition": "Faire douter la victime de sa mémoire, de son ressenti ou de sa perception des faits.",
        "exemple": "Tu te fais des films, comme d’habitude.",
        "pattern": r"(tu es folle|tu te fais des films|c’est dans ta tête|tu vois bien que|comme d’habitude)",
        "intensite": "moyen"
    },
    {
        "code": "CULP001",
        "categorie": "Culpabilisation",
        "label": "Renversement de responsabilité",
        "definition": "Faire croire à la victime qu’elle est responsable des comportements violents de l’auteur.",
        "exemple": "Tu me pousses à bout, c’est toi qui me rends comme ça.",
        "pattern": r"(tu me pousses à bout|tu provoques toujours les conflits|c’est toi qui as commencé)",
        "intensite": "grave"
    },
    {
        "code": "DER001",
        "categorie": "Déni de responsabilité",
        "label": "Refus de responsabilité émotionnelle",
        "definition": "L’auteur nie l’impact de ses actes sur les émotions de la victime.",
        "exemple": "Je ne suis pas responsable de tes émotions.",
        "pattern": r"(je ne suis pas responsable de tes émotions|je n’y peux rien|c’est toi qui réagis mal)",
        "intensite": "moyen"
    },
    {
        "code": "MIN001",
        "categorie": "Minimisation",
        "label": "Invalidation de la souffrance",
        "definition": "Minimiser les faits pour délégitimer la réaction ou la douleur de la victime.",
        "exemple": "C’est rien du tout, tu dramatises encore.",
        "pattern": r"(c’est rien du tout|tu exagères|tu dramatises toujours)",
        "intensite": "faible"
    },
    {
        "code": "SIL001",
        "categorie": "Contrôle psychologique",
        "label": "Silence punitif",
        "definition": "Refus délibéré de communication comme stratégie de punition ou de pression psychique.",
        "exemple": "Je ne vais pas te parler, tu n’as qu’à réfléchir.",
        "pattern": r"(je ne vais pas te parler|tu ne mérites pas de réponse|tu n’as qu’à réfléchir)",
        "intensite": "moyen"
    },
    {
        "code": "THR001",
        "categorie": "Violence verbale / Menace",
        "label": "Menace explicite ou implicite",
        "definition": "Proférer des menaces directes ou voilées pour imposer la peur.",
        "exemple": "Si tu en parles, tu vas le regretter.",
        "pattern": r"(si tu dis ça à quelqu’un|tu verras ce qui va t’arriver|je te préviens)",
        "intensite": "grave"
    },
    {
        "code": "CTRL001",
        "categorie": "Isolement affectif",
        "label": "Dévalorisation et dépendance",
        "definition": "Faire croire à la victime qu’elle est incapable ou indigne sans l’auteur.",
        "exemple": "Tu ne trouveras jamais mieux que moi.",
        "pattern": r"(tu ne trouveras jamais mieux|tu es rien sans moi|tu devrais me remercier)",
        "intensite": "grave"
    },
    {
        "code": "INV001",
        "categorie": "Inversion de logique",
        "label": "Justification de la violence",
        "definition": "L’auteur justifie ses actes par un comportement supposé de la victime.",
        "exemple": "Si je crie, c’est parce que tu m’énerves.",
        "pattern": r"(je t’aime mais tu me rends fou|si je crie, c’est parce que tu m’énerves|tu me forces à faire ça)",
        "intensite": "grave"
    }
]
