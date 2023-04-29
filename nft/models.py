from django.db import models
from authentication.models import User


class Collection(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)
    changeable = models.BooleanField(verbose_name='Изменямость', default=True)


class NftImage(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    price = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(max_length=4, verbose_name='Валюта')
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        verbose_name='Коллекция',
        related_name='images'
    )


class NftPost(models.Model):
    image = models.ForeignKey(NftImage, verbose_name='Изображение', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(max_length=4, verbose_name='Валюта')
