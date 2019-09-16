##FOR TONE ANALYSIS


import sys
from moviepy.editor import *
video = VideoFileClip('test.mp4')
audio = video.audio
audio.write_audiofile('./test6.wav')



from pydub import AudioSegment
import os
song = AudioSegment.from_wav("C:/Users/Nimish/Documents/Flasktut/hirebot/test6.wav")
song.export("test8.flac",format = "flac")



from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import json


speech_to_text = SpeechToTextV1(
    iam_apikey='API_KEY',
    url='https://gateway-lon.watsonplatform.net/speech-to-text/api'
)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

with open('test5.flac','rb') as audio_file:
    audio_source = AudioSource(audio_file)
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/flac',
        word_alternatives_threshold=0.9,).get_result()
# print(json.dumps(speech_recognition_results, indent=2))

text=''
for dict_ in speech_recognition_results['results']:
    text=text+(dict_['alternatives'][0]['transcript']).capitalize()+'.'

with open('ans1.txt','w') as f:
    f.write(text)
    
import json
from ibm_watson import ToneAnalyzerV3


tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='s5dlNRmCgOWKmStaFyhn17dehz0kCpqlk7UfRViT0TS9',
    url='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
)


text = text



tone_analysis1 = tone_analyzer.tone(
    {'text': text},
    content_type='application/json'
).get_result()
# print(json.dumps(tone_analysis1, indent=2))
    
    
    
    
    
    

document_tones=[]
for dicts in tone_analysis1['document_tone']['tones']:
    document_tones.append((dicts['tone_name'],dicts['score']))
    
    
sentences_tone_pairs=[]
for total_sentences in tone_analysis1['sentences_tone']:
    a1=total_sentences['tones']
    for tones in a1:
        sentences_tone_pairs.append((tones['tone_name'],tones['score']))

Analytical=[]
Tentaive=[]
Sadness=[]
Joy=[]
Confident=[]
for pair in sentences_tone_pairs:
    if pair[0]=="Analytical":
        Analytical.append(pair)
    elif pair[0]=="Tentaive":
        Tentaive.append(pair)
    elif pair[0]=="Sadness":
        Sadness.append(pair)
    elif pair[0]=="Joy":
        Joy.append(pair)
    elif pair[0]=="Confident":
        Confidence.append(pair)
        
Analytical_count=len(Analytical)
Tentaive_count=len(Tentaive)
Sadness_count=len(Sadness)
Joy_count=len(Joy)
Confident_count=len(Confident)

def total_score(trait):
    c=0
    for pair in trait:
        s=pair[1]+c
        c=s
    return(c) 

Total_Analytical_Score=total_score(Analytical)
Total_Tentaive_Score=total_score(Tentaive)
Total_Sadness_Score=total_score(Sadness)
Total_Joy_Score=total_score(Joy)
Total_Confident_Score=total_score(Confident)
