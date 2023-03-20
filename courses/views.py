from django.shortcuts import render
from django.http import JsonResponse

def courses_view(request):
    return render(request=request, template_name='courses/currency_courses.html', context={'section':"courses"})
