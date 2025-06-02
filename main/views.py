from django.shortcuts import render, get_object_or_404
from .models import CV
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from rest_framework import viewsets
from .serializers import CVSerializer

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
