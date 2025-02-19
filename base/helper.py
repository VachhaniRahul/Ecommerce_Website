from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.conf import settings
from users.models import Invoice

def save_pdf(param:dict):
    template = get_template('email.html')
    html = template.render(param)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = param['name']

    try :
        with open(f'static/pdf/{file_name}.pdf', 'wb') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
        
    except Exception as e:

        print(e)

    if pdf.err:
        return "", False
    
    return file_name, True


from django.core.mail import EmailMessage

def send_email_with_pdf(email):
    mail = EmailMessage(
        subject='Invoice',
        body='Please find the attached PDF.',
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    # Attach PDF
    pdf_path = f'static/pdf/{email}.pdf'
    with open(pdf_path, 'rb') as pdf_file:
        mail.attach('invoice.pdf', pdf_file.read(), 'application/pdf')

        invoice = Invoice(email=email)
        invoice.file.save(f'{email} => invoice.pdf', pdf_file)  # Correct way to save a file in FileField
        invoice.save()

    mail.send()
    return invoice