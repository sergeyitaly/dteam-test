from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML

@shared_task(bind=True)
def send_cv_pdf_email(self, cv_id, email_to):
    from .models import CV
    cv = CV.objects.get(pk=cv_id)
    
    # Generate PDF
    html_string = render_to_string('main/cv_pdf.html', {'cv': cv})
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)
    
    # Send email
    subject = f"CV of {cv.first_name} {cv.last_name}"
    body = f"Please find attached the CV of {cv.first_name} {cv.last_name}"
    
    email = EmailMessage(
        subject,
        body,
        'noreply@cvproject.com',
        [email_to],
    )
    email.attach(
        f"{cv.first_name}_{cv.last_name}_CV.pdf",
        pdf_file.getvalue(),
        'application/pdf'
    )
    email.send()
    
    return f"Email sent to {email_to}"