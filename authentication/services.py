from .models import User


def get_user_data(user: User) -> list:
    currencies = ("USDT", "ETH", "BTC", "SOL", "KPFU")
    data = []
    for currency in currencies:
        data.append({
        'name': currency,
        'value': f'''{getattr(user, currency) + getattr(user, f"{currency}_reserved")} {currency}{f" ({getattr(user, f'{currency}_reserved')} в резерве)" if getattr(user, f"{currency}_reserved")  else ""}''',
    })
    return data