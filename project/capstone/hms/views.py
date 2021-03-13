from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator # Needed to split posts
from django import forms # Needed for django built-in forms
from django.contrib.auth.decorators import login_required # Needed for login only views
from django.views.decorators.csrf import csrf_exempt # Needed for JSON put requests
import json # Need for JSON dumps
import decimal # Used for JSON encoder
from .models import User, Patient, Record, Allergy, Log, Hospitalization

# Form to create a new patient
class NewPatientForm(forms.Form):
    first_name = forms.CharField(max_length=200, label="First Name")
    last_name = forms.CharField(max_length=200, label="Last Name")
    gender = forms.CharField(max_length=100, widget=forms.Select(choices=Patient.GENDER_CHOICES), label="Gender")
    address = forms.CharField(max_length=400, label="Home Address", required=False)
    birth_date = forms.DateField(required=False, label="Date of Birth")
    phone = forms.CharField(max_length=200, label="Phone Number", required=False)
    email = forms.CharField(max_length=200, label="E-mail Address", required=False)
    avatar = forms.ImageField(label="Avatar", required=False)
    height_cm = forms.DecimalField(max_digits=50, label="Height (in cm)")
    weight_kg = forms.DecimalField(max_digits=50, label="Weight (in kg)")
    blood_type = forms.CharField(max_length=100, widget=forms.Select(choices=Patient.BLOOD_TYPES), label="Blood Type")
    contact_name = forms.CharField(max_length=200, label="Secondary Contact - Name", required=False)
    contact_relationship = forms.CharField(max_length=200, label="Secondary Contact - Relationship to Patient", required=False)
    contact_phone = forms.CharField(max_length=200, label="Secondary Contact - Phone Number", required=False)
    contact_email = forms.CharField(max_length=200, label="Secondary Contact - E-mail Address", required=False)
    insurance_policy_provider = forms.CharField(max_length=200, label="Insurance Policy Provider", required=False)
    insurance_policy_number = forms.CharField(max_length=200, label="Insurance Policy Number", required=False)
    bed_location = forms.CharField(max_length=200, label="Bed Location", required=False)

# Form to create a new patient
class EditPatientForm(forms.Form):
    first_name = forms.CharField(max_length=200, label="First Name")
    last_name = forms.CharField(max_length=200, label="Last Name")
    gender = forms.CharField(max_length=100, widget=forms.Select(choices=Patient.GENDER_CHOICES), label="Gender")
    address = forms.CharField(max_length=400, label="Home Address", required=False)
    birth_date = forms.DateField(required=False, label="Date of Birth")
    phone = forms.CharField(max_length=200, label="Phone Number", required=False)
    email = forms.CharField(max_length=200, label="E-mail Address", required=False)
    height_cm = forms.DecimalField(max_digits=50, label="Height (in cm)")
    weight_kg = forms.DecimalField(max_digits=50, label="Weight (in kg)")
    blood_type = forms.CharField(max_length=100, widget=forms.Select(choices=Patient.BLOOD_TYPES), label="Blood Type")
    contact_name = forms.CharField(max_length=200, label="Secondary Contact - Name", required=False)
    contact_relationship = forms.CharField(max_length=200, label="Secondary Contact - Relationship to Patient", required=False)
    contact_phone = forms.CharField(max_length=200, label="Secondary Contact - Phone Number", required=False)
    contact_email = forms.CharField(max_length=200, label="Secondary Contact - E-mail Address", required=False)
    insurance_policy_provider = forms.CharField(max_length=200, label="Insurance Policy Provider", required=False)
    insurance_policy_number = forms.CharField(max_length=200, label="Insurance Policy Number", required=False)
    bed_location = forms.CharField(max_length=200, label="Bed Location", required=False)

# Form to delete a patient
class DeletePatientForm(forms.Form):
    pass

# Form to edit the picture
class NewPictureForm(forms.Form):
    avatar = forms.ImageField(label="Avatar")

# Form to create a new log item
class NewLogForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea(), label="Note")

    # Provide a placeholder value
    # ref: https://stackoverflow.com/questions/44133562/django-add-placeholder-text-to-form-field
    def __init__(self, *args, **kwargs):
        super(NewLogForm, self).__init__(*args, **kwargs)
        self.fields['note'].widget.attrs['placeholder'] = 'Please include information such as: toilet habits, meals and Oxygen Saturation Levels.'

# Form to edit a log item
class EditLogForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea(), label="Note")

# Form to delete a log item
class DeleteLogForm(forms.Form):
    pass

