from functools import wraps
from logging.config import dictConfig

from flask import Flask, redirect, render_template, request, session, url_for

from forms import build_form
from helpers import QuizEnded
from quiz import Quiz
from users import UsersFromJSON


app = Flask(__name__)
app.config.from_object('settings')


def check_session_exist(func):
    @wraps(func)
    def check():
        if session.get('user'):
            return func()
        else:
            return redirect(url_for('login_get'))

    return check


def build_quiz():
    quiz = Quiz.from_json(session['data'])
    try:
        form = build_form(quiz.question)
        if request.method == 'GET':
            return render_template('quiz.html', form=form)
        elif form.validate_on_submit():
            quiz.pop_questions()
            form = build_form(quiz.question)
            session['data'] = quiz.to_json()
            return render_template('quiz.html',
                                   form=form,
                                   msg='Не, ну заебок же!')
        else:
            return render_template('quiz.html',
                                   form=form,
                                   msg='Миша, все хуйня, давай по новой!')
    except QuizEnded:
        return render_template('end.html')


@app.route('/', methods=['GET', 'POST'])
@check_session_exist
def quiz_worker():
    return build_quiz()


@app.route('/reload')
@check_session_exist
def reload():
    session['data'] = Quiz(file=app.config.get('QUIZ_FILE')).to_json()
    return redirect('/')


@app.post('/login')
def login_post():
    if users.check_login(request.form['user_name'], request.form['password']):
        session['user'] = request.form['user_name']
        session['data'] = Quiz(app.config.get('QUIZ_FILE')).to_json()
        session.permanent = True
        return redirect(url_for('quiz_worker'))
    else:
        return render_template('login.html'), 401


@app.get('/login')
def login_get():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', default=None)
    return redirect(url_for('login_get'))


if __name__ == '__main__':
    print(len([1,2,3]))
    dictConfig(app.config.get('LOGGING')) # type: ignore 
    app.logger.debug(f"App configuration:")
    for key, value in app.config.items():
        app.logger.debug(f"{key}: {value}")
    users = UsersFromJSON(app.config.get('USER_FILE')) # type: ignore 
    app.logger.debug(f"Known users: {', '.join(users.users.keys())}")
    app.run(host=app.config.get('APP_HOST'), port=app.config.get('APP_PORT'))
