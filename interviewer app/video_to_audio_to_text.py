
import sys
from moviepy.editor import *
video = VideoFileClip('test.mp4')
audio = video.audio
audio.write_audiofile('./test.wav')



from pydub import AudioSegment
import os
song = AudioSegment.from_wav("C:/Users/Nimish/Documents/Flasktut/hirebot/test.wav")
song.export("test.flac",format = "flac")



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

with open('ans.txt','w') as f:
    f.write(text)
    
