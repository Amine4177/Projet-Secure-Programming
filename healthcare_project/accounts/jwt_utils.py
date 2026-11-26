"""
Generation et decodage des JWT.

ATTENTION - CECI EST LA VERSION "RED TEAM" / VULNERABLE DU PROJET.
Objectif pedagogique : ce module cree volontairement un JWT "bearer" classique,
sans aucune protection contre le vol/rejeu :

- Pas de liaison a un device ou a une cle client (pas de DPoP, pas de cnf.jkt).
- Duree de vie longue (24h) : un token vole reste utilisable longtemps.
- Aucune verification d'origine, d'IP ou de user-agent.
- Aucune revocation possible (pas de table de tokens, pas de jti blacklist).

=> Si un attaquant recupere ce token (reseau, XSS, log, etc.), il peut
   l'utiliser depuis n'importe quelle machine, exactement comme le compte
   proprietaire, tant que le token n'a pas expire.

La version Blue Team (faite par un autre membre de l'equipe) remplacera ce
module par un systeme DPoP (RFC 9449) qui lie le token a une cle publique
ECDSA P-256 detenue par le client.
"""

import datetime

import jwt
from django.conf import settings

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24  # volontairement long pour la demo de vol de token


def generate_access_token(user) -> str:
    """Cree un JWT bearer simple pour l'utilisateur donne."""
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "iat": now,
        "exp": now + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    """
    Decode et verifie uniquement la signature et l'expiration du token.
    Volontairement minimaliste : pas de verification d'audience, d'issuer,
    de device, d'IP ... C'est exactement cette absence de controle que le
    Red Team va exploiter.
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
