from flask import Flask
from flask import render_template, redirect, request, abort
from data import db_session, users_resource, jobs_resource
from data.jobs import Jobs
from data.users import User
from data.department import Department
from data.category import Category
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.job import JobForm
from forms.department import DepartmentForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api
import requests

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    @app.route('/')
    def index():
        work = db_sess.query(Jobs)
        return render_template("works.html", works=work)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                surname=form.surname.data,
                age=form.age.data,
                position=form.position.data,
                speciality=form.speciality.data,
                city_from=form.city_from.data,
                address=form.address.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
        return render_template('register.html', title='Регистрация', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/addjob', methods=['GET', 'POST'])
    @login_required
    def add_jobs():
        form = JobForm()
        if form.validate_on_submit():
            jobs = Jobs()
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            current_user.jobs.append(jobs)
            category = Category()
            if int(form.work_size.data) <= 24:
                category.name = '1'
            elif int(form.work_size.data) > 72:
                category.name = '3'
            else:
                category.name = '2'
            jobs.categories.append(category)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('addjob.html', title='Adding a job',
                               form=form)

    @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_jobs(id):
        form = JobForm()
        if request.method == "GET":
            jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                              ((Jobs.user == current_user) | (current_user.id == 1))).first()
            if jobs:
                form.job.data = jobs.job
                form.team_leader.data = jobs.team_leader
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
                form.is_finished.data = jobs.is_finished
            else:
                abort(404)
        if form.validate_on_submit():
            jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                              ((Jobs.user == current_user) | (current_user.id == 1))).first()
            if jobs:
                jobs.job = form.job.data
                jobs.team_leader = form.team_leader.data
                jobs.work_size = form.work_size.data
                jobs.collaborators = form.collaborators.data
                jobs.is_finished = form.is_finished.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('addjob.html',
                               title='Edit Job',
                               form=form
                               )

    @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def jobs_delete(id):
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1))).first()
        if jobs:
            db_sess.delete(jobs)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')

    @app.route('/departments')
    def departments():
        department = db_sess.query(Department)
        return render_template("departments.html", departments=department)

    @app.route('/adddepartment', methods=['GET', 'POST'])
    @login_required
    def add_department():
        form = DepartmentForm()
        if form.validate_on_submit():
            department = Department()
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.add(department)
            db_sess.commit()
            return redirect('/departments')
        return render_template('adddepartment.html', title='Adding a department',
                               form=form)

    @app.route('/departments/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_departments(id):
        form = DepartmentForm()
        if request.method == "GET":
            dep = db_sess.query(Department).filter(Department.id == id).first()
            if dep:
                form.title.data = dep.title
                form.chief.data = dep.chief
                form.members.data = dep.members
                form.email.data = dep.email
            else:
                abort(404)
        if form.validate_on_submit():
            dep = db_sess.query(Department).filter(Department.id == id).first()
            if dep:
                dep.title = form.title.data
                dep.chief = form.chief.data
                dep.members = form.members.data
                dep.email = form.email.data
                db_sess.commit()
                return redirect('/departments')
            else:
                abort(404)
        return render_template('adddepartment.html',
                               title='Edit Department',
                               form=form
                               )

    @app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def department_delete(id):
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            db_sess.delete(dep)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/users_show')

    @app.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
    def users_show(user_id):
        user = db_sess.query(User).filter(User.id == user_id).first()

        adress = user.city_from
        geocoder_request_1 = "http://geocode-maps.yandex.ru/1.x/" \
                             "?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + adress + ", 1&format=json"
        response_1 = requests.get(geocoder_request_1)
        json_response_1 = response_1.json()
        toponym_1 = json_response_1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = ','.join(toponym_1["Point"]["pos"].split(' '))
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": toponym_coodrinates,
            "l": "sat",
            "spn": "0.02,0.02"
        }
        response3 = requests.get(map_api_server, params=map_params)
        with open("static/img/map.png", "wb") as file:
            file.write(response3.content)
            file.close()

        return render_template('users_show.html',
                               title='Hometown',
                               pers=user
                               )



    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    app.run()


if __name__ == '__main__':
    main()
