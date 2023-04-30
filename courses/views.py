from django.shortcuts import render


def courses_view(request):
    return render(request=request, template_name='courses/currency_courses.html', context={'section': "courses"})
