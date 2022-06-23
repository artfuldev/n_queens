__mod_100_nth = {
    11: 'th',
    12: 'th',
    13: 'th',
}
__nth = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

def nth(n: int):
    return '{}{}'.format(n, __mod_100_nth.get(n % 100, __nth.get(n % 10, 'th')))
