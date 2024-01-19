def oddeven(num):
    if num % 2 == 0:
        return True
    else:
        return False
    
result = oddeven(102817218)
print(result)

def is_adult(age):
    if age > 20:
        print('성인입니다')
    elif age >= 13:
        print('청소년이에요')
    else:
        print('어린이네요!')

is_adult(21)