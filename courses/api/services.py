# from courses.models import Course
from django.template.loader import render_to_string


def get_courses_html() -> str:
    # Course.update_courses()
    # courses = Course.objects.order_by('RUB')
    return render_to_string('courses/courses_table.html', context={})
