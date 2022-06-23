__nth_100 = {
    11: 'th',
    12: 'th',
    13: 'th',
}
__nth_10 = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

def nth(n: int):
    return '{}{}'.format(n, __nth_100.get(n % 100, __nth_10.get(n % 10, 'th')))
