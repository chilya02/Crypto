# Generated by Django 4.1.3 on 2022-12-14 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyPost',
            fields=[
                ('currency', models.CharField(choices=[('USDT', 'usdt'), ('BTC', 'btc'), ('ETH', 'eth'), ('KPFU', 'kpfu'), ('SOL', 'sol')], max_length=4, verbose_name='Валюта')),
                ('limit', models.IntegerField(verbose_name='Лимит')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('bank', models.CharField(choices=[('TN', 'Тинькофф'), ('SB', 'Сбер')], max_length=2, verbose_name='Банк')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellPost',
            fields=[
                ('currency', models.CharField(choices=[('USDT', 'usdt'), ('BTC', 'btc'), ('ETH', 'eth'), ('KPFU', 'kpfu'), ('SOL', 'sol')], max_length=4, verbose_name='Валюта')),
                ('limit', models.IntegerField(verbose_name='Лимит')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('bank', models.CharField(choices=[('TN', 'Тинькофф'), ('SB', 'Сбер')], max_length=2, verbose_name='Банк')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('card_number', models.IntegerField(verbose_name='Номер карты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('currency', models.CharField(choices=[('USDT', 'usdt'), ('BTC', 'btc'), ('ETH', 'eth'), ('KPFU', 'kpfu'), ('SOL', 'sol')], max_length=4, verbose_name='Валюта')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_orders', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_orders', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
        ),
        migrations.CreateModel(
            name='NewOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_type', models.CharField(max_length=4, verbose_name='Тип поста')),
                ('payed', models.BooleanField(default=False, verbose_name='Факт оплаты')),
                ('card_number', models.IntegerField(blank=True, default=None, null=True, verbose_name='Номер карты')),
                ('buy_post', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='new_orders', to='p2p.buypost')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_buy_orders', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('sell_post', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='new_orders', to='p2p.sellpost')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_sell_orders', to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended_messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='p2p.neworder', verbose_name='Сообщение')),
            ],
        ),
    ]
