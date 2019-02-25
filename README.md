# pyOrganizer
collection of python modules to extract information from texts using nlp and 
knowledge databases (dbpedia)

> For now, this repository is work in progress

The main script for now is topics_in_web.py


## setup

install the required packages for your system
for instance , ubuntu/debian distros:
`sudo apt-get install python3-venv python3-dev`

setup the python virtual env
`python3 -m venv <project_root_folder>`

activate the environment (from the project folder)
`source bin/activate`

install pip requirements
`pip install -r requirements.txt`


install nltk and spacy required resources
`python -c "import nltk; nltk.download('cess_esp')"`
`python -c "import nltk; nltk.download('stopwords')"`
`python -m spacy download en`


## USAGE
```
Topics in web: script to get dbpedia resources from a web page
USAGE:
    python topics_in_web.py URL [lang]


# example

python topics_in_web.py https://elpais.com/tecnologia/2019/02/25/actualidad/1551092139_314804.html
['Cada', 'vez']
    http://es.dbpedia.org/resource/Vez
['usuarios']
    http://es.dbpedia.org/resource/Usuario_(informática)
['smartphones']
    http://es.dbpedia.org/resource/Teléfono_inteligente
['vídeos']
    http://es.dbpedia.org/resource/Video

```

## Future work

* Index collections of any text documents based on dbpedia resources (for instance using ElasticSearch and Tika)
* Allow query indexed documents using sparql
* Semantic resources visualization using plotly