# Form to create a new Allergy
class NewAllergyForm(forms.Form):
    allergy = forms.CharField(max_length=200, label="Allergy")
    reaction = forms.CharField(widget=forms.Textarea(), label="Reaction")
    category = forms.CharField(max_length=100, widget=forms.Select(choices=Allergy.CATEGORY_CHOICES), label="Category")
    severity = forms.CharField(max_length=100, widget=forms.Select(choices=Allergy.SEVERITY_CHOICES), label="Severity")

# Form to edit an allergy
class EditAllergyForm(forms.Form):
    allergy = forms.CharField(max_length=200, label="Allergy")
    reaction = forms.CharField(widget=forms.Textarea(), label="Reaction")
    category = forms.CharField(max_length=100, widget=forms.Select(choices=Allergy.CATEGORY_CHOICES), label="Category")
    severity = forms.CharField(max_length=100, widget=forms.Select(choices=Allergy.SEVERITY_CHOICES), label="Severity")

# Form to delete an allergy
class DeleteAllergyForm(forms.Form):
    pass

# Create your views here.
def index(request):
    return render(request, "hms/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hms/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hms/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "hms/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hms/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hms/register.html")

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def patientindex(request):
    # Get all the users.
    patients= Patient.objects.order_by('last_name').all()

    # Paginate patients
    paginator = Paginator(patients, 20) # Show 20 patients per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"patients": page_obj}
    return render(request, "hms/patientindex.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def patient(request, pk):
    # Get the user ID and profile
    patient = Patient.objects.get(id=pk)
    allergies = Allergy.objects.filter(patient=patient).order_by('allergy').all()
    logs = Log.objects.filter(patient=patient).order_by('-timestamp').all()

    statuses = Hospitalization.objects.filter(patient=patient).order_by('-timestamp').all()

    if (len(statuses) > 0 and statuses[0].status == 'Check-in'):
        status = statuses[0]
    else:
        status = "Released"

    # Paginate history
    his_paginator = Paginator(statuses, 3) # Show 3 elements per page.
    his_page_number = request.GET.get('page_his')
    his_page_obj = his_paginator.get_page(his_page_number)

    # Paginate Log
    logs_paginator = Paginator(logs, 5) # Show 5 logs per page.
    logs_page_number = request.GET.get('page_log')
    logs_page_obj = logs_paginator.get_page(logs_page_number)

    # Paginate Allergoes
    allergies_paginator = Paginator(allergies, 10) # Show 10 allergies per page.
    allergies_page_number = request.GET.get('page_all')
    allergies_page_obj = allergies_paginator.get_page(allergies_page_number)

    context = {"patient": patient, "status": status, "statuses": his_page_obj, "logs": logs_page_obj, "NewLogForm": NewLogForm, "allergies": allergies_page_obj, "NewAllergyForm": NewAllergyForm}
    return render(request, "hms/profile.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def addpatient(request):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPatientForm(request.POST, request.FILES)
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            gender = form.cleaned_data["gender"]
            address = form.cleaned_data["address"]
            birth_date = form.cleaned_data["birth_date"]
            phone = form.cleaned_data["phone"]
            avatar = form.cleaned_data['avatar']
            email = form.cleaned_data["email"]
            height_cm = form.cleaned_data["height_cm"]
            weight_kg = form.cleaned_data["weight_kg"]
            blood_type = form.cleaned_data["blood_type"]
            contact_name = form.cleaned_data["contact_name"]
            contact_relationship = form.cleaned_data["contact_relationship"]
            contact_phone = form.cleaned_data["contact_phone"]
            contact_email = form.cleaned_data["contact_email"]
            insurance_policy_provider = form.cleaned_data["insurance_policy_provider"]
            insurance_policy_number = form.cleaned_data["insurance_policy_number"]
            bed_location = form.cleaned_data["bed_location"]

            # Write to DB, Patient table
            patient = Patient(
                first_name = first_name,
                last_name = last_name,
                gender = gender,
                address = address,
                birth_date = birth_date,
                phone = phone,
                avatar = avatar,
                email = email,
                height_cm = height_cm,
                weight_kg = weight_kg,
                blood_type = blood_type,
                contact_name = contact_name,
                contact_relationship = contact_relationship,
                contact_phone = contact_phone,
                contact_email = contact_email,
                insurance_policy_provider = insurance_policy_provider,
                insurance_policy_number = insurance_policy_number,
                bed_location = bed_location
                )
            patient.save()

            # Redirect user to new patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient.id,)))

   # Check if method is not POST, display the add page
    else:
        view = "addpatient"
        title = "New Patient"
        form = NewPatientForm
        context = {"view": view, "title": title, "form": form}
        return render(request, "hms/add.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def editpatient(request, patient_pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditPatientForm(request.POST, request.FILES)
        # Check if form data is valid (server-side)
        if form.is_valid():

            patient = Patient.objects.get(id=patient_pk)
            # Isolate the items from the 'cleaned' version of form data
            patient.first_name = form.cleaned_data["first_name"]
            patient.last_name = form.cleaned_data["last_name"]
            patient.gender = form.cleaned_data["gender"]
            patient.address = form.cleaned_data["address"]
            patient.birth_date = form.cleaned_data["birth_date"]
            patient.phone = form.cleaned_data["phone"]
            patient.email = form.cleaned_data["email"]
            patient.height_cm = form.cleaned_data["height_cm"]
            patient.weight_kg = form.cleaned_data["weight_kg"]
            patient.blood_type = form.cleaned_data["blood_type"]
            patient.contact_name = form.cleaned_data["contact_name"]
            patient.contact_relationship = form.cleaned_data["contact_relationship"]
            patient.contact_phone = form.cleaned_data["contact_phone"]
            patient.contact_email = form.cleaned_data["contact_email"]
            patient.insurance_policy_provider = form.cleaned_data["insurance_policy_provider"]
            patient.insurance_policy_number = form.cleaned_data["insurance_policy_number"]
            patient.bed_location = form.cleaned_data["bed_location"]
            patient.save()

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk)))

   # Check if method is not POST, display the edit page
    else:
        view = "editpatient"
        title = "patient"
        patient = Patient.objects.get(id=patient_pk)
        form = EditPatientForm(initial={
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'gender': patient.gender,
            'address': patient.address,
            'birth_date': patient.birth_date,
            'phone': patient.phone,
            'email': patient.email,
            'height_cm': patient.height_cm,
            'weight_kg': patient.weight_kg,
            'blood_type': patient.blood_type,
            'contact_name': patient.contact_name,
            'contact_relationship': patient.contact_relationship,
            'contact_phone': patient.contact_phone,
            'contact_email': patient.contact_email,
            'insurance_policy_provider': patient.insurance_policy_provider,
            'insurance_policy_number': patient.insurance_policy_number,
            'bed_location': patient.bed_location
        })
        element = patient
        element_name = patient.first_name + " " + patient.last_name
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/edit.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def deletepatient(request, patient_pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = DeleteLogForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            patient = Patient.objects.get(id=patient_pk)
            patient.delete()

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse(index))

   # Check if method is not POST, display the dete confirmation page
    else:
        view = "deletepatient"
        title = "patient"
        patient = Patient.objects.get(id=patient_pk)
        form = DeletePatientForm
        element = patient
        element_name = patient.first_name + " " + patient.last_name
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/delete.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def editpicture(request, patient_pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPictureForm(request.POST, request.FILES)
        # Check if form data is valid (server-side)
        if form.is_valid():

            patient = Patient.objects.get(id=patient_pk)
            # Isolate the items from the 'cleaned' version of form data
            patient.avatar = form.cleaned_data["avatar"]
            patient.save()

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk)))

   # Check if method is not POST, display the edit page
    else:
        view = "editpicture"
        title = "Edit/Add Picture"
        patient = Patient.objects.get(id=patient_pk)
        form = NewPictureForm
        element = patient
        element_name = patient.first_name + " " + patient.last_name
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/edit.html", context)


