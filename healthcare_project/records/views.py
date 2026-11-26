from rest_framework import permissions, viewsets

from .models import Evaluation
from .serializers import EvaluationSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les evaluations medicales. Comme pour PatientViewSet, la seule
    protection active est VulnerableJWTAuthentication : un JWT vole donne
    acces complet aux notes medicales confidentielles de n'importe quel
    patient. C'est le coeur de la demonstration Red Team.
    """

    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
