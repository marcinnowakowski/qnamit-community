from django.urls import path
from .views import PatientDetailAPIView, PatientRegisterAPIView

urlpatterns = [
    path('patient/', PatientRegisterAPIView.as_view(), name='patient-create-if-doesnt-exist'),
    path('api/patient/<str:patient_number>/', PatientDetailAPIView.as_view(), name='patient-detail'),
]
