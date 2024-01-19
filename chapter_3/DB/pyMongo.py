from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle

# db 연결 및 데이터 넣기
# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
# db.users.insert_one({'name':'bobby','age':21})
# db.users.insert_one({'name':'kay','age':27})
# db.users.insert_one({'name':'john','age':30})

# 모든 결과 값 보기
# MongoDB에서 데이터 모두 보기
all_users = list(db.users.find({}))
# # # 참고) MongoDB에서 특정 조건의 데이터 모두 보기
# same_ages = list(db.users.find({'age':21}))
# print(all_users[0])         # 0번째 결과값을 보기
# print(all_users[0]['name']) # 0번째 결과값의 'name'을 보기

# for user in all_users:      # 반복문을 돌며 모든 결과값을 보기
#     print(user)

# # 특정 결과 값 뽑기
# user = db.users.find_one({'name':'bobby'})
# print(user)
# # 그 중 특정 키 값을 빼고 보기
# user = db.users.find_one({'name':'bobby'},{'_id':False})
# print(user)
# 수정하기
# db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# user = db.users.find_one({'name':'bobby'})
# print(user)
# 삭제하기
# db.users.delete_one({'name':'bobby'})
# user = db.users.find_one({'name':'bobby'})
# print(user)
    
# 데이터 저장
# doc = {'name':'bobby', 'age':21}
# db.users.insert_one(doc)
# 데이터 한 개 찾기
# user = db.users.find_one({'name':'bobby'})
# print(user)
# 데이터 여러개 찾기
same_ages = list(db.users.find({'age':30},{'_id':False}))
print(same_ages)
# # 데이터 바꾸기
# db.users.update_one({'name':'kay'},{'$set':{'age':39}})
# # 데이터 지우기
# db.users.delete_one({'name':'john'})