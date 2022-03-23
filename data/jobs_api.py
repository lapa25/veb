import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'user.name', 'work_size',
                                    'collaborators', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_news(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('team_leader', 'job', 'user.name', 'work_size',
                                       'collaborators', 'is_finished'
                                       ))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    sp = []
    for elem in jobs:
        sp.append(elem.id)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'collaborators', 'is_finished', 'work_size']):
        return jsonify({'error': 'Bad request'})
    elif request.json['id'] in sp:
        return jsonify({'error': 'Id already exists'})
    elif not request.json['id'].isdigit() or not request.json['work_size'].isdigit() or \
            not request.json['team_leader'].isdigit():
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        work_size=request.json['work_size']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET', 'POST'])
def edit_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    elif not request.json:
        return jsonify({'error': 'Empty request'})
    if 'team_leader' in request.json:
        jobs.team_leader = request.json['team_leader']
    if 'job' in request.json:
        jobs.job = request.json['job']
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    if 'work_size' in request.json:
        jobs.work_size = request.json['work_size']
    db_sess.commit()
    return jsonify({'success': 'OK'})
