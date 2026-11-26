from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur de l'application.
    Le role determine si l'utilisateur possede un PatientProfile ou un DoctorProfile.
    """

    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"

    role = models.CharField(max_length=10, choices=Role.choices)

    def __str__(self):
        return f"{self.username} ({self.role})"


class PatientProfile(models.Model):
    """
    Donnees personnelles et medicales critiques d'un patient.
    C'est ce type de donnee que le JWT "vole" permettra d'exposer
    si l'attaque Red Team reussit.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    birth_date = models.DateField(null=True, blank=True)
    social_security_number = models.CharField(max_length=30, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"


class DoctorProfile(models.Model):
    """Informations professionnelles d'un medecin."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialty})"
