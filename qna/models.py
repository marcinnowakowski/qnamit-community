from django.db import models
from django.urls import reverse

class Survey(models.Model):
  title = models.CharField(max_length=255)
  pub_date = models.DateTimeField('Date submitted',auto_now_add=True)
  slug = models.SlugField(unique=True)
  description = models.TextField()
  public = models.BooleanField(default=False)

  def __str__(self):
    return self.title

class Question(models.Model):
  title = models.CharField(max_length=255)
  survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING, related_name='questions')
  pub_date = models.DateTimeField('Date submitted',auto_now_add=True)
  question_text = models.TextField()
  public = models.BooleanField(default=False)

  def __str__(self):
    return str(self.survey) + ":" + self.title

class Patient(models.Model):
  patient_number = models.CharField(max_length=50, unique=True)
  registered_at = models.DateTimeField('Date submitted',auto_now_add=True)

  def __str__(self):
    return self.patient_number

class SurveySubmission(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='survey_submissions')
  survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
  submitted_at = models.DateTimeField('Date submitted',auto_now_add=True)

  def __str__(self):
    return str(self.submitted_at) + ":" + str(self.patient) + ":" + str(self.survey)

class Answer(models.Model):
  survey_submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name='answers')
  question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
  answer_text = models.TextField()

  def __str__(self):
    return str(self.survey_submission) + ":" + str(self.question)