@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def checkinout(request, patient_pk):

    patient = Patient.objects.get(id=patient_pk)
    nurse = request.user

    statuses = Hospitalization.objects.filter(patient=patient).order_by('-timestamp').all()

    if (len(statuses) > 0 and statuses[0].status == 'Check-in'):
        new_status = "Check-out"
        patient.bed_location = "N/A"
        patient.save()
    else:
        new_status = "Check-in"

    hospitalization = Hospitalization(
        patient = patient,
        nurse = nurse,
        status = new_status
    )
    hospitalization.save()

    return HttpResponseRedirect(reverse("patient", args=(patient_pk)))

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def addlog(request, patient_pk):
    # If post, save to DB and redirect to the profile page
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewLogForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            note = form.cleaned_data["note"]

            # Values not from form
            patient = Patient.objects.get(id=patient_pk)
            nurse = request.user

            # Write to DB, log table
            log = Log(patient=patient, nurse=nurse, note=note)
            log.save()

        return HttpResponseRedirect(reverse("patient", args=(patient_pk,)))

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def editlog(request, pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditLogForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            log = Log.objects.get(id=pk)
            # Isolate the items from the 'cleaned' version of form data
            log.note = form.cleaned_data["note"]
            log.nurse = request.user
            log.save()

            # Values not from form
            patient_pk = Patient.objects.get(id=log.patient.id)

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk.id,)))

   # Check if method is not POST, display the edit page
    else:
        view = "editlog"
        title = "Log"
        log = Log.objects.get(id=pk)
        patient = patient_pk = Patient.objects.get(id=log.patient.id)
        form = EditLogForm(initial={'note': log.note})
        element = log
        element_name = log.timestamp
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/edit.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def deletelog(request, pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = DeleteLogForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            log = Log.objects.get(id=pk)
            log.delete()

            # Values not from form
            patient_pk = Patient.objects.get(id=log.patient.id)

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk.id,)))

   # Check if method is not POST, display the dete confirmation page
    else:
        view = "deletelog"
        title = "Log"
        log = Log.objects.get(id=pk)
        patient = patient_pk = Patient.objects.get(id=log.patient.id)
        form = DeleteLogForm
        element = log
        element_name = log.timestamp
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/delete.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def addallergy(request, patient_pk):
    # If post, save to DB and redirect to the profile page
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewAllergyForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            allergy = form.cleaned_data["allergy"]
            reaction = form.cleaned_data["reaction"]
            category = form.cleaned_data["category"]
            severity = form.cleaned_data["severity"]

            # Values not from form
            patient = Patient.objects.get(id=patient_pk)
            nurse = request.user

            # Write to DB, allergy table
            allergy = Allergy(patient=patient, nurse=nurse, allergy=allergy, reaction=reaction, category=category, severity=severity)
            allergy.save()

        return HttpResponseRedirect(reverse("patient", args=(patient_pk)))

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def editallergy(request, pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditAllergyForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            allergy = Allergy.objects.get(id=pk)
            # Isolate the items from the 'cleaned' version of form data
            allergy.allergy = form.cleaned_data["allergy"]
            allergy.reaction = form.cleaned_data["reaction"]
            allergy.category = form.cleaned_data["category"]
            allergy.severity = form.cleaned_data["severity"]
            allergy.nurse = request.user
            allergy.save()

            # Values not from form
            patient_pk = Patient.objects.get(id=allergy.patient.id)

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk.id,)))

   # Check if method is not POST, display the edit page
    else:
        view = "editallergy"
        title = "Allergy"
        allergy = Allergy.objects.get(id=pk)
        patient = patient_pk = Patient.objects.get(id=allergy.patient.id)
        form = EditAllergyForm(initial={'allergy': allergy.allergy, 'reaction': allergy.reaction, 'category': allergy.category, 'severity': allergy.severity})
        element = allergy
        element_name = allergy.allergy
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/edit.html", context)

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def deleteallergy(request, pk):
   # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = DeleteAllergyForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            allergy = Allergy.objects.get(id=pk)
            allergy.delete()

            # Values not from form
            patient_pk = Patient.objects.get(id=allergy.patient.id)

            # Redirect user to patient profile
            return HttpResponseRedirect(reverse("patient", args=(patient_pk.id,)))

   # Check if method is not POST, display the delete page
    else:
        view = "deleteallergy"
        title = "Allergy"
        allergy = Allergy.objects.get(id=pk)
        patient = patient_pk = Patient.objects.get(id=allergy.patient.id)
        form = DeleteAllergyForm
        element = allergy
        element_name = allergy.allergy
        context = {"view": view, "title": title, "form": form, "element": element, "element_name": element_name, "patient": patient}
        return render(request, "hms/delete.html", context)

@csrf_exempt
@login_required
def chart(request, patient_pk, vital_id):
    # Get the user ID, vital and extract data
    patient = Patient.objects.get(id=patient_pk)
    data_db = Record.objects.filter(patient=patient, vital=vital_id).all().order_by('timestamp')

    if not data_db.exists():
        return JsonResponse({"error": "No data."}, status=404)
    # Put the data into an array
    data=[['Date-Time', 'Value']]

    for row in data_db:
        value =  [str(row.timestamp), row.value]
        data.append(value)

    return JsonResponse(json.dumps(data, cls=DecimalEncoder), safe=False)

@csrf_exempt
@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def add_vital(request, patient_pk, vital_id):
    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Extract Post ID and data
    patient = Patient.objects.get(id=patient_pk)
    data = json.loads(request.body)
    value = data.get("value", "")

    record = Record(
        patient=patient,
        nurse=request.user,
        vital=vital_id,
        value=value
        )
    record.save()

    return JsonResponse({"message": "Value added successfully."}, status=201)

# Decimal encoder for JSON
# ref: https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)