from flask import Flask
from flask import render_template
from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    @app.route('/')
    def index():
        work = db_sess.query(Jobs)
        return render_template("works.html", works=work)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
