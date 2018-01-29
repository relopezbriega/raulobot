# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

default_response="""
En mis blogs están todas las respuestas! <a href='https://relopezbriega.github.io/' target='_blank'>https://relopezbriega.github.io/</a> - <a href='http://relopezbriega.com.ar/' target='_blank'>http://relopezbriega.com.ar/</a> - <a href='https://iaarbook.github.io/' target='_blank'>https://iaarbook.github.io/</a>"""
raulobot = ChatBot("Chatterbot", 
                   storage_adapter="chatterbot.storage.SQLStorageAdapter",
                   logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': default_response
        }
    ],)

raulobot.set_trainer(ChatterBotCorpusTrainer)
raulobot.train("chatterbot.corpus.spanish")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(raulobot.get_response(userText))


if __name__ == "__main__":
    app.run()
