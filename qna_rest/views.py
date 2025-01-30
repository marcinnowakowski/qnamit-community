from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from qna.models import Answer, Patient, Question, Survey, SurveySubmission
from .serializers import AnswerSerializer, PatientRegisterSerializer, PatientDetailSerializer, SurveySubmissionSerializer, SurveySummarySerializer, SurveyDetailSerializer, QuestionSerializer


class PatientRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=PatientRegisterSerializer,  # Serializer for input data
        responses={
            200: openapi.Response('Patient already exists', PatientRegisterSerializer),
            201: openapi.Response('Patient created successfully', PatientRegisterSerializer),
            400: 'Invalid input'
        },
        operation_description="Register a new patient. Accepts JSON data."
    )
    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            if Patient.objects.filter(patient_number=serializer.validated_data['patient_number']).exists():
                return Response(serializer.data, status=status.HTTP_200_OK)  # Patient already exists
            serializer.save()  # Create a new patient
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid input

class PatientDetailAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'patient_number',
                openapi.IN_PATH,
                description="Unique patient number to retrieve details",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Patient details', PatientDetailSerializer),
            404: 'Patient not found',
        },
        operation_description="Retrieve patient details by their unique patient number."
    )
    def get(self, request, patient_number):
        try:
            patient = Patient.objects.get(patient_number=patient_number)
            response_serializer = PatientDetailSerializer(patient)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
          
class SurveyListAPIView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of surveys', SurveySummarySerializer(many=True)),
        },
        operation_description="Retrieve a list of surveys."
    )
    def get(self, request):
        surveys = Survey.objects.all()
        response_serializer = SurveySummarySerializer(surveys, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class SurveyDetailAPIView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Survey details with questions',
                SurveyDetailSerializer
            ),
            404: openapi.Response('Survey not found'),
        },
        operation_description="Retrieve detailed information about a survey, including its questions."
    )
    def get(self, request, slug):
        try:
            survey = Survey.objects.get(slug=slug, public=True)
            survey_serializer = SurveyDetailSerializer(survey)
            
            # Fetch associated questions
            questions = survey.questions.filter(public=True)
            questions_serializer = QuestionSerializer(questions, many=True)
            
            return Response(
                {
                    "survey": survey_serializer.data,
                    "questions": questions_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Survey.DoesNotExist:
            return Response(
                {"detail": "Survey not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
class QuestionDetailAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'survey_submission_id',
                openapi.IN_PATH,
                description="Survey submission id",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'question_id',
                openapi.IN_PATH,
                description="Question id",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                'Question details with answer',
                SurveyDetailSerializer
            ),
            404: openapi.Response('Question not found'),
        },
        operation_description="Retrieve detailed information about a question, including its answer."
    )
    def get(self, request, survey_submission_id, question_id):
        # Fetch survey submission and question
        survey_submission = get_object_or_404(SurveySubmission, id=survey_submission_id)
        question = get_object_or_404(Question, id=question_id)
        question_serializer = QuestionSerializer(question)
        
        answer = survey_submission.answers.filter(question_id=question_id).first()

        if(answer == None):
          return Response(
                {
                    "question": question_serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        answer_serializer = AnswerSerializer(answer)
        return Response(
                {
                    "question": question_serializer.data,
                    "answer": answer_serializer.data
                },
                status=status.HTTP_200_OK
            )
            
class SurveySubmissionAPIView(APIView):
    @swagger_auto_schema(
        request_body=SurveySubmissionSerializer,  # Serializer for input data
        responses={
            201: openapi.Response('Survey submitted successfully', PatientRegisterSerializer),
            400: 'Invalid input'
        },
        operation_description="Submit a new survey. Accepts JSON data."
    )
    def post(self, request):
        # Validate the input data
        serializer = SurveySubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        patient_id = serializer.validated_data.get('patient_id')
        survey_id = serializer.validated_data.get('survey_id')
        answers = serializer.validated_data.get('answers')

        # Fetch patient and survey objects
        patient = get_object_or_404(Patient, id=patient_id)
        survey = get_object_or_404(Survey, id=survey_id)

        # Create survey submission
        survey_submission = SurveySubmission.objects.create(
            patient=patient,
            survey=survey
        )

        # Save answers
        for answer in answers:
            question_id = answer.get('question_id')
            answer_text = answer.get('answer_text')

            question = get_object_or_404(Question, id=question_id)
            Answer.objects.create(
                survey_submission=survey_submission,
                question=question,
                answer_text=answer_text
            )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
