## brown flasky

 nltk brown,shakespeare etc... corpus word experiments


## Install and Run

    conda create -n brownflasky python=3
    source activate brownflasky
    pip install -r requirements.txt
    conda install --file requirements-conda.txt
    
    python generate_data.py setup
    python generate_data.py gen-brown
    python generate_data.py gen-speare
    python generate_data.py stat
        
    python app.py


## ideas


- [ x ] build up tri-gram collection of shakespeare. 
      combine them into sentences ending in a noun
      http://www.nltk.org/howto/wordnet.html
      https://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
      https://stackoverflow.com/questions/28033882/determining-whether-a-word-is-a-noun-or-not
- [x] 

## Source
Forked from flask-boilerplate

