#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os


import nltk
from xml.etree import ElementTree
nltk.download('shakespeare')
nltk.download('brown')
from nltk.corpus import brown, shakespeare

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():

    return render_template('pages/placeholder.home.html')



@app.route('/words')
def words():

    categories = brown.categories()
    return render_template('pages/words.html',
                            categories=categories)

@app.route('/words/<category>')
def word_category(category='lore'):

    words = brown.words(categories=category)

    return render_template('pages/word_category.html', category=category,
                           words=words[0:100])

@app.route('/speare')
def speare():

    plays = []
    for idx,play_name in enumerate(shakespeare.fileids()):
        play = shakespeare.xml(play_name)
        plays.append( {'name': play[0].text,
                       'id': idx})

    return render_template('pages/speare.html',
                            plays=plays)

@app.route('/speare/<play_id>')
def speare_play(play_id):
    ##http://www.nltk.org/howto/corpus.html

    plays = shakespeare.fileids()
    play = shakespeare.xml(plays[int(play_id)])

    act_elems = []
    for p in play.findall('ACT'):
        element_text = p.itertext()
        element_text = list(element_text)
        act_elems.append((p.tag, element_text))

    personae = [persona.text for persona in
            play.findall('PERSONAE/PERSONA')]

    return render_template('pages/speare_play.html',
                           title=play[0].text,
                           personae=personae,
                           act_elems=act_elems)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
