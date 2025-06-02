from django.shortcuts import render, get_object_or_404, redirect
from .models import CV
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from rest_framework import viewsets
from .serializers import CVSerializer
from django.views.generic import TemplateView
from django.conf import settings
from .decorators import staff_required
from django.utils.decorators import method_decorator
from .tasks import send_cv_pdf_email
from django.contrib import messages
import openai
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai

logger = logging.getLogger(__name__)

@csrf_exempt 
def translate_cv(request, pk):
    if request.method == 'POST':
        try:
            cv = CV.objects.get(pk=pk)
            target_language = request.POST.get('language')
            
            text_to_translate = f"""
            CV of {cv.first_name} {cv.last_name}
            Bio: {cv.bio}
            Skills: {', '.join(skill.name for skill in cv.skills.all())}
            Projects: {' | '.join(f"{p.title}: {p.description}" for p in cv.projects.all())}
            """
            
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following CV content to {target_language}."},
                    {"role": "user", "content": text_to_translate}
                ],
                temperature=0.3,
            )

            translated_text = response.choices[0].message.content
            return JsonResponse({'translation': translated_text})
        
        except openai.RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {e}")
            return JsonResponse({
                'error': 'Translation service quota exceeded. Please try again later or contact support.',
                'details': str(e)
            }, status=429)
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {e}")
            return JsonResponse({
                'error': 'Authentication failed with translation service.',
                'details': str(e)
            }, status=401)
            
        except Exception as e:
            logger.error(f"Translation error: {e}", exc_info=True)
            return JsonResponse({
                'error': 'An unexpected error occurred during translation.',
                'details': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_cv_email(request, pk):
    if request.method == 'POST':
        email_to = request.POST.get('email')
        task = send_cv_pdf_email.delay(pk, email_to)
        messages.success(
            request,
            f"CV is being sent to {email_to}. Task ID: {task.id}"
        )
    return redirect('main:cv_detail', pk=pk)

@method_decorator(staff_required, name='dispatch')
class SettingsView(TemplateView):
    template_name = 'main/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_settings'] = {
            'DEBUG': settings.DEBUG,
            'SECRET_KEY': '*****' if settings.SECRET_KEY else None,
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'DATABASES': settings.DATABASES,
            'INSTALLED_APPS': settings.INSTALLED_APPS,
            'MIDDLEWARE': settings.MIDDLEWARE,
            'TEMPLATES': settings.TEMPLATES,
        }
        return context
    
    
class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all().prefetch_related('skills', 'projects')
    serializer_class = CVSerializer

def cv_pdf(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    
    # Render HTML template
    html_string = render_to_string('main/cv_pdf.html', {'cv': cv})
    
    # Create PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    
    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.first_name}_{cv.last_name}_CV.pdf"'
    response.write(result)
    
    return response

def cv_list(request):
    cvs = CV.objects.all().prefetch_related('skills', 'projects')
    return render(request, 'main/cv_list.html', {'cvs': cvs})

def cv_detail(request, pk):
    cv = get_object_or_404(CV.objects.prefetch_related('skills', 'projects'), pk=pk)
    return render(request, 'main/cv_detail.html', {'cv': cv})
