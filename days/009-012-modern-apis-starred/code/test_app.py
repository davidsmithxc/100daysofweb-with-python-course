from apistar import test

from app import app, characters, CHARACTER_NOT_FOUND

client = test.TestClient(app)

def test_list_characters():
    response = client.get('/')
    assert response.status_code == 200

    json_resp = response.json()
    character_count = len(characters)
    assert len(json_resp) == character_count

    expected = {"pid":1025,"name":"Emil Blonsky",
                "sid":"Secret Identity",
                "align":"Bad Characters",
                "sex":"Male Characters",
                "appearances":"115",
                "year":1967}

    assert json_resp[0] == expected

def test_create_character():
    character_count = len(characters)
    data = {"name":"VB",
                "sid":"Secret Identity",
                "align":"Good Characters",
                "sex":"Female Characters",
                "appearances":"1000",
                "year":2017}

    # check basic post with okay response, characters len increased
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(characters) == character_count + 1

    new_id = max(characters.keys())
    # check that expected value was added
    response = client.get(f'/{new_id}/')
    expected = data = {
                        "pid":new_id,
                        "name":"VB",
                        "sid":"Secret Identity",
                        "align":"Good Characters",
                        "sex":"Female Characters",
                        "appearances":"1000",
                        "year":2017}

    assert response.json() == expected


def test_create_character_validation():
    pass

def test_delete_character():
    pass

