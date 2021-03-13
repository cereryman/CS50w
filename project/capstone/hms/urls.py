from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("patientindex", views.patientindex, name="patientindex"),
    path("patient/<str:pk>", views.patient, name="patient"),
    path("addpatient", views.addpatient, name="addpatient"),
    path("editpatient/<str:patient_pk>", views.editpatient, name="editpatient"),
    path("deletepatient/<str:patient_pk>", views.deletepatient, name="deletepatient"),
    path("editpicture/<str:patient_pk>", views.editpicture, name="editpicture"),
    path("checkinout/<str:patient_pk>", views.checkinout, name="checkinout"),
    path("addlog/<str:patient_pk>", views.addlog, name="addlog"),
    path("editlog/<str:pk>", views.editlog, name="editlog"),
    path("deletelog/<str:pk>", views.deletelog, name="deletelog"),
    path("addallergy/<str:patient_pk>", views.addallergy, name="addallergy"),
    path("editallergy/<str:pk>", views.editallergy, name="editallergy"),
    path("deleteallergy/<str:pk>", views.deleteallergy, name="deleteallergy"),
    path("chart/<str:patient_pk>/<str:vital_id>", views.chart, name="chart"),
    path("add_vital/<str:patient_pk>/<str:vital_id>", views.add_vital, name="add_vital")
]
