import records
import dataset
import nltk
import time
from xml.etree import ElementTree
# nltk.download('shakespeare')
# nltk.download('brown')

from config import DATABASE_URI

# db = records.Database(DATABASE_URI)
db = dataset.connect(DATABASE_URI)

table_name = 'lines_nose'
#create_table = '''CREATE TABLE {} (text TEXT);'''.format(table_name)
#truncate_table = ''' DELETE FROM lines '''

#db.query(create_table)


def insert_brown_phrases():
    from nltk.corpus import brown

    start_time = time.time()
    brown_table = db['brown']
    words = brown.words(categories=brown.categories())

    # words have ',' separating each phrase
    import string
    sentence = []
    for w in words[2000:10000]:
        if w[0] not in string.ascii_letters:
            sentence = ' '.join(sentence)
            brown_table.insert({'chunk': sentence})
            # print('skipped {}'.format(w))
            # print('dumped sentence {}'.format(sentence))
            sentence = []
            continue
        sentence.append(w)


def insert_shakespeare_lines():
    table = db[table_name] # will create table
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


def get_lines_from_play():
    # table = db['quadgrams']
    from nltk.corpus import shakespeare
    plays = [ shakespeare.xml(i) for i in shakespeare.fileids()]
    start_time = time.time()
    print(start_time)
    all_lines = []
    for p in plays[0:2]:
        lines = p.findall('*/*/*/LINE')
        for l in lines:
            all_lines.append(l.text)
    return all_lines

def get_word_quadgram_from_lines(lines):
    import nltk
    from nltk import word_tokenize
    from nltk.util import ngrams
    fails = []
    s = ''
    from collections import defaultdict
    quad_dict = defaultdict(list)
    for line in lines:
        try:
            token=nltk.word_tokenize(line)
            quadgrams = ngrams(token,4)
            for quad in quadgrams:
                quad_dict[quad[0].lower()].append(quad)
        except:
            fails.append(line)

    print("failed {} lines".format(len(fails)))
    if len(fails) > 5:
        print(fails[0:5])
    return quad_dict

if __name__ == '__main__':
    lines = get_lines_from_play()
    # import ipdb; ipdb.set_trace();
    qd = get_word_quadgram_from_lines(lines)
    print(len(qd.keys()))
    # if input('populate lines table (y/n)?: ') == 'y':
    #     insert_shakespeare_lines()
    pass




