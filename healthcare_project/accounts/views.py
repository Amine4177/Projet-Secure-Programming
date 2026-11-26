from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .jwt_utils import generate_access_token
from .models import DoctorProfile, PatientProfile
from .serializers import (
    DoctorProfileSerializer,
    PatientProfileSerializer,
    RegisterSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """Inscription publique : cree un User + son profil (patient ou docteur)."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Compte cree.", "username": user.username, "role": user.role},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Authentifie l'utilisateur avec username/password puis renvoie un JWT bearer
    "Red Team" : simple, non lie au client, longue duree de vie.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_access_token(user)
        return Response(
            {
                "access_token": token,
                "token_type": "Bearer",
                "role": user.role,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )


class PatientViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les dossiers patients.
    Protege uniquement par VulnerableJWTAuthentication (voir settings.py) :
    toute personne presentant un JWT valide - vole ou non - peut lire/modifier
    n'importe quel dossier patient. C'est exactement la faille que la demo
    Red Team doit mettre en evidence.
    """

    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
