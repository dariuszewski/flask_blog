from datetime import datetime
from drinksblog import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    authority = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


    def __repr__(self):
        return f"User('{self.id},'{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    picture1 = db.Column(db.String(20), nullable=False, default='default.png')
    picture2 = db.Column(db.String(20))
    picture3 = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')




    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.user_id},'{self.post_id}', '{self.id}', '{self.content}')"

class Conversation(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
        user_2 = db.Column(db.Integer, db.ForeignKey('user.id'))
        messages = db.relationship('Message', backref='mail', lazy=True)

        def get_username(self, id):
            user = User.query.filter_by(id=id).first()
            return user.username

        def get_image_file(self, id):
            user = User.query.filter_by(id=id).first()
            return user.image_file

        def get_last_date(self, id):
            date = Message.query.filter_by(mail_id=self.id).order_by(Message.date_posted.desc()).first()
            return date.date_posted

        def get_status(self):
            status = Message.query.filter_by(is_read=True).all()
            return bool(status)

        def get_last_msg(self, id):
            msg = Message.query.filter_by(mail_id=self.id).order_by(Message.date_posted.desc()).first()
            return msg

        #<!--<small class="text-muted">{{ conversation.get_last_date(conversation.id).strftime('%Y-%m-%d %H:%M') }}</small>-->

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(140))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Integer, nullable=False, default=False)
    mail_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))


    def get_username(self, id):
        user = User.query.filter_by(id=id).first()
        return user.username

    def short(self):
        return 'Hello'

    def __repr__(self):
        return f'{self.content}'
