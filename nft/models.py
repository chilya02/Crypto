from django.db import models
from authentication.models import User
from courses.models import Course
from common_utils import normalize_number


currencies = (("USDT", 'usdt'), ('BTC', 'btc'), ('ETH', 'eth'), ('KPFU', 'kpfu'), ('SOL', 'sol'))


class Collection(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)
    changeable = models.BooleanField(verbose_name='Изменямость', default=True)

    def __str__(self):
        return self.name

    @property
    def summary_price_rub(self) -> str:
        images = self.images.all()
        total_sum_rub = 0
        crypto_courses = Course.objects.all()
        clean_courses = {}
        for course in crypto_courses:
            clean_courses[course.currency] = course.RUB
        for image in images:
            current_price_rub = image.price * clean_courses[image.currency]
            total_sum_rub += current_price_rub
        return normalize_number(total_sum_rub)

    @property
    def summary_price_usdt(self) -> str:
        images = self.images.all()
        total_sum_usdt = 0
        crypto_courses = Course.objects.all()
        clean_courses = {}
        for course in crypto_courses:
            clean_courses[course.currency] = course.USDT
        for image in images:
            current_price_usdt = image.price * clean_courses[image.currency]
            total_sum_usdt += current_price_usdt
        return normalize_number(total_sum_usdt)

    @property
    def count(self):
        images = self.images.all()
        return len(images)


class NftImage(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    price = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(verbose_name='Валюта', choices=currencies, max_length=4)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        verbose_name='Коллекция',
        related_name='images'
    )
    img = models.ImageField(verbose_name='Изображение', upload_to='NFTs')

    def __str__(self):
        return self.name


class NftPost(models.Model):
    image = models.ForeignKey(NftImage, verbose_name='Изображение', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(verbose_name='Валюта', choices=currencies, max_length=4)

    def __str__(self):
        return self.image.name
