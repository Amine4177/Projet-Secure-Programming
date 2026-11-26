from django.contrib import admin

from .models import DoctorProfile, PatientProfile, User

admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
