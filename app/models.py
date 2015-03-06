from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column('username', db.String(30), unique = True)
    password = db.Column('password', db.String(20))
    email = db.Column(db.String(120), unique = True)

    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)



class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('questions', lazy='dynamic'))


    def __repr__(self):
        return '<Question %r>' % (self.text)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text)
    like = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('answers', lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref=db.backref('answers', lazy='dynamic'))
