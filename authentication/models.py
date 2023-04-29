from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from courses.models import Course


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Имя пользователя', max_length=20, unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_staff = models.BooleanField(default=False)
    USDT = models.IntegerField(verbose_name='USDT', default=0)
    BTC = models.IntegerField(verbose_name='BTC', default=0)
    ETH = models.IntegerField(verbose_name='ETH', default=0)
    KPFU = models.IntegerField(verbose_name='KPFU', default=0)
    SOL = models.IntegerField(verbose_name='SOL', default=0)
    USDT_reserved = models.IntegerField(verbose_name='USDT резерв', default=0)
    BTC_reserved = models.IntegerField(verbose_name='BTC резерв', default=0)
    ETH_reserved = models.IntegerField(verbose_name='ETH резерв', default=0)
    KPFU_reserved = models.IntegerField(verbose_name='KPFU резерв', default=0)
    SOL_reserved = models.IntegerField(verbose_name='SOL резерв', default=0)

    USDT_reserved_payed = models.IntegerField(verbose_name='USDT оплаченный резерв', default=0)
    BTC_reserved_payed = models.IntegerField(verbose_name='BTC оплаченный резерв', default=0)
    ETH_reserved_payed = models.IntegerField(verbose_name='ETH оплаченный резерв', default=0)
    KPFU_reserved_payed = models.IntegerField(verbose_name='KPFU оплаченный резерв', default=0)
    SOL_reserved_payed = models.IntegerField(verbose_name='SOL оплаченный резерв', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email

    def reserve_currency(self, currency: str, count: int):
        count = int(count)
        balance = getattr(self, currency)
        setattr(self, currency, balance - count)
        reserved_balnce = getattr(self, f'{currency}_reserved')
        setattr(self, f'{currency}_reserved', reserved_balnce + count)
        self.save()

    def reserve_payed_currency(self, currency: str, count: int):
        count = int(count)
        balance = getattr(self, f'{currency}_reserved')
        setattr(self, f'{currency}_reserved', balance - count)
        reserved_balnce = getattr(self, f'{currency}_reserved_payed')
        setattr(self, f'{currency}_reserved_payed', reserved_balnce + count)
        self.save()

    @property
    def balance(self) -> str:
        Course.update_courses()
        _balance = self.USDT + self.USDT_reserved
        for currency in ("BTC", "ETH", "KPFU", "SOL"):
            count = getattr(self, currency) + getattr(self, f'{currency}_reserved')
            price = Course.objects.get(currency=currency).USDT
            _balance += count * price
        litter = ''
        if _balance > 1000:
            _balance /= 1000
            litter = 'К'
            if _balance > 1000:
                _balance /= 1000
                litter = 'М'
        return f'{round(_balance, 1)}{litter} USDT'
