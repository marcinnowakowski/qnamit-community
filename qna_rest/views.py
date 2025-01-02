from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from qna.models import Patient
from .serializers import PatientRegisterSerializer, PatientDetailSerializer


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
