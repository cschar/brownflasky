#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import logging

import os
import dataset



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#app.config.from_object('config')
from config import DATABASE_URI
db = dataset.connect(DATABASE_URI)


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
    import random
    i = random.randint(1,50)
    result = db.query('''SELECT chunk FROM brown
                      WHERE id > {}
                      GROUP BY chunk LIMIT 30;'''.format(i))
    for row in result:
        row2 = next(result, '')
        phrases.append([row['chunk'], row2['chunk']])

    return render_template('pages/words.html',
                            phrases=phrases)

@app.route('/words/<category>')
def word_category(category='lore'):
    phrases = []
    lines = db['lines_nose'].all()
    for i in range(100):
        phrases.append(lines.next()['text'])

    return render_template('pages/word_category.html', category=category,
                           words=" ".join(phrases))




from flask import jsonify

import generate_data as gd
all_lines = gd.get_lines_from_play()
qd = gd.get_word_quadgram_from_lines(all_lines)

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

#
# @app.route('/speare')
# def speare():
#     from nltk.corpus import shakespeare
#     plays = []
#     for idx,play_name in enumerate(shakespeare.fileids()):
#         play = shakespeare.xml(play_name)
#         plays.append( {'name': play[0].text,
#                        'id': idx})
#
#     return render_template('pages/speare.html',
#                             plays=plays)
#
# @app.route('/speare/<play_id>')
# def speare_play(play_id):
#     ##http://www.nltk.org/howto/corpus.html
#     from nltk.corpus import shakespeare
#     plays = shakespeare.fileids()
#     play = shakespeare.xml(plays[int(play_id)])
#
#     act_elems = []
#     for p in play.findall('ACT'):
#         element_text = p.itertext()
#         element_text = list(element_text)
#         act_elems.append((p.tag, element_text))
#
#     personae = [persona.text for persona in
#             play.findall('PERSONAE/PERSONA')]
#
#     return render_template('pages/speare_play.html',
#                            title=play[0].text,
#                            personae=personae,
#                            act_elems=act_elems)

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
