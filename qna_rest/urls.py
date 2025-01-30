from django.urls import path
from .views import PatientDetailAPIView, PatientRegisterAPIView, QuestionDetailAPIView, SurveyListAPIView, SurveyDetailAPIView, SurveySubmissionAPIView

urlpatterns = [
    path('patient/', PatientRegisterAPIView.as_view(), name='patient-create-if-doesnt-exist'),
    path('patient/<str:patient_number>/', PatientDetailAPIView.as_view(), name='patient-detail'),
    path('survey/', SurveyListAPIView.as_view(), name='list-surveys'),
    path('survey/<slug:slug>/', SurveyDetailAPIView.as_view(), name='survey-detail'),
    path('survey-submission/', SurveySubmissionAPIView.as_view(), name='survey-submission'),
    path('survey-submissions/<int:survey_submission_id>/questions/<int:question_id>/', QuestionDetailAPIView.as_view(), name='question-detail'),
]
