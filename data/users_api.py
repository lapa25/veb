import flask
from flask import jsonify, request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_news(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('surname', 'name', 'age', 'position',
                                         'speciality', 'address', 'email'
                                         ))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET', 'POST'])
def edit_jobs(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Empty request'})
    if 'surname' in request.json:
        users.surname = request.json['surname']
    if 'name' in request.json:
        users.name = request.json['name']
    if 'age' in request.json:
        users.age = request.json['age']
    if 'position' in request.json:
        users.position = request.json['position']
    if 'speciality' in request.json:
        users.speciality = request.json['speciality']
    if 'email' in request.json:
        users.email = request.json['email']
    if 'address' in request.json:
        users.address = request.json['address']
    db_sess.commit()
    return jsonify({'success': 'OK'})
