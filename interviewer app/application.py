from flask import Flask,request,render_template,redirect,jsonify
import json
from ibm_watson import ToneAnalyzerV3

app = Flask(__name__)

video_path = "nimish.mp4"

text1 = open('ans1.txt','r').read()
text2 = open('ans2.txt','r').read()
text3 = open('ans3.txt','r').read()



tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='s5dlNRmCgOWKmStaFyhn17dehz0kCpqlk7UfRViT0TS9',
    url='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
)

tone_analysis1 = tone_analyzer.tone(
    {'text': text1},
    content_type='application/json'
).get_result()

tone_analysis2 = tone_analyzer.tone(
    {'text': text2},
    content_type='application/json'
).get_result()

tone_analysis3 = tone_analyzer.tone(
    {'text': text3},
    content_type='application/json'
).get_result()

document_tones1 = []
document_tones2 = []
document_tones3 = []
for dicts in tone_analysis1['document_tone']['tones']:
    document_tones1.append((dicts['tone_name'],dicts['score']))

traits1 = []
for pair in document_tones1:
    traits1.append(pair[0])

if 'Tentative' not in traits1:
    document_tones1.append(('Tentative',0.0))
if 'Analytical' not in traits1:
    document_tones1.append(('Analytical',0.0))
if 'Sadness' not in traits1:
    document_tones1.append(('Sadness',0.0))
if 'Confident' not in traits1:
    document_tones1.append(('Confident',0.0))
if 'Joy' not in traits1:
    document_tones1.append(('Joy',0.0))

print(document_tones1)

for dicts in tone_analysis2['document_tone']['tones']:
    document_tones2.append((dicts['tone_name'],dicts['score']))

traits2 = []
for pair in document_tones2:
    traits2.append(pair[0])

if 'Tentative' not in traits2:
    document_tones2.append(('Tentative',0.0))
if 'Analytical' not in traits2:
    document_tones2.append(('Analytical',0.0))
if 'Sadness' not in traits1:
    document_tones2.append(('Sadness',0.0))
if 'Confident' not in traits2:
    document_tones2.append(('Confident',0.0))
if 'Joy' not in traits2:
    document_tones2.append(('Joy',0.0))



print(document_tones2)

for dicts in tone_analysis3['document_tone']['tones']:
    document_tones3.append((dicts['tone_name'],dicts['score']))

traits3 = []
for pair in document_tones3:
    traits3.append(pair[0])

if 'Tentative' not in traits3:
    document_tones3.append(('Tentative',0.0))
if 'Analytical' not in traits3:
    document_tones3.append(('Analytical',0.0))
if 'Sadness' not in traits3:
    document_tones3.append(('Sadness',0.0))
if 'Confident' not in traits3:
    document_tones3.append(('Confident',0.0))
if 'Joy' not in traits3:
    document_tones3.append(('Joy',0.0))

for dicts in tone_analysis3['document_tone']['tones']:
    document_tones3.append((dicts['tone_name'],dicts['score']))


print(document_tones3)

document_tones = document_tones1+document_tones2+document_tones3


print(document_tones)

Analytical=[]
Tentative=[]
Sadness=[]
Joy=[]
Confident=[]
for pair in document_tones:
    if pair[0]=="Analytical":
        Analytical.append(pair[1])
    elif pair[0]=="Tentative":
        Tentative.append(pair[1])
    elif pair[0]=="Sadness":
        Sadness.append(pair[1])
    elif pair[0]=="Joy":
        Joy.append(pair[1])
    elif pair[0]=="Confident":
        Confident.append(pair[1])


res ={
        'Analytical':Analytical,
        'Tentative':Tentative,
        'Sadness':Sadness,
        'Joy':Joy,
        'Confident':Confident
    }
print(res)

@app.route('/',methods=['GET'])
def index():
    print(res)
    return render_template('index.html',res=res,txt1=text1,txt2=text2,txt3=text3)