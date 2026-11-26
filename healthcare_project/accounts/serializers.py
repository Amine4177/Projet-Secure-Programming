from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DoctorProfile, PatientProfile

User = get_user_model()


class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "username",
            "birth_date",
            "social_security_number",
            "blood_type",
            "allergies",
            "medical_history",
        ]


class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ["id", "username", "specialty", "license_number"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

    # Champs specifiques patient (optionnels si role = doctor)
    birth_date = serializers.DateField(required=False, allow_null=True)
    social_security_number = serializers.CharField(required=False, allow_blank=True)
    blood_type = serializers.CharField(required=False, allow_blank=True)
    allergies = serializers.CharField(required=False, allow_blank=True)
    medical_history = serializers.CharField(required=False, allow_blank=True)

    # Champs specifiques docteur (optionnels si role = patient)
    specialty = serializers.CharField(required=False, allow_blank=True)
    license_number = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe deja.")
        return value

    def create(self, validated_data):
        role = validated_data["role"]
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
            role=role,
        )

        if role == User.Role.PATIENT:
            PatientProfile.objects.create(
                user=user,
                birth_date=validated_data.get("birth_date"),
                social_security_number=validated_data.get("social_security_number", ""),
                blood_type=validated_data.get("blood_type", ""),
                allergies=validated_data.get("allergies", ""),
                medical_history=validated_data.get("medical_history", ""),
            )
        else:
            DoctorProfile.objects.create(
                user=user,
                specialty=validated_data.get("specialty", ""),
                license_number=validated_data.get("license_number", ""),
            )

        return user
