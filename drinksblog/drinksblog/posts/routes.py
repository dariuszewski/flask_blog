from flask import (render_template, url_for, flash, redirect, request, abort,
                    Blueprint)
from flask_login import login_user, current_user, login_required
from drinksblog import db
from drinksblog.posts.forms import PostForm, CommentForm
from drinksblog.models import Post, Comment
from drinksblog.users.utils import save_picture


from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route("/post_type", methods=['GET', 'POST'])
@login_required
def post_type():
    return render_template('post_type.html', title='Rodzaj posta')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():



        post = Post(title=form.title.data, content=form.content.data,
         author=current_user)


        db.session.add(post)
        db.session.commit()
        try:
            post.picture1 = save_picture(form.picture1.data, 'post_pics', (300, 300))
        except:
            pass
        try:
            post.picture2 = save_picture(form.picture2.data, 'post_pics', (300, 300))
        except:
            pass
        try:
            post.picture3 = save_picture(form.picture3.data, 'post_pics', (300, 300))
        except:
            pass

        db.session.commit()

        flash('Wpis został dodany!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="Nowy Post", form=form,
                        legend='Dodaj Wpis')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post=post)

    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                        author=current_user, post=post)

        db.session.add(comment)
        db.session.commit()
        flash('Twój komentarz został dodany!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    return render_template('post.html', title=post.title, post=post,
                        comments=comments, form=form)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        try:
            post.picture1 = save_picture(form.picture1.data, 'post_pics', (300, 300))
        except:
            pass
        try:
            post.picture2 = save_picture(form.picture2.data, 'post_pics', (300, 300))
        except:
            pass
        try:
            post.picture3 = save_picture(form.picture3.data, 'post_pics', (300, 300))
        except:
            pass

        db.session.commit()

        flash('Wpis został zaktualizowany!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Aktualizuj wpis')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Wpis został usunięty!', 'success')
    return redirect(url_for('main.home'))
