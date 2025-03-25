import qrcode
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings

class EmergencyInfo(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    medical_conditions = models.TextField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR Code with the emergency info URL
        qr_url = f"http://127.0.0.1:8000/emergency/{self.user_id}/"
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Save QR code image
        self.qr_code.save(f'{self.user_id}.png', ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
        
        # Send QR Code to user's email
        self.send_qr_email(buffer)
        
    def send_qr_email(self, qr_buffer):
        subject = "Your Emergency QR Code"
        message = f"""
            Hello {self.name},

            Your emergency QR code has been generated. 

            📌 **Scan the QR code** attached to this email to access your emergency details.

            🔗 Or click this link: [View Emergency Info](http://127.0.0.1:8000/emergency/{self.user_id}/)

            Stay safe!
            """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]

        # Create Email Message
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach(f"qr_code_{self.user_id}.png", qr_buffer.getvalue(), "image/png")

        # Send Email
        email.send()

    def __str__(self):
        return self.name
