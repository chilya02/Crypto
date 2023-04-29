from django.db import models
from authentication.models import User

currencies = (("USDT", 'usdt'), ('BTC', 'btc'), ('ETH', 'eth'), ('KPFU', 'kpfu'), ('SOL', 'sol'))
banks = (("TN", "Тинькофф"), ("SB", "Сбер"))


class Post(models.Model):
    currency = models.CharField(verbose_name='Валюта', choices=currencies, max_length=4)
    limit = models.IntegerField(verbose_name='Лимит')
    price = models.FloatField(verbose_name='Цена')
    bank = models.CharField(verbose_name='Банк', choices=banks, max_length=2)

    class Meta:
        abstract = True

    def remove(self):
        self.delete()


class SellPost(Post):
    id = models.AutoField(verbose_name='id', primary_key=True)
    user = models.ForeignKey(User, related_name='sell_posts', on_delete=models.CASCADE)
    card_number = models.IntegerField(verbose_name='Номер карты')

    @property
    def has_payed_orders(self) -> bool:
        orders = self.new_orders.filter(payed=True)
        if orders:
            return True
        return False

    def remove(self):
        self.user.reserve_currency(self.currency, -self.limit)
        super().remove()


class BuyPost(Post):
    user = models.ForeignKey(User, related_name='buy_posts', on_delete=models.CASCADE)
    id = models.AutoField(verbose_name='id', primary_key=True)

    @property
    def has_payed_orders(self) -> bool:
        orders = self.new_orders.filter(payed=True)
        if orders:
            return True
        return False


class NewOrder(models.Model):
    id = models.AutoField(primary_key=True)
    post_type = models.CharField(verbose_name='Тип поста', max_length=4)
    buy_post = models.ForeignKey(BuyPost, on_delete=models.CASCADE, related_name='new_orders', blank=True, default=None,
                                 null=True)
    sell_post = models.ForeignKey(SellPost, on_delete=models.CASCADE, related_name='new_orders', blank=True,
                                  default=None, null=True)
    count = models.IntegerField(verbose_name='Количество', blank=True, null=0, default=1)
    buyer = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='new_buy_orders'
    )
    seller = models.ForeignKey(
        User,
        verbose_name='Продавец',
        on_delete=models.CASCADE,
        related_name='new_sell_orders'
    )
    payed = models.BooleanField(verbose_name='Факт оплаты', default=False)
    change = models.BooleanField(verbose_name='Возможность редактирования', default=True)
    card_number = models.IntegerField(verbose_name='Номер карты', blank=True, default=None, null=True)
    REQUIRED_FIELDS = ['payed', 'seller', 'buyer', 'post_type']

    @classmethod
    def create(cls, post: Post, count: int, seller: User | None = None, buyer: User | None = None, payed: bool = False, change: bool = True):
        if isinstance(post, BuyPost):
            return cls(buyer=post.user, seller=seller, buy_post=post, post_type='buy', payed=payed, count=count, change=change)
        else:
            return cls(buyer=buyer, seller=post.user, sell_post=post, post_type='sell', payed=payed,count=count, change=change, card_number=post.card_number)

    @property
    def post(self):
        if self.post_type == 'buy':
            return self.buy_post
        elif self.post_type == 'sell':
            return self.sell_post

    @property
    def client(self):
        if self.post_type == 'buy':
            return self.seller
        elif self.post_type == 'sell':
            return self.buyer

    @property
    def sum(self) -> float:
        price = self.post.price
        order_sum = round((self.count * price), 2)
        if (order_sum % 1) == 0.0:
            return int(order_sum)
        return order_sum

    def pay(self, was_reserved: bool = False) -> None:
        self.payed = True
        self.change = False
        self.seller.reserve_payed_currency(self.post.currency, self.count)
        self.post.limit -= self.count
        self.post.save()

    def get_other_side(self, user: User) -> User:
        if self.seller == user:
            return self.buyer
        return self.seller

    def check_count(self, user_limit: int | None = None):
        if self.change:
            if user_limit is None:
                if self.count > self.post.limit:
                    self.count = self.post.limit
            elif self.count > min(self.post.limit, user_limit):
                self.count = min(self.post.limit, user_limit)
            self.save()

    def close_order(self):
        buyer_balance = getattr(self.buyer, self.post.currency)
        setattr(self.buyer, self.post.currency, buyer_balance + self.count)
        seller_balance = getattr(self.seller, f'{self.post.currency}_reserved_payed')
        setattr(self.seller, f'{self.post.currency}_reserved_payed', seller_balance - self.count)
        self.buyer.save()
        self.seller.save()


class Message(models.Model):
    order = models.ForeignKey(NewOrder, verbose_name='Ордер', on_delete=models.CASCADE, related_name='messages')
    from_user = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE,
                                  related_name='sent_messages')
    text = models.TextField(verbose_name='Текст')


class Order(models.Model):

    @classmethod
    def create(cls, order: NewOrder):
        return cls(
            buyer=order.buyer,
            seller=order.seller,
            price=order.post.price,
            currency=order.post.currency,
            count=order.count,
            sum=order.sum
        )

    id = models.AutoField(primary_key=True)
    price = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(verbose_name='Валюта', choices=currencies, max_length=4)
    sum = models.IntegerField(verbose_name='Сумма')
    count = models.IntegerField(verbose_name='Количество')
    buyer = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='buy_orders'
    )
    seller = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='sell_orders'
    )

    def get_other_side(self, user: User) -> User:
        if self.seller == user:
            return self.buyer
        return self.seller

    def __str__(self) -> str:
        return f'{self.seller} => {self.buyer} {self.count} {self.currency}'
