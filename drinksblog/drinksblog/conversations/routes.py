from flask import render_template, url_for, flash, redirect, Blueprint
from datetime import datetime
from drinksblog import db
from drinksblog.models import User, Message, Conversation
from drinksblog.conversations.forms import MessageForm
from flask_login import current_user, login_required

conversations = Blueprint('conversations', __name__)

@conversations.route("/chat/<string:recipient>", methods=['GET', 'POST'])
@login_required
def chat(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()

    if Conversation.query.filter_by(user_1=user.id, user_2=current_user.id).first() != None:
        conversation = Conversation.query.filter_by(user_1=user.id, user_2=current_user.id).first()
    elif Conversation.query.filter_by(user_1=current_user.id, user_2=user.id).first() != None:
        conversation = Conversation.query.filter_by(user_1=current_user.id, user_2=user.id).first()
    else:
        conversation = Conversation(user_1=current_user.id, user_2=user.id)
        db.session.add(conversation)
        db.session.commit()

    conv_id = conversation.id

    messages = Message.query.filter_by(mail_id=conv_id).order_by(Message.date_posted).all()

    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      content=form.content.data, mail_id=conv_id)

        db.session.add(msg)
        db.session.commit()

        flash('Wiadomość wysłana!', 'success')
        return redirect(url_for('conversations.chat', recipient=recipient, form=form, messages=messages))

    return render_template('chat.html', recipient=recipient, form=form, messages=messages)

#edit start
@conversations.route('/messages')
@login_required
def messages():
    conv1 = Conversation.query.filter_by(user_1=current_user.id).all()
    conv2 = Conversation.query.filter_by(user_2=current_user.id).all()
    conversations = conv1 + conv2

    return render_template('messages.html', conversations=conversations)
