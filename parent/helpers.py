# parent/helpers.py

# You can import any necessary modules for sending emails
from django.core.mail import send_mail

def send_forget_password_mail(email, token):
    # Define your email sending logic here
    subject = "Reset Your Password"
    message = f"Click the link below to reset your password:\n\nhttp://127.0.0.1:8000/parent/change_password/{token}"
    from_email = "noreply@example.com"
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
