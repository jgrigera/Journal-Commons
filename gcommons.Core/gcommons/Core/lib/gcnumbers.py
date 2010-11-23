#ENGLISH only...

_known = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
    }
def _positive_spoken_number(n):
    """Assume n is a positive integer.
    >>> _positive_spoken_number(900)
    'nine hundred'
    >>> _positive_spoken_number(100)
    'one hundred'
    >>> _positive_spoken_number(100000000000)
    'one hundred billion'
    >>> _positive_spoken_number(1000000000000)
    'one trillion'
    >>> _positive_spoken_number(33000000000000)
    'thirty-three trillion'
    >>> _positive_spoken_number(34954523539)
    'thirty-four billion, nine hundred fifty-four million, five hundred twenty-three thousand, five hundred thirty-nine'
    """
    #import sys; print >>sys.stderr, n
    if n in _known:
        return _known[n]
    bestguess = str(n)
    remainder = 0
    if n<=20:
        assert 0
    elif n < 100:
        bestguess= _positive_spoken_number((n//10)*10) + '-' + \
                   _positive_spoken_number(n%10)
        return bestguess
    elif n < 1000:
        bestguess= _positive_spoken_number(n//100) + ' ' + 'hundred'
        remainder = n%100
    elif n < 1000000:
        bestguess= _positive_spoken_number(n//1000) + ' ' + 'thousand'
        remainder = n%1000
    elif n < 1000000000:
        bestguess= _positive_spoken_number(n//1000000) + ' ' + 'million'
        remainder = n%1000000
    elif n < 1000000000000:
        bestguess= _positive_spoken_number(n//1000000000) + ' ' + 'billion'
        remainder = n%1000000000
    else:
        bestguess= _positive_spoken_number(n//1000000000000)+' '+'trillion'
        remainder = n%1000000000000
    if remainder:
        if remainder >= 100: comma = ','
        else:                comma = ''
        return bestguess + comma + ' ' + _positive_spoken_number(remainder)
    else:
        return bestguess
    
def gcommons_spoken_number(n):
    """Return the number as it would be spoken, or just str(n) if unknown.
    >>> spoken_number(0)
    'zero'
    >>> spoken_number(1)
    'one'
    >>> spoken_number(2)
    'two'
    >>> spoken_number(-2)
    'minus two'
    >>> spoken_number(42)
    'forty-two'
    >>> spoken_number(-1011)
    'minus one thousand eleven'
    >>> spoken_number(1111)
    'one thousand, one hundred eleven'
    """
    if not isinstance(n, int) and not isinstance(n, long): return n
    if n<0:
        if n in _known: return _known[n]
        else:           return 'minus ' + _positive_spoken_number(-n)
    return _positive_spoken_number(n)
