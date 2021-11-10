from datetime import datetime

import requests
from flask import render_template, request

from program import app

time_now = str(datetime.today())


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Template Demo', time=time_now)


@app.route('/100Days')
def p100days():
    return render_template('100Days.html')


@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html',
                           joke=joke)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    valid = False
    if request.method == 'POST' and 'pokecolour' in request.form:
        colour = request.form.get('pokecolour')
        valid_colours = get_valid_poke_colours()
        valid = colour in valid_colours
        if valid:
            pokemon = get_poke_colours(colour)
        else:
            pokemon = valid_colours
    return render_template('pokemon.html',
                           pokemon=pokemon,
                           valid_colour=valid)

@app.route('/trivia')                           
def trivia():
    question, answer = get_trivia_question()
    return render_template('trivia.html',
                            question=question,
                            answer=answer)

def get_trivia_question():
    r = requests.get('https://jservice.io/api/random')
    data = r.json()
    return data[0]['question'], data[0]['answer']


def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']


def get_valid_poke_colours():
        r = requests.get('https://pokeapi.co/api/v2/pokemon-color/')
        colour_data = r.json()
        valid_colours = [each['name'] for each in colour_data['results']]
        return valid_colours

def get_poke_colours(colour):
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + colour.lower())
    pokedata = r.json()
    pokemon = []

    for i in pokedata['pokemon_species']:
        r = requests.get(i['url'])
        url_data = r.json()
        flavor_text = url_data['flavor_text_entries'][0]['flavor_text']
        pokemon.append((i['name'], flavor_text))

    return pokemon
