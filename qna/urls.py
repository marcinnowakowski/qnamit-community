from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientRegisterView.as_view(), name='patient_register'),
    path('patient_register/', views.PatientRegisterView.as_view(), name='patient_register'),
    path('survey_select/<str:patient_number>/', views.SurveySelectView.as_view(), name='survey_select'),
    path('survey_submission_create/<str:patient_number>/<slug:survey_selected>', views.SurveySubmissionCreateView.as_view(), name='survey_submission_create'),
    path('survey_submission_completed/<str:patient_number>/<slug:survey_selected>', views.SurveySubmissionCompletedView.as_view(), name='survey_submission_completed'),
]