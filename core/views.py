from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .models import Patient, Herbalist, Prescription, ChatMessage
from .serializers import (PatientSerializer, PatientRegisterSerializer,
                          HerbalistSerializer, HerbalistRegisterSerializer,
                          PrescriptionSerializer, ChatMessageSerializer)


# Patient Views
class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientRegisterView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientRegisterSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data['password']))


@api_view(['POST'])
def patient_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        patient = Patient.objects.get(email=email)
        if check_password(password, patient.password):
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)


# Herbalist Views
class HerbalistListView(generics.ListAPIView):
    queryset = Herbalist.objects.all()
    serializer_class = HerbalistSerializer


class HerbalistRegisterView(generics.CreateAPIView):
    queryset = Herbalist.objects.all()
    serializer_class = HerbalistRegisterSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data['password']))


@api_view(['POST'])
def herbalist_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        herbalist = Herbalist.objects.get(email=email)
        if check_password(password, herbalist.password):
            serializer = HerbalistSerializer(herbalist)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    except Herbalist.DoesNotExist:
        return Response({"error": "Herbalist not found"}, status=status.HTTP_404_NOT_FOUND)


# Prescription Views
@api_view(['GET'])
def get_prescriptions(request):
    patient_id = request.query_params.get('patient_id')
    prescriptions = Prescription.objects.filter(patient__patient_id=patient_id)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def complete_prescription(request):
    prescription_id = request.data.get('prescription_id')
    patient_id = request.data.get('patient_id')
    try:
        prescription = Prescription.objects.get(prescription_id=prescription_id, patient__patient_id=patient_id)
        prescription.is_complete = True
        prescription.save()
        return Response({"success": "Prescription marked as complete"})
    except Prescription.DoesNotExist:
        return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete_prescription(request):
    prescription_id = request.data.get('prescription_id')
    patient_id = request.data.get('patient_id')
    try:
        prescription = Prescription.objects.get(prescription_id=prescription_id, patient__patient_id=patient_id)
        prescription.delete()
        return Response({"success": "Prescription deleted"})
    except Prescription.DoesNotExist:
        return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_prescription(request):
    data = request.data
    serializer = PrescriptionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Chat Views
@api_view(['GET'])
def get_chats(request):
    patient_id = request.query_params.get('patient_id')
    herbalist_ids = ChatMessage.objects.filter(patient__patient_id=patient_id).values_list('herbalist_id',
                                                                                           flat=True).distinct()
    herbalists = Herbalist.objects.filter(herbalist_id__in=herbalist_ids)
    serializer = HerbalistSerializer(herbalists, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_message(request):
    data = request.data
    serializer = ChatMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_messages(request):
    patient_id = request.query_params.get('patient_id')
    herbalist_id = request.query_params.get('herbalist_id')
    messages = ChatMessage.objects.filter(patient__patient_id=patient_id, herbalist_id=herbalist_id).order_by('date')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)
