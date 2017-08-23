#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import random
import os
import logging

import dataset
from flask import Flask, render_template, request




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#app.config.from_object('config')
from config import DATABASE_URI
db = dataset.connect(DATABASE_URI)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/placeholder.home.html')

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')



@app.route('/words')
def words():

    phrases = []
    i = random.randint(1,500)
    i2 = random.randint(i,i+200)
    result = db.query('''SELECT chunk FROM brown
                      WHERE id > {} AND id < {}
                      '''.format(i,i2))

    for row in result:
        if row['chunk'] == '':
            continue
        row2 = next(result, None)
        if row2:
            phrases.append([row['chunk'], row2['chunk']])


    return render_template('pages/words.html',
                            phrases=phrases)


from flask import jsonify

import generate_data as gd
import pickle
try:
    qd = pickle.load(open( "save.p", "rb" ))
except:
    all_lines = gd.get_lines_from_play()
    qd = gd.get_word_quadgram_from_lines(all_lines)
    pickle.dump(qd, open( "save.p", "wb" ))

@app.route('/speare/api/<word>')
def speare_word_api(word):
    word = word.lower()
    try:
        phrases = qd[word]
    except:
        print('word not found')
        phrases = []

    d = {'word': word, 'phrases': phrases}
    return jsonify(d)

@app.route('/speare')
def speare():
    words_available = len(qd.keys())
    best_words = [] # figure out offline
    return render_template('pages/speare.html',
                            best_words=best_words,
                            words_available=words_available)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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
