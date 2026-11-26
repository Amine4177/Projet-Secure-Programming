from rest_framework import serializers

from .models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source="patient.user.username", read_only=True)
    doctor_username = serializers.CharField(source="doctor.user.username", read_only=True)

    class Meta:
        model = Evaluation
        fields = [
            "id",
            "patient",
            "patient_username",
            "doctor",
            "doctor_username",
            "date",
            "diagnostic",
            "notes",
            "treatment",
        ]
        read_only_fields = ["date"]
