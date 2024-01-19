fruits = ['사과','배','배','감','수박','귤','딸기','사과','배','수박']


def fruitCnt(fruitVal):
    count = 0
    for fruit in fruits:
        if fruit == fruitVal:
            count += 1
    return count

apple_cnt = fruitCnt('사과')
print(apple_cnt)

waterMelon_cnt = fruitCnt('수박')
print(waterMelon_cnt)

preach_cnt = fruitCnt('배')
print(preach_cnt)

persimmon_cnt = fruitCnt('감')
print(persimmon_cnt)

orange_cnt = fruitCnt('귤')
print(orange_cnt)

strawberry_cnt = fruitCnt('딸기')
print(strawberry_cnt)
