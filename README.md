# TrainBot — Coach IA emlyon × Brico Dépôt

Chatbot pédagogique RAG pour les apprenants du parcours La Toile.

---

## Stack

- **Backend** : FastAPI + Python + Anthropic SDK → Railway
- **Frontend** : HTML/CSS/JS Vanilla → Netlify

---

## Déploiement Railway (backend) — ~15 min

### 1. Crée un repo GitHub

```bash
git init trainbot-backend
cd trainbot-backend
cp /chemin/vers/main.py .
cp /chemin/vers/requirements.txt .
cp /chemin/vers/Procfile .
git add .
git commit -m "init trainbot backend"
git remote add origin https://github.com/raymondgadji/trainbot-backend.git
git push -u origin main
```

### 2. Railway

1. Va sur [railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo → sélectionne `trainbot-backend`
3. Variables d'environnement → ajoute :
   - `ANTHROPIC_API_KEY` = ta clé Anthropic
4. Deploy → attends 2-3 minutes
5. Settings → Networking → Generate Domain
6. Copie l'URL : `https://trainbot-backend-xxxxx.up.railway.app`

---

## Déploiement Netlify (frontend) — ~5 min

### 1. Mets à jour l'URL dans index.html

Ligne ~220 dans `index.html` :
```js
const API_BASE = "https://TON-SERVICE.up.railway.app";
```
→ Remplace par ton URL Railway réelle.

### 2. Netlify

1. Va sur [netlify.com](https://netlify.com)
2. Drag & drop le dossier `frontend/` dans Netlify
3. URL générée automatiquement ex: `https://trainbot-emlyon.netlify.app`
4. (Optionnel) Domain settings → Custom domain

---

## Les 4 scénarios

| ID | Scénario | Description |
|----|----------|-------------|
| 0 | Simuler une vente | Jeu de rôle client/conseiller |
| 1 | Étude de cas RNCP | Prépa certification avec feedback /10 |
| 2 | Prise de congé | Fin d'interaction et fidélisation |
| 3 | Mes indicateurs | Quiz KPIs retail (CA, panier moyen, NPS) |

---

## Structure du projet

```
trainbot/
├── backend/
│   ├── main.py           # FastAPI app + proxy Claude API
│   ├── requirements.txt  # Dépendances Python
│   └── Procfile          # Config Railway
└── frontend/
    └── index.html        # App complète (HTML/CSS/JS)
```

---

## Variables d'environnement requises

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Clé API Anthropic (railway) |
| `PORT` | Fourni automatiquement par Railway |

---

## Évolutions V1 (post-appel d'offre)

- RAG réel sur documents RNCP + fiches produits Brico Dépôt
- Authentification apprenant (login)
- Tableau de bord formateur (progression, scores)
- Analytics Umami
- Nouveaux scénarios (gestion conflits, vente additionnelle...)
