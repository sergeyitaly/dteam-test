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
from openai import OpenAI

logger = logging.getLogger(__name__)

@csrf_exempt 
def translate_cv(request, pk):
    if request.method == 'POST':
        try:
            cv = CV.objects.get(pk=pk)
            target_language = request.POST.get('language')
            
            text_to_translate = f"""
            CV of {cv.first_name} {cv.last_name}
            Contact Information: {cv.contact_info if hasattr(cv, 'contact_info') else 'Not provided'}
            Bio: {cv.bio}
            Skills: {', '.join(skill.name for skill in cv.skills.all())}
            Projects: {' | '.join(f"{p.title}: {p.description}" for p in cv.projects.all())}
            Work Experience: {' | '.join(f"{exp.position} at {exp.company}: {exp.description}" 
                                      for exp in cv.experience.all()) if hasattr(cv, 'experience') else 'Not provided'}
            Education: {' | '.join(f"{edu.degree} at {edu.institution}" 
                                for edu in cv.education.all()) if hasattr(cv, 'education') else 'Not provided'}
            """
            
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                max_retries=3, 
                timeout=30 
            )
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125", 
                messages=[
                    {
                        "role": "system", 
                        "content": f"""You are a professional CV translator. 
                        Translate the following CV content to {target_language}.
                        Maintain the original formatting and structure.
                        Keep professional terminology accurate.
                        Preserve proper names and technical terms unless they have 
                        a commonly accepted translation in {target_language}."""
                    },
                    {
                        "role": "user", 
                        "content": text_to_translate
                    }
                ],
                temperature=0.2,  # Lower temperature for more deterministic translations
                max_tokens=3000,  # Set appropriate limit
                top_p=0.1,  # Focus on most likely translations
                frequency_penalty=0.2,  # Reduce repetition
                presence_penalty=0.1,  # Encourage diversity
            )

            translated_text = response.choices[0].message.content
            
            return JsonResponse({
                'translation': translated_text,
                'status': 'success',
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            })
            
        except openai.RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {e}")
            return JsonResponse({
                'error': 'Translation service quota exceeded. Please try again later or contact support.',
                'details': str(e),
                'solution': 'Check your OpenAI plan and billing details'
            }, status=429)
            
        except openai.APITimeoutError as e:
            logger.error(f"OpenAI Timeout Error: {e}")
            return JsonResponse({
                'error': 'Translation service timeout. Please try again.',
                'details': str(e)
            }, status=504)
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {e}")
            return JsonResponse({
                'error': 'Authentication failed with translation service.',
                'details': str(e),
                'solution': 'Verify your OPENAI_API_KEY in settings'
            }, status=401)
            
        except openai.APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            return JsonResponse({
                'error': 'Translation service unavailable.',
                'details': str(e),
                'solution': 'Try again later or contact support'
            }, status=503)
            
        except Exception as e:
            logger.error(f"Unexpected translation error: {e}", exc_info=True)
            return JsonResponse({
                'error': 'An unexpected error occurred during translation.',
                'details': str(e),
                'solution': 'Check server logs for more information'
            }, status=500)
    
    return JsonResponse({
        'error': 'Invalid request method',
        'allowed_methods': ['POST']
    }, status=405)


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
