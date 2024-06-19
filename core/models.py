from django.db import models


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=55, default='password')

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    herbalist_id = models.IntegerField()
    sender = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}..."


class Herbalist(models.Model):
    herbalist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    herbalist_name = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)
    prescription_id = models.CharField(max_length=100, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prescription_id