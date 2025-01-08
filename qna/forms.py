from django import forms
from .models import Patient, Survey

class PatientForm(forms.Form):
    patient_number = forms.CharField(
    max_length=50,
    label="Numer pacjenta",
    widget=forms.TextInput(attrs={'placeholder': 'Wpisz numer pacjenta'}),
    required=True,
    )
        
class SurveySelectForm(forms.Form):
    survey_selected = forms.ModelChoiceField(
        queryset=Survey.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select a Survey",
        empty_label="Choose a survey"
    )

class SurveySubmissionForm(forms.Form):
    """
    A dynamic form that generates fields for each question in a survey.
    """
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')  # Get questions passed during initialization
        super().__init__(*args, **kwargs)

        # Dynamically create a field for each question
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.question_text,
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                required=True
            )
