import sys

import dataset
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import time
from collections import defaultdict

# nltk.download('shakespeare')
# nltk.download('brown')
# nltk.download('punkt')

from config import DATABASE_URI

db = dataset.connect(DATABASE_URI)

#create_table = '''CREATE TABLE {} (text TEXT);'''.format(table_name)
#truncate_table = ''' DELETE FROM lines '''



def insert_brown_phrases(categories=None, cutoff=10000):
    from nltk.corpus import brown
    if not categories:
        categories=brown.categories()

    start_time = time.time()
    brown_table = db['brown']
    words = brown.words(categories=categories)
    print("importing brown words from categories {},"
          " w maximum word count of {}".format(categories, cutoff))
    # words have ',' separating each phrase
    import string

    cutoff = min(len(words), cutoff)
    insertions = 0
    db.begin()
    try:

        sentence = []
        for idx, w in enumerate(words[:cutoff]):
            if idx % 1000 == 0:
                print('processed {} words'.format(idx))
            if w[0] not in string.ascii_letters:
                sentence = ' '.join(sentence)
                brown_table.insert({'chunk': sentence})
                # print('skipped {}'.format(w))
                # print('dumped sentence {}'.format(sentence))
                sentence = []
                insertions += 1
                continue
            sentence.append(w)
        db.commit()
    except:
        db.rollback()
        print("error inserting data")
    end_time = time.time() - start_time
    print("Done, w {} phrase insertions, took {}s".format(insertions, end_time))


def insert_shakespeare_lines():
    table = db['speare_lines'] # will create table
    from nltk.corpus import shakespeare
    plays = [ shakespeare.xml(i) for i in shakespeare.fileids()]
    start_time = time.time()
    print(start_time)
    for p in plays[0:2]:
        lines = p.findall('*/*/*/LINE')
        for line in lines:
            line = line.text
            if line:
                line = line.replace("'","''")
                table.insert({'text':line})
                # db.query("INSERT INTO lines VALUES ('{}')".format(line))
        print("inserted {} values into db".format(len(lines)))
    # t.commit()
    print('took{}'.format((time.time() - start_time)))


def get_lines_from_play(amount=None):
    # table = db['quadgrams']
    from nltk.corpus import shakespeare
    plays = [ shakespeare.xml(i) for i in shakespeare.fileids()]
    all_lines = []
    for p in plays[0:2]:
        lines = p.findall('*/*/*/LINE')
        for l in lines:
            if amount and amount <= len(all_lines):
                return all_lines
            if len(all_lines) % 100 == 0:
                print("processed {} lines".format(len(all_lines)))
            all_lines.append(l.text)
    return all_lines

def get_word_quadgram_from_lines(lines):
    fails = []
    s = ''
    quad_dict = defaultdict(list)
    # store 5 quadgrams per key
    QUADGRAMS_PER_KEY = 5
    for line in lines:
        try:
            token=nltk.word_tokenize(line)
            quadgrams = ngrams(token,4)
            for quad in quadgrams:
                if len(quad_dict[quad[0].lower()]) > QUADGRAMS_PER_KEY:
                    continue
                quad_dict[quad[0].lower()].append(quad)
        except:
            fails.append(line)

    print("failed to quadgram {} lines".format(len(fails)))
    return quad_dict

def set_db_quadgrams(qd, amount=None):
    print('inserting keys ({})'.format(amount))
    table = db['quadgram'] # will create table
    db.begin()
    try:
        for idx, key in enumerate(qd.keys()):
            if idx % 10 == 0:
                print('set {} values in db'.format(idx))
            if amount and amount <= idx:
                break
            for q in qd[key]:
                table.insert({'one': key,
                              'two':q[1],
                              'three':q[2],
                              'four':q[3]})
        print('commited')
        db.commit()
    except:
        print("rolling back qd insertion")
        db.rollback()

def get_db_quadgrams(amount=None):
    table = db['quadgram']
    qd = defaultdict(list)
    if amount:
        quads = db.query('''SELECT root, one, two, three
                            FROM quadgram ORDER BY id
                             LIMIT {}'''.format(amount))
    else:
        quads = table.all()

    for quad in quads:
        qd[quad['one']].append([quad['one'], quad['two'], quad['three'], quad['four']])
    return qd


if __name__ == '__main__':

    if sys.argv[1] == 'setup':
        nltk.download('shakespeare')
        nltk.download('brown')
        nltk.download('punkt')

    if sys.argv[1] == 'gen-brown':
        # ['adventure', 'belles_lettres', 'editorial', 'fiction',
        #  'government', 'hobbies', 'humor', 'learned', 'lore',
        #  'mystery', 'news', 'religion', 'reviews', 'romance',
        #  'science_fiction']

        cutoff = int(sys.argv[2]) if len(sys.argv) == 3 else 10000
        insert_brown_phrases(categories=['adventure', 'lore',
                                         'belles_lettres',
                                         'romance','science_fiction'],
                             cutoff=cutoff)

    if sys.argv[1] == 'gen-speare':
        lines = get_lines_from_play(amount=1000)
        qd = get_word_quadgram_from_lines(lines)
        print('generated quads: {}'.format(len(qd.keys())))

        set_db_quadgrams(qd)

    if sys.argv[1] == 'stat':
        qd2 = get_db_quadgrams()
        print('fetched quads: {}'.format(len(qd2.keys())))





