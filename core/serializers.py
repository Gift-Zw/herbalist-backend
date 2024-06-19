from rest_framework import serializers
from .models import Patient, Herbalist, Prescription, ChatMessage


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['password']


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class HerbalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herbalist
        exclude = ['password']


class HerbalistRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herbalist
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
