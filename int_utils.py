__switch_mod_100 = {
    11: 'th',
    12: 'th',
    13: 'th',
}
__switch = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

def nth(n: int):
    return '{}{}'.format(n, __switch_mod_100.get(n % 100, __switch.get(n % 10, 'th')))
