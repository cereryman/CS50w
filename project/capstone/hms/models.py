from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

class User(AbstractUser):
    pass

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    BLOOD_TYPES = [
        ('APOS', 'A+'),
        ('ANEG', 'A-'),
        ('BPOS', 'B+'),
        ('BNEG', 'B-'),
        ('OPOS', 'O+'),
        ('ONEG', 'O-'),
        ('ABPOS', 'AB+'),
        ('ABNEG', 'AB-'),
        ('UNKNOWN', 'Unknown')
    ]
    first_name = models.CharField(max_length=200, blank=True, default='N/A')
    last_name = models.CharField(max_length=200, blank=True, default='N/A')
    gender = models.CharField(max_length=100, null=True, blank=True, default='Other', choices=GENDER_CHOICES)
    address = models.CharField(max_length=400, blank=True, default='N/A')
    birth_date = models.DateField(null=True, blank=True, default='N/A')
    phone = models.CharField(max_length=200, blank=True, default='N/A')
    email = models.CharField(max_length=200, blank=True, default='N/A')
    avatar = models.ImageField(null=True, blank=True)
    height_cm = models.DecimalField(default="0.00", decimal_places=2, max_digits=5, blank=True, null=True)
    weight_kg = models.DecimalField(default="0.00", decimal_places=2, max_digits=50, blank=True, null=True)
    blood_type = models.CharField(max_length=100, null=True, default="Unknown", choices=BLOOD_TYPES)
    contact_name = models.CharField(max_length=200, blank=True, default='N/A')
    contact_relationship = models.CharField(max_length=200, blank=True, default='N/A')
    contact_phone = models.CharField(max_length=200, blank=True, default='N/A')
    contact_email = models.CharField(max_length=200, blank=True, default='N/A')
    insurance_policy_provider = models.CharField(max_length=200, blank=True, default='N/A')
    insurance_policy_number = models.CharField(max_length=200, blank=True, default='N/A')
    bed_location = models.CharField(max_length=200, blank=True, default='N/A')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def age(self):
        if not self.birth_date:
            return 0
        else:
            return (datetime.date.today().year - self.birth_date.year)

    def gender_full(self):
        return self.get_gender_display()

    def blood_type_full(self):
        return self.get_blood_type_display()

class Record(models.Model):
    VITALS_CHOICES = [
        ('SYS_BP', 'Systolic Blood Pressure'),
        ('DIA_BP', 'Diastolic Blood Pressure'),
        ('HR', 'Heart Rate'),
        ('BT', 'Body Temperature'),
        ('RR', 'Respiratory Rate')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="record_patient", null=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name="record_nurse", null=True)
    vital = models.CharField(max_length=100, choices=VITALS_CHOICES, null=True)
    value = models.DecimalField(default="0.00", decimal_places=2, max_digits=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}, {}, {} of {}\n".format(self.timestamp, self.patient, self.vital,self.value)

class Allergy(models.Model):
    CATEGORY_CHOICES = [
        ('SFX', 'Side Effect'),
        ('ALGY', 'Allergy')
    ]
    SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="allergy_patient", null=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allergy_nurse", null=True)
    allergy = models.CharField(max_length=200, blank=True)
    reaction = models.TextField(blank=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=100, null=True, choices=SEVERITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def display_category(self):
        return self.get_category_display()

    def display_severity(self):
        return self.get_severity_display()

class Log(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="log_patient", null=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name="log_nurse", null=True)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Hospitalization(models.Model):
    STATUS_CHOICES = [
        ('CHECKIN', 'Check-in'),
        ('CHECKOUT', 'Check-out')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="hospitalization_patient", null=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hospitalization_nurse", null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s on %s' % (self.status, self.timestamp)