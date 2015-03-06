# -*- coding: utf-8 -*-
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import QuestionForm, AnswerForm
from models import User, Question, Answer


from datetime import date
import md5

from flask import render_template, flash, request, redirect, url_for, abort
from flask.ext.login import (login_user, login_required, logout_user,
                             current_user)
from flask.ext.mail import Message





@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    questions = db.session.query(Question).all()

    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           questions = questions)



@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/question', methods=['GET', 'POST'])
def question():
    form = QuestionForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All field are required.')
            return render_template('question.html', form=form)
        else:
            question = Question(
                text=form.text.data,
                user=current_user
                )
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('question.html', form=form)



def _get_user_object_or_404(model, object_id, user, code=404):
    ''' get an object by id and owner user or raise an abort '''
    result = model.query.filter_by(id=object_id).first()
    return result or abort(code)



@app.route('/answer/<int:question_id>/', methods=['GET', 'POST'])
@login_required
def write_answer(question_id):
    question = _get_user_object_or_404(Question, question_id, current_user)
    form = AnswerForm(user=current_user, question=request.args.get('question'))

    if request.method == 'POST':
        if form.validate() == False:
            flash('All field are required.')
            return render_template('answer.html', form=form, question=question)
        else:
            answer = Answer(
                text=form.text.data,
                question_id=question.id,
                user=current_user
            )
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('answer.html', form=form, question=question)



@app.route('/view_answer/<int:question_id>/')
def view_answers(question_id):
    question = Question.query.filter_by(id=question_id).all()
    answers = Answer.query.filter_by(question_id=question_id).all()
    return render_template('view_answer.html', answers=answers, question=question)



@app.route('/questions/<int:question_id>/')
@login_required
def question_answers(question_id):
    question = _get_user_object_or_404(Question, question_id, current_user)
    answers = Answer.query.filter_by(question_id=question.id).all()
    return render_template('answer_list.html', question=question, answers=answers)


@app.route('/answer/<int:answer_like>/')
@login_required
def add_like(answer_like):
    return None

