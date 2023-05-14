def normalize_number(number: float) -> str:
    litter = ''
    if number > 1000:
        number /= 1000
        litter = 'К'
        if number > 1000:
            number /= 1000
            litter = 'М'
    return f'{round(number, 1)} {litter}'
