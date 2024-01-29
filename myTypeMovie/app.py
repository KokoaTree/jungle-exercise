from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider
import json
import sys
app = Flask(__name__)
client = MongoClient('mongodb://user:password@3.36.26.2', 27017)
db = client.dbjungle
#####################################################################################
# 이 부분은 코드를 건드리지 말고 그냥 두세요. 코드를 이해하지 못해도 상관없는 부분입니다.
# ObjectId 타입으로 되어있는 _id 필드는 Flask 의 jsonify 호출시 문제가 된다.
# 이를 처리하기 위해서 기본 JsonEncoder 가 아닌 custom encoder 를 사용한다.
# Custom encoder 는 다른 부분은 모두 기본 encoder 에 동작을 위임하고 ObjectId 타입만 직접 처리한다.


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


# 위에 정의되 custom encoder 를 사용하게끔 설정한다.
app.json = CustomJSONProvider(app)
# 여기까지 이해 못해도 그냥 넘어갈 코드입니다.
# #####################################################################################


@app.route('/')
def home():
    return render_template('index.html')
# 메인 페이지 기본 정렬(좋아요 순서)
# client에서 요청한 정렬 방식 확인


@app.route('/api/list', methods=['GET'])
def show_movies():
    sort_type = request.args.get('sort_type', 'likes')
    # 좋아요, 누적관객수, 개봉일자에 따라 정렬(오름차순)
    if sort_type == 'likes':
        movies = list(db.movies.find({'trashed': False}).sort([('likes', -1)]))
    elif sort_type == 'viewers':
        movies = list(db.movies.find(
            {'trashed': False}).sort([('viewers', -1)]))
    elif sort_type == 'date':
        # 개봉일은 연(year),월(month),일(day) 순서로 정렬(오름차순)
        movies = list(db.movies.find({'trashed': False}).sort(
            [('open_year', -1), ('open_month', -1), ('open_day', -1)]))
    else:
        # 정의되지 않은 정렬 방식이 요청되면 실패 메시지 반환
        return jsonify({'result': 'failure', 'msg': '유효하지 않은 정렬'})
    # 성공하면 success 메시지, movies_list 목록을 클라이언트에 전달
    return jsonify({'result': 'success', 'movies_list': movies})

# 영화에 좋아요 카운트 1 증가


@app.route('/api/likes', methods=['POST'])
def like_movie():
    # 클라이언트로부터 영화 제목을 받습니다.
    title = request.json.get('post_title')
    if not title:
        return jsonify({'result': 'failure', 'msg': '영화 제목이 없음'}), 400

    # movies 목록에서 title을 사용하여 영화 하나를 찾습니다.
    movie = db.movies.find_one({'title': title})
    if not movie:
        return jsonify({'result': 'failure', 'msg': '영화를 찾을 수 없음'}), 404

    # movie의 likes에 1을 더하기
    new_likes = movie.get('likes', 0) + 1
    # movies 목록에서 title이 매칭되는 영화의 likes를 new_likes로 변경
    result = db.movies.update_one(
        {'title': title}, {'$set': {'likes': new_likes}})

    # 하나의 영화만 영향을 받아야 하므로 result.modified_count 가 1이면 result = success 를 보냄
    if result.modified_count == 1:
        return jsonify({'result': 'success', 'likes': new_likes})
    else:
        return jsonify({'result': 'failure', 'msg': '업데이트 실패'}), 500

# 클라이언트에게 받은 정보를 GET으로 처리


@app.route('/api/list/trash', methods=['GET'])
def get_trash_movies():
    sortType = request.args.get('sort_type', 'likes')

    # 휴지통에 있는(trashed가 True인) 영화들을 sortType 따라 정렬
    if sortType == 'likes':
        movies = list(db.movies.find({'trashed': True}).sort('likes', -1))
    elif sortType == 'viewers':
        movies = list(db.movies.find({'trashed': True}).sort('viewers', -1))
    elif sortType == 'date':
        movies = list(db.movies.find({'trashed': True}).sort(
            [('open_year', -1), ('open_month', 1), ('open_day', 1)]))
    else:
        return jsonify({'result': 'failure', 'msg': '유효하지 않은 정렬 방식입니다.'}), 400

    return jsonify({'result': 'success', 'movies_list': movies})

# 클라이언트에게 받은 정보를 POST으로 처리(휴지통으로 보내기)


@app.route('/api/update/trash', methods=['POST'])
def trash_movie():
    title = request.form['post_title']
    result = db.movies.update_one(
        {'title': title}, {'$set': {'trashed': True}})

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure', 'msg': '휴지통으로 보내기 실패'}), 500

# 클라이언트에게 받은 정보를 POST으로 처리(휴지통에서 복구하기)


@app.route('/api/update/restore', methods=['POST'])
def restore_movie():
    title = request.form['post_title']
    result = db.movies.update_one(
        {'title': title}, {'$set': {'trashed': False}})

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure', 'msg': '복구 실패'}), 500


@app.route('/api/update/delete', methods=['POST'])
def delete_movie():
    title = request.form['post_title']
    result = db.movies.delete_one({'title': title})

    if result.deleted_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure', 'msg': '삭제 실패'}), 500


if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)
