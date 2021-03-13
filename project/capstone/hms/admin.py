from django.contrib import admin
from .models import User, Patient, Record, Allergy, Log, Hospitalization

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(Allergy)
admin.site.register(Log)
admin.site.register(Hospitalization)