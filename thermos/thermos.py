from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash

from forms import BookmarkForm

app = Flask(__name__)
bookmarks = []
app.config['SECRET_KEY'] = '\x80\xedU\xde\xca\x8f\xf8\xa8H\x15_\x9a\xa7\x98\xadRs\x05\xdb\xf9\xf6(\xec\x82'


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        user='vikas',
        date=datetime.utcnow(),
        description=description
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return '{}. {}.'.format(self.firstname[0], self.lastname[0])

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash("Stored '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
