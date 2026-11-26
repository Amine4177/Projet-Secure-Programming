# Project 19 — Red Team — Partie 2 : Simulation de Phishing

Clone visuel de la page de connexion officielle (`healthcare_project`),
servi depuis un **port différent** (simulation d'une origine/domaine
différent), qui capture les identifiants tapés par la victime avant de la
rediriger vers le vrai site.

Ce projet est **totalement indépendant** de `healthcare_project` : aucun
modèle ni aucune URL en commun. Il ne contient aucune base de données
utilisée (pas de modèles) — `python manage.py runserver` suffit, pas besoin
de `migrate`.

⚠️ Usage strictement local et pédagogique, avec des comptes synthétiques
créés exprès pour la démo. Ne jamais héberger ceci publiquement ni
l'utiliser contre de vraies personnes.

## Scénario simulé

1. La victime arrive sur `http://localhost:9000/` (le faux site), au lieu de
   `http://localhost:8000/login/` (le vrai).
2. La page est visuellement identique (même CSS, même logo "MediTrust").
3. Elle tape son nom d'utilisateur et son mot de passe, clique "Se connecter".
4. Le serveur du faux site **enregistre** ces identifiants en clair dans
   `stolen_credentials.log`.
5. Il redirige ensuite la victime vers `http://localhost:8000/login/` (le
   vrai site), où elle devra se reconnecter — dans cette version "simple"
   du phishing (capture puis redirection), c'est le compromis assumé pour
   rester facile à construire.

> Variante plus avancée (non implémentée ici) : un "relais transparent"
> façon Evilginx relaierait immédiatement les identifiants volés vers la
> vraie API pour authentifier la victime sans qu'elle ait à se reconnecter.
> Cette version est plus difficile à détecter, mais plus complexe à coder.
> Les deux variantes sont bloquées de la même façon par WebAuthn/Passkeys,
> car la vérification d'origine se fait côté navigateur, indépendamment de
> ce que fait le serveur derrière la fausse page.

## Installation et lancement

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py runserver 9000
```

Le vrai site (`healthcare_project`) doit tourner en parallèle sur le port
8000 pour que la redirection finale ait un sens (sinon elle pointera vers
un site indisponible, ce qui n'empêche pas de voir le vol fonctionner).

## Déroulé de la démo / vidéo

1. Démarrer `healthcare_project` sur le port 8000 (`python manage.py runserver`).
2. Démarrer ce projet sur le port 9000 (`python manage.py runserver 9000`).
3. Ouvrir `http://localhost:9000/` dans un navigateur — montrer que ça
   ressemble exactement à `http://localhost:8000/login/`, mais avec une URL
   différente.
4. Se connecter avec un compte patient existant (ex: `alice`).
5. Montrer qu'on est redirigé vers le vrai `/login/` (la victime pense
   avoir fait une erreur de frappe).
6. Ouvrir `stolen_credentials.log` et montrer que le mot de passe y est
   enregistré en clair.
7. (Optionnel, lien avec la partie 1) Utiliser ces identifiants volés pour
   se connecter réellement sur le vrai site et récupérer un JWT — montrant
   que le vol de mot de passe mène directement au vol de session.

## Où se branchera la défense Blue Team (WebAuthn/Passkeys)

Le futur login WebAuthn du vrai site appellera
`navigator.credentials.get()` dans le navigateur. Le navigateur refusera de
fournir la passkey si le domaine affiché ne correspond pas à celui
enregistré lors de l'inscription (RP ID) — donc même un clone pixel-perfect
de cette page, à cet endroit précis, ne pourra jamais obtenir de passkey
valide. C'est ce qu'il faudra démontrer dans la vidéo "après" : la même
page clonée, mais où la tentative de connexion WebAuthn échoue
silencieusement côté navigateur.

## Structure

```
phishing_site/
├── manage.py
├── config/            # settings, urls (projet Django minimal)
├── fake_login/        # vue qui capture + redirige
├── templates/fake_login.html   # clone visuel du vrai /login/
└── static/css/site.css         # copie du CSS du vrai site
```

## Branche Git recommandée

`red-team/phishing-clone`, créée à partir de `main`, indépendante du travail
du Blue Team sur `healthcare_project`.
