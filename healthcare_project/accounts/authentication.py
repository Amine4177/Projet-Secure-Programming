"""
Classe d'authentification DRF "Red Team" : authentification par JWT bearer simple.

Elle lit l'en-tete `Authorization: Bearer <token>`, verifie uniquement la
signature et l'expiration du JWT, puis authentifie l'utilisateur correspondant
a `user_id`. Aucune autre verification n'est faite (pas de binding de cle,
pas de verification d'IP/device, pas de liste de revocation).

C'est volontairement la partie la plus faible de l'application : n'importe
quel client possedant un JWT valide (vole ou non) est traite comme le
proprietaire legitime du compte.
"""

import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .jwt_utils import decode_access_token

User = get_user_model()


class VulnerableJWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]

        try:
            payload = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expire.")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token invalide.")

        try:
            user = User.objects.get(id=payload.get("user_id"))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Utilisateur introuvable.")

        # Pas de verification supplementaire ici (volontaire) :
        # ni l'IP, ni le user-agent, ni une empreinte de device ne sont
        # comparees. Le token seul suffit, d'ou la vulnerabilite au vol/rejeu.
        return (user, token)

    def authenticate_header(self, request):
        return self.keyword
