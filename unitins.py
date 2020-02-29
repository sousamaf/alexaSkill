from flask import Flask
from flask_ask import Ask, statement, request, context, question, session, convert_errors, version
import json
import requests
import time
import unidecode
import lxml.html as html
import pandas as pd
import random

## https://developer.amazon.com/en-US/docs/alexa/alexa-design/adaptable.html

app = Flask(__name__)
ask = Ask(app, "/unitins")

def get_news():
    pass

def get_telefone(contato):
    fone = "3 2 1 8 29 49"
    url = "https://www.unitins.br/nportal/portal/page/show/contatos-da-unitins"
    conteudo = requests.get(url)
    return fone


@app.route("/")
def homepage():
    return "Olá, Mundo!"

@ask.launch
def start_skill():
    welcome_message = "E aí meu querido, o que posso fazer por você?"
    return question(welcome_message).reprompt("Consigo acessar os contatos, abrir um chamado no iProtocolo e outras coisas mais.")


@ask.intent('AgeIntent', convert={'age': int})
def say_age(age):
    if 'age' in convert_errors:
        return question("Poderia repetir sua idade?")
    
    if age is None:
        return question("Poderia me contar sua idade?")

    return statement("Você possui {} anos.".format(age))


@ask.intent("iProtocoloIntent")
def iprotocolo():
    return question("Ummmm.. vamos lá então. Qual é sua solicitação?")

@ask.intent("ContatosIntent", convert={'contato': str})
def contatos(contato):

    if 'contato' in convert_errors:
        return question("Número de quem mesmo?")
    
    if contato is None:
        return question("Devo procurar o telefone de quem ou de onde mesmo?")
    
    fone = get_telefone(contato)

    return statement("O telefone solicitado: {},  é: {}".format(contato, fone))

@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Até mais")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Até mais")


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == "__main__":
    app.run(debug=True)