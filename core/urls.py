from django.urls import path
from .views import (
    PatientListView, PatientRegisterView, patient_login,
    HerbalistListView, HerbalistRegisterView, herbalist_login,
    get_prescriptions, complete_prescription, delete_prescription, create_prescription,
    get_chats, create_message, view_messages
)

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/register/', PatientRegisterView.as_view(), name='patient-register'),
    path('patients/login/', patient_login, name='patient-login'),

    path('herbalist/register/', HerbalistRegisterView.as_view(), name='herbalist-register'),
    path('herbalist/login/', herbalist_login, name='herbalist-login'),
    path('herbalist/all/', HerbalistListView.as_view(), name='herbalist-list'),

    path('prescription/', get_prescriptions, name='get-prescriptions'),
    path('prescription/complete/', complete_prescription, name='complete-prescription'),
    path('prescription/delete/', delete_prescription, name='delete-prescription'),
    path('prescription/create/', create_prescription, name='create-prescription'),

    path('chat/chats/', get_chats, name='get-chats'),
    path('chat/message/create/', create_message, name='create-message'),
    path('chat/view/', view_messages, name='view-messages'),
]