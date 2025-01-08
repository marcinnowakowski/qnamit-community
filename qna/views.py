from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView
from .models import Answer, Patient, Question, Survey, SurveySubmission
from .forms import PatientForm, SurveySelectForm, SurveySubmissionForm

class PatientRegisterView(FormView):
    template_name = 'qna/patient_register.html'
    form_class = PatientForm

    def form_valid(self, form):
        print("8888888888888888888")
        # Sprawdź, czy istnieje pacjent o tym numerze
        patient_number = form.cleaned_data.get('patient_number')
        existing_patient = Patient.objects.filter(patient_number=patient_number).first()

        if existing_patient:
            # Jeśli pacjent istnieje, przekieruj do SurveySelectView
            return HttpResponseRedirect(reverse_lazy('survey_select', kwargs={
                'patient_number': existing_patient.patient_number
            }))

        # Jeśli pacjent nie istnieje, utwórz nowy obiekt
        new_patient = Patient.objects.create(
            patient_number=form.cleaned_data.get('patient_number')
        )

        # Przekieruj do SurveySelectView dla nowego pacjenta
        return HttpResponseRedirect(reverse_lazy('survey_select', kwargs={
            'patient_number': new_patient.patient_number
        }))

# Create view to select survey
class SurveySelectView(FormView):
    template_name = 'qna/survey_select.html'
    form_class = SurveySelectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the recently created or selected patient by patient_number
        patient_number = self.kwargs.get('patient_number')
        context['patient_selected_model'] = get_object_or_404(Patient, patient_number=patient_number)
        return context
    
    def form_valid(self, form):
        # Access form data
        survey_selected = form.cleaned_data['survey_selected']

        # Save survey or perform additional logic if needed
        self.object = survey_selected  # Save the selected survey for use in success_url
        return super().form_valid(form)

    def get_success_url(self):
        # Get patient_number from URL kwargs
        patient_number = self.kwargs.get('patient_number')

        return reverse_lazy('survey_submission_create', kwargs={
            'patient_number': patient_number,
            'survey_selected': self.object.slug,
        })

class SurveySubmissionCreateView(FormView):
    template_name = 'qna/survey_submission_create.html'
    form_class = SurveySubmissionForm

    def get_form_kwargs(self):
        # Pass questions to the form dynamically
        kwargs = super().get_form_kwargs()

        # Fetch the selected survey
        survey_selected_slug = self.kwargs.get('survey_selected')
        survey = get_object_or_404(Survey, slug=survey_selected_slug)

        # Add questions to kwargs for dynamic form generation
        kwargs['questions'] = survey.questions.all()
        print(str(kwargs['questions']))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the selected patient
        patient_number = self.kwargs.get('patient_number')
        context['patient_selected_model'] = get_object_or_404(Patient, patient_number=patient_number)

        # Fetch the selected survey
        survey_selected_slug = self.kwargs.get('survey_selected')
        context['survey_selected_model'] = get_object_or_404(Survey, slug=survey_selected_slug)

        return context

    def form_valid(self, form):
        # Handle submitted answers
        patient_number = self.kwargs.get('patient_number')
        patient = get_object_or_404(Patient, patient_number=patient_number)

        survey_slug = self.kwargs.get('survey_selected')
        survey = get_object_or_404(Survey, slug=survey_slug)
        
        # Save survey submission
        survey_submission = SurveySubmission.objects.create(
            patient=patient,
            survey=survey
        )

        # Save answers
        for field_name, answer_text in form.cleaned_data.items():
            question_id = field_name.split('_')[1]  # Extract question ID from field name
            question = get_object_or_404(Question, id=question_id)
            Answer.objects.create(
                survey_submission=survey_submission,
                question=question,
                answer_text=answer_text
            )

        return super().form_valid(form)

    def get_success_url(self):
        # Get patient_number from URL kwargs
        patient_number = self.kwargs.get('patient_number')
        survey_selected_slug = self.kwargs.get('survey_selected')
      
        return reverse_lazy('survey_submission_completed', kwargs={
            'patient_number': patient_number,
            'survey_selected': survey_selected_slug,
        })
        
# Create view to select survey
class SurveySubmissionCompletedView(TemplateView):
    template_name = 'qna/survey_submission_completed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the selected patient
        patient_number = self.kwargs.get('patient_number')
        context['patient_selected_model'] = get_object_or_404(Patient, patient_number=patient_number)

        # Fetch the selected survey
        survey_selected_slug = self.kwargs.get('survey_selected')
        context['survey_selected_model'] = get_object_or_404(Survey, slug=survey_selected_slug)

        return context
