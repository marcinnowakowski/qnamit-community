from rest_framework import serializers
from qna.models import Patient, Survey, Question

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'patient_number', 'registered_at']

class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_number']
        
class SurveySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['title','slug']

class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'slug']
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'question_text']
        
class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField()

class SurveySubmissionSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    survey_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)

    def validate(self, data):
        """
        Custom validation for the survey submission.
        Ensures the survey exists, all questions belong to the survey, and answers are valid.
        """
        survey_id = data.get('survey_id')
        answers = data.get('answers')

        # Validate survey existence
        survey = Survey.objects.filter(id=survey_id).first()
        if not survey:
            raise serializers.ValidationError({'survey_slug': 'Survey not found.'})

        # Validate questions
        survey_question_ids = set(survey.questions.values_list('id', flat=True))
        answer_question_ids = set(answer['question_id'] for answer in answers)

        if not answer_question_ids.issubset(survey_question_ids):
            raise serializers.ValidationError({'answers': 'Some questions do not belong to the specified survey.'})

        return data
