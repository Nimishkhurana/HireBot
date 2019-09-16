from flask import Flask,request,render_template,redirect,jsonify
import json
import * from tone_analysis

app = Flask(__name__)

text1 = open('ans1.txt','r').read()
text2 = open('ans2.txt','r').read()
text3 = open('ans3.txt','r').read()


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
