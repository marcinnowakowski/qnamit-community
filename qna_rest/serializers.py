from rest_framework import serializers
from qna.models import Patient

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_number', 'registered_at']

class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_number']
