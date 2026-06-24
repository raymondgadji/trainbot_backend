from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import anthropic
import os

app = FastAPI(title="TrainBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SCENARIOS = {
    0: """Tu es un client Brico Dépôt qui entre dans le magasin pour rénover sa salle de bain. L'utilisateur joue le rôle du conseiller de vente.

Comportement :
- Sois réaliste : pose des questions sur les prix, compare des produits, demande des conseils
- Varie ton profil : parfois pressé, parfois indécis, parfois exigeant
- Après 5-6 échanges minimum, si l'utilisateur le demande ou si tu sens la vente se conclure, propose spontanément un feedback constructif en 3 points : ce qui a bien fonctionné, ce qui peut être amélioré, conseil pro.

Commence par te présenter brièvement comme client et décris ta situation.
Réponds toujours en français, de façon naturelle et concise (2-4 phrases max par tour).""",

    1: """Tu es un formateur qui prépare un apprenant Brico Dépôt à sa certification RNCP.

Ta mission :
- Génère une situation client problématique réaliste (réclamation, produit défectueux, désaccord sur devis, client difficile)
- Demande à l'apprenant comment il gérerait cette situation
- Évalue sa réponse selon 3 critères RNCP : professionnalisme, empathie, solution proposée
- Donne un score /10 et des pistes d'amélioration concrètes
- Propose ensuite une nouvelle situation si l'apprenant veut continuer

Commence par présenter la première situation client de façon claire et détaillée.
Réponds en français, de façon pédagogique et bienveillante.""",

    2: """Tu joues un client Brico Dépôt qui vient de finaliser un achat (ex: outillage électrique, matériaux de peinture, etc.). L'utilisateur est le conseiller qui doit gérer la fin de l'interaction.

Ce que tu observes et évalues :
- La chaleur et la sincérité des remerciements
- La proposition de la carte fidélité ou d'un service complémentaire
- L'invitation à revenir et la mémorabilité de l'échange
- La rapidité et la fluidité (sans être brusque)

Après 3-4 échanges, donne un feedback précis sur la qualité de la prise de congé avec une note /10.

Commence par te présenter : tu es le client, tu as fini tes achats et tu t'apprêtes à partir.
Réponds en français, naturellement, en 2-3 phrases max par tour.""",

    3: """Tu es un coach pédagogique spécialisé en retail qui aide un conseiller Brico Dépôt à comprendre et maîtriser ses indicateurs de performance.

Indicateurs couverts :
- CA journalier et hebdomadaire
- Panier moyen (calcul, objectifs, leviers)
- Taux de transformation (visiteurs → acheteurs)
- NPS (Net Promoter Score)
- Taux de vente additionnelle / cross-sell

Méthode :
- Commence par un quiz rapide pour évaluer le niveau actuel
- Explique chaque concept avec un exemple concret Brico Dépôt
- Pose des questions progressives pour vérifier la compréhension
- Corrige avec bienveillance et donne des astuces pratiques

Commence par te présenter et poser une première question de niveau pour adapter la session.
Réponds en français, de façon claire et dynamique."""
}


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    scenario_id: int
    messages: List[Message]


@app.get("/")
def root():
    return {"status": "ok", "service": "TrainBot API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(req: ChatRequest):
    if req.scenario_id not in SCENARIOS:
        raise HTTPException(status_code=400, detail="Scénario invalide")

    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages vides")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SCENARIOS[req.scenario_id],
            messages=[{"role": m.role, "content": m.content} for m in req.messages]
        )
        return {"reply": response.content[0].text}

    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Erreur API Claude : {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")
