from .models import Answer, Patient, Question, Survey, SurveySubmission
from django.contrib import admin

class SurveyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    class Media:
        js = ('/media/fckeditor/fckeditor.js','/media/fckeditor/fckareas.js')

admin.site.register(Survey, SurveyAdmin)

class QuestionAdmin(admin.ModelAdmin):
    class Media:
        js = ('/media/fckeditor/fckeditor.js','/media/fckeditor/fckareas.js')

admin.site.register(Question, QuestionAdmin)

class PatientAdmin(admin.ModelAdmin):
    class Media:
        js = ('/media/fckeditor/fckeditor.js','/media/fckeditor/fckareas.js')

admin.site.register(Patient, PatientAdmin)

class SurveySubmissionAdmin(admin.ModelAdmin):
    class Media:
        js = ('/media/fckeditor/fckeditor.js','/media/fckeditor/fckareas.js')

admin.site.register(SurveySubmission, SurveySubmissionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    class Media:
        js = ('/media/fckeditor/fckeditor.js','/media/fckeditor/fckareas.js')

admin.site.register(Answer, AnswerAdmin)
