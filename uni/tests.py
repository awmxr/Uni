import re

def starfunc(a):
    b3 = re.search(r'\b +\b',a)
    d3 = re.search(r'^ *',a)
    g3 = re.search(r' *$',a)
    g4 = re.search('\d+$',a)

    if b3:
        a = re.sub(r'\b +\b',' ',a)
    if d3:
        a = re.sub(r'^ *','',a)
    if g3:
        a = re.sub(r' +$',' ',a)
    if g4:
        a += ' '
    
    return a



b = ' 12  13  14    '
b = starfunc(b)
b += 'amir'
print(b)