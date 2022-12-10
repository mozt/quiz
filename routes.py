from flask import Flask, render_template, redirect, url_for, request, session, render_template_string
from quiz import PopQuiz, Quiz
from hashlib import sha256
import datetime
import json
import os

APP_HOST = os.getenv('APP_HOST','127.0.0.1')
APP_PORT = os.getenv('APP_PORT', 8080)
DEBUG = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
SECRET_KEY = 'Kgvb*&3dYJUKF^Sv12ecys'
QUIZ_FILE = './quiz.json'
USER_FILE = './users.json'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if session.get('user'):
        data = Quiz.fromJSON(session['data'])
        try:
            if request.method == 'GET':
                PopQuiz.builder(data)
            form = PopQuiz()
            if form.validate_on_submit():
                PopQuiz.builder(data)
                form = PopQuiz()
                session['data'] = data.toJSON()
                return render_template('quiz.html', form=form, msg='Не, ну заебок же!')
            else:
                if request.method == 'GET':
                    session['data'] = data.toJSON()
                    return render_template('quiz.html', form=form)
                else:
                    return render_template('quiz.html', form=form, msg='Миша, все хуйня, давай по новой!')
        except IndexError:
            return render_template('end.html')
    else:
        return redirect(url_for('login'))
    
@app.get('/reload')
def reload():
    if session.get('user'):
        data = Quiz(file=app.config.get('QUIZ_FILE'))
        session['data'] = data.toJSON()
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            if sha256(request.form['password'].encode()).hexdigest() == users[request.form['user_name']]:
                session['user'] = request.form['user_name']
                data = Quiz(app.config.get('QUIZ_FILE'))
                session['data'] = data.toJSON()
                session.permanent = True
                return redirect(url_for('quiz'))
        except KeyError:
            return redirect(url_for('login'))
    return """
        <h1>LOGIN</h1>
        <form method="post">
        <table width="600" border="0">
            <tr>
            <td align="right"> <label for="user">Enter your username (email):</label></td>
            <td align="left"><input type="email" id="user" name="user_name" required align="center"/></td> 
            </tr>
            <tr>
            <td align="right"> <label for="pass"> and password:</label></td>
            <td align="left"><input type="password" id="pass" name="password" required align="center"/></td>
            </tr> 
        </table>
        <button type="submit">Submit</button>
        </form>
        """

@app.route('/logout')
def logout():
    session.pop('user', default=None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with open(app.config.get('USER_FILE'), 'rt') as f:
        users = json.loads(f.read())
        f.close()
    app.run(host=app.config.get('APP_HOST'), port=app.config.get('APP_PORT'))