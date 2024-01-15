people = [{'name' : 'bob', 'age': 20},
          {'name' : 'carry', 'age': 38},
          {'name' : 'john', 'age': 7},
          {'name' : 'smith', 'age': 17},
          {'name' : 'ben', 'age': 27}]

# for person in people:
#     if person['name'] == 'bob':
#         print(person['age'])

def print_age(Name):
    for person in people:
        if person['name'] == Name:
            return person['age']
    return '그런 이름은 없습니다!!'

print(print_age('hoyoung'))
print(print_age('smith'))
print(print_age('ben'))
print(print_age('carry'))
print(print_age('taeyoung'))