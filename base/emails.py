from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_profile_activation_email(email, email_token):
    subject = 'Your acount needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on this link to activate your profile http http://127.0.0.1:8000/users/activate/{email_token}/'
    send_mail(subject, message, email_from, [email])








   







# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# def send_profile_activation_email(user_email, user):
#     subject = "Welcome to Our Website!"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     print('uuuu')
#     # Render HTML content using Django template
#     html_content = render_to_string("email.html")
    
#     # Convert HTML to plain text
#     text_content = strip_tags(html_content)
#     print(text_content)

#     # Create email with both plain text and HTML
#     email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
#     email.attach_alternative(html_content, "text/html")  # Attach HTML version
#     email.send()
#     print('yes')
#     return "Email sent successfully!"