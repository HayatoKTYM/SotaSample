#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template,request
host = '0.0.0.0'
#host = '192.168.10.108'
port = 5000
app = Flask(__name__)
from controller import action

message_list = {"a":"こんにちは",
                "b":"ありがとう",
                "c":"ごめんね",
                "d":"さようなら",
                "e":"よろしくお願いします",
                "f":"お名前を教えてください"
                }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['GET'])
def hello():
    #fname = request.form['message']
    message = "Hello World!"
    print(message)
    #rc.terminate(request.form['message'])
    return render_template('hello.html', message=message)

@app.route('/<command>/<detail>', methods=['POST'])
def push_button(command, detail):
    if command == 'look': #head_yを動かす
        print("head_y")

    elif command == 'head_p': #head_pを動かす
        print("head_p")
    elif command == 'incline': #head_rを動かす
        print("head_r")
    elif 'elbo' in command : #elb_r or elb_l
        print("elbo")
    elif 'sho' in command : #sho_l or sho_r
        print("sho")
    elif 'body' in command: #body_y
        print("body")
    else:  #speak[]
        print("speak")
    action(command,detail)
    return render_template('index.html')
    #return render_template('hello.html',message="")

if __name__ == '__main__':
    app.run(host = host, port = port, debug = True)
