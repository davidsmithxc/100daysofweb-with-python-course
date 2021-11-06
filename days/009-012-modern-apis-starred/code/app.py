from collections import Counter, namedtuple, defaultdict
import csv
import re
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

# helpers

DATA = './marvel-wikia-data.csv'
Character = namedtuple('Character', 'pid name sid align sex appearances year')


def _load_marvel_data(data=DATA):
    '''write a function to parse marvel-wikia-data.csv, see
       https://docs.python.org/3.7/library/csv.html#csv.DictReader
       should return a list of OrderedDicts or a list of Character
       namedtuples (see Character namedtuple above')'''
    with open(data) as csvfile:
        for row in csv.DictReader(csvfile):
            name = re.sub(r'(.*?)\(.*', r'\1', row['name']).strip()
            # could do:
            # yield row
            # but namedtuple is more elgant
            # tried to make pytest work with both
            if row['Year'] == '':
                row['Year'] = None
            else:
                row['Year'] = int(row['Year'])
            yield Character(pid=int(row['page_id']),
                            name=name,
                            sid=row['ID'],
                            align=row['ALIGN'],
                            sex=row['SEX'],
                            appearances=row['APPEARANCES'],
                            year=row['Year'])


data = list(_load_marvel_data())
characters = defaultdict(dict)
characters = {character.pid: character._asdict() for character in data}

VALID_SIDS = set([value['sid'] for key, value in characters.items()])
VALID_ALIGNS = set([value['align'] for key, value in characters.items()])
VALID_SEXES = set([value['sex'] for key, value in characters.items()])
MIN_YEAR = min([value['year'] if value['year'] is not None else 10000 for key, value in characters.items()])

CHARACTER_NOT_FOUND = 'This character is so secret, they don\'t exist!'

# definition

class MarvelCharacter(types.Type):
    pid = validators.Integer(allow_null=True)
    name = validators.String(max_length=100)
    sid = validators.String(enum=list(VALID_SIDS) , default='')
    align = validators.String(enum=list(VALID_ALIGNS) , default='')
    sex = validators.String(enum=list(VALID_SEXES) , default='')
    appearances = validators.String(default='')
    year = validators.Integer(minimum=MIN_YEAR, allow_null=True)

# API methods

def list_characters() -> List[MarvelCharacter]:
    return [MarvelCharacter(character) for key, character in sorted(characters.items())]

def create_character(character: MarvelCharacter) -> JSONResponse:
    character_id = max(characters.keys())+1
    character.pid = character_id
    characters[character_id] = character

    return JSONResponse(MarvelCharacter(character), status_code=201)

def get_character(character_id: int) -> JSONResponse:
    character = characters.get(character_id)
    if not character:
        error = {'error': CHARACTER_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(MarvelCharacter(character), status_code=200)

def update_character(character_id: int, character: MarvelCharacter) -> JSONResponse:
    if not characters.get(character_id):
        error = {'error': CHARACTER_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    character.id = character_id
    characters[character_id] = character
    return JSONResponse(MarvelCharacter(character), status_code=200)

def delete_character(character_id: int) -> JSONResponse:
    if not characters.get(character_id):
        error = {'error': CHARACTER_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    
    del characters[character_id]
    return JSONResponse({}, status_code=204)

routes = [
    Route('/', method='GET', handler=list_characters),
    Route('/', method='POST', handler=create_character),
    Route('/{character_id}/', method='GET', handler=get_character),
    Route('/{character_id}/', method='PUT', handler=update_character),
    Route('/{character_id}/', method='DELETE', handler=delete_character),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)