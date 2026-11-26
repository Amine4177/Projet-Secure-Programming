# Project 19 — Healthcare App — Partie Red Team (JWT vulnérable)

Cette partie met en place :
- L'application Django "MediTrust" (patients, docteurs, évaluations médicales).
- Les API CRUD (Django REST Framework).
- Un login/register avec JWT **volontairement vulnérable** (bearer simple,
  non lié au client, longue durée de vie, sans révocation).
- Les pages web (templates Django, pas de framework front) : `/login/`,
  `/register/`, `/dashboard/`.
- Un script de démonstration du vol/rejeu de token (`red_team/replay_simulator.py`).

## Pourquoi c'est vulnérable (volontairement)

| Fichier | Ce qui est volontairement faible |
|---|---|
| `accounts/jwt_utils.py` | JWT HS256 simple, 24h de validité, aucune liaison à un device/clé client |
| `accounts/authentication.py` | Vérifie seulement la signature + l'expiration, aucune vérification d'IP/device/révocation |
| `templates/login.html` | Stocke le JWT dans `localStorage` (accessible en JS, donc vulnérable XSS) |

👉 La partie Blue Team remplacera ces éléments par WebAuthn/Passkeys + DPoP
(RFC 9449) + révocation de famille de refresh tokens, **sans changer les
modèles métier** (`accounts/models.py`, `records/models.py`).

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\Activate.ps1
pip install -r requirements.txt

cp .env.example .env            # puis éditez les valeurs si besoin

python manage.py migrate
python manage.py createsuperuser   # optionnel, pour /admin/
python manage.py runserver
```

Ouvrir :
- Site web : http://localhost:8000/register/ puis http://localhost:8000/login/
- API (ex.) : http://localhost:8000/api/patients/
- Admin Django : http://localhost:8000/admin/

## Démonstration de la faille (Red Team)

### 1. Créer un compte patient et se connecter
Via le site (`/register/` puis `/login/`), ou directement en API :

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"Password123!","role":"patient","blood_type":"O+","allergies":"Pollen","medical_history":"Asthme"}'

curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"Password123!"}'
```

La réponse contient un `access_token` (JWT).

### 2. Simuler le vol + le rejeu du token

Avec le script fourni :

```bash
python red_team/replay_simulator.py --username alice --password Password123!
```

Ou, si vous avez récupéré un token autrement (ex. copié depuis `localStorage`
dans les DevTools du navigateur, ou intercepté sur le réseau) :

```bash
python red_team/replay_simulator.py --token "<le_token_vole>"
```

### 3. Vérifier avec Postman

- Nouvelle requête `GET http://localhost:8000/api/patients/`
- Onglet **Headers** : `Authorization: Bearer <token_vole>`
- Résultat attendu : **200 OK** avec les données de *tous* les patients
  (y compris leurs données médicales), **sans jamais avoir fourni le mot de
  passe**, et même depuis une machine/un client totalement différent de
  celui qui s'est connecté.

C'est exactement la preuve de vulnérabilité que la partie Red Team doit
démontrer : un bearer JWT simple n'est pas "lié" à qui l'utilise.

## Structure du projet

```
healthcare_project/
├── accounts/      # User, PatientProfile, DoctorProfile, JWT, login/register
├── records/       # Evaluation (consultations confidentielles)
├── frontend/      # Pages Django (templates) : login, register, dashboard
├── red_team/      # Simulateur de vol/rejeu de JWT
├── templates/      # login.html, register.html, dashboard.html, base.html
├── static/css/     # style du site officiel
└── config/         # settings, urls du projet Django
```

## Pour la suite (phase 2 — toujours Red Team)

La prochaine étape (phishing) créera un **clone visuel de `/login/`** servi
sur un autre domaine/port, qui capture les identifiants avant de rediriger
vers le vrai site. Elle n'a pas encore été ajoutée dans ce livrable pour ne
pas mélanger les deux démonstrations ; elle réutilisera le même
`static/css/site.css` pour que le clone soit visuellement identique.

## Pour la partie Blue Team (autres membres de l'équipe)

Partez de `main` (après merge de cette branche). Les modèles
(`PatientProfile`, `DoctorProfile`, `Evaluation`) ne doivent pas changer de
structure métier — seule la couche d'authentification/autorisation doit être
renforcée :
- Remplacer `VulnerableJWTAuthentication` par une vérification DPoP (RFC 9449).
- Ajouter WebAuthn/Passkeys (`py_webauthn`) pour le login.
- Ajouter le modèle `RefreshToken` (token_id, family_id, user, token_hash,
  expires_at, revoked, replaced_by) et la logique de révocation de famille.
