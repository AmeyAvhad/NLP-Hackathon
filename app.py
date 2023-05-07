from flask import Flask ,render_template ,request
from langdetect import detect
from textblob import TextBlob
import spacy

# Load pre-trained NER model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

language = ''
sentiment = ''
org = ''
contact =''

@app.route('/')
def index():
    return render_template('index.html',language=language,sentiment=sentiment,org=org,contact=contact)

# Function to detect the language of a given text
@app.route('/detect_language',methods=['GET','POST'])
def detect_language():
    text = str(request.form.get('input'))
    return render_template('index.html',language=str(detect(text)),sentiment=sentiment,org=org,contact=contact)

# Function to calculate sentiment polarity of a given text
@app.route('/calculate_sentiment',methods=['GET','POST'])
def calculate_sentiment():
    text = str(request.form.get('input'))
    blob = TextBlob(text)
    return render_template('index.html',language=language,sentiment=blob.sentiment.polarity,org=org,contact=contact)


# Function to extract organization entities from a given text
@app.route('/organization',methods=['GET','POST'])
def extract_organization_entities():
    text = str(request.form.get('input'))
    doc = nlp(text)
    organizations = []
    for entity in doc.ents:
        if entity.label_ == "ORG":
            organizations.append(entity.text)
    return render_template('index.html',language=language,sentiment=sentiment,org=str(organizations),contact=contact)

# Function to extract contact information from a given text
@app.route('/contact',methods=['GET','POST'])
def extract_contact_info():
    text = str(request.form.get('input'))
    # Extract phone numbers
    doc = nlp(text)


    phone_numbers = []
    for i in doc:
        if(i.like_num):
            phone_numbers.append(i)
    
    email_ids = []
    # Extract email IDs
    for i in doc:
        if(i.like_email):
            email_ids.append(i)
    # Extract names
    names=[]
    for i in doc:
        if(i.pos_ == 'PROPN'):
            names.append(i)

    return render_template('index.html',language=language,sentiment=sentiment,org=org,contact=[names,phone_numbers,email_ids])


app.run()