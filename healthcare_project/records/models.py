from django.db import models

from accounts.models import DoctorProfile, PatientProfile


class Evaluation(models.Model):
    """
    Evaluation / consultation realisee par un docteur pour un patient.
    Donnee tres sensible : diagnostic et notes medicales confidentielles.
    """

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="evaluations")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="evaluations")
    date = models.DateTimeField(auto_now_add=True)
    diagnostic = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    treatment = models.TextField(blank=True)

    def __str__(self):
        return f"Evaluation #{self.id} - {self.patient} par {self.doctor}"
