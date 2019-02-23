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
`python -m spacy download en`

