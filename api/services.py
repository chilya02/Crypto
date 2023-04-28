from .utils import menu, modal, html
from .utils.rows import generate_user_post_row, generate_post_row, generate_currency_row
from .utils.info import get_post_info, get_post_actions
from authentication.models import User
from p2p.models import NewOrder, BuyPost, SellPost, Order, Message
from courses.models import Course
from django.template.loader import render_to_string


def get_courses_html() -> str:
    Course.update_courses()
    courses = Course.objects.order_by('RUB')
    return render_to_string('courses/courses_table.html', context={'courses': courses})

