from flask import Flask
from flask import render_template
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
                address=form.address.name
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
        return render_template('register.html', title='Регистрация', form=form)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
