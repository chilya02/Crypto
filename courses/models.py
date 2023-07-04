from django.db import models
from .services import get_courses_from_api
import datetime
# Create your models here.
from asgiref.sync import sync_to_async


class Course(models.Model):
    currency = models.CharField(verbose_name="Валюта", max_length=4)
    time = models.DateTimeField(verbose_name="Дата обновления")
    RUB = models.FloatField(verbose_name='В рублях')
    USDT = models.FloatField(verbose_name='В USDT')
    volume = models.IntegerField(verbose_name='Объём')
    change = models.FloatField(verbose_name='Изменение')
    quote_volume = models.FloatField(verbose_name='Капитализация')

    @classmethod
    def update_courses(cls):
        try:
            if datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4))) - Course.objects.get(currency='USDT').time > datetime.timedelta(minutes=1, seconds=1, milliseconds=1, microseconds=1):
                data = get_courses_from_api()
                for key, value in data.items():
                    currency = cls.objects.get(currency=key)
                    for inner_key, inner_value in value.items():
                        setattr(currency, inner_key, inner_value)
                        currency.time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
                    currency.save()
                KPFU = cls.objects.get(currency='KPFU')
                KPFU.RUB = 4 * cls.objects.get(currency='USDT').RUB
                KPFU.quote_volume = round(KPFU.volume * KPFU.RUB, 2)
                KPFU.save()
        except:
            pass

    def __str__(self) -> str:
        return self.currency


@sync_to_async
def get_courses():
    courses = Course.objects.all()
    data = []
    for course in courses:
        data.append({
            'currency': course.currency,
            'RUB': course.RUB,
            'change': course.change,
            'volume': course.volume,
            'quote_volume': course.quote_volume,
        })
    return data
