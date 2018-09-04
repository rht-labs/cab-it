import pytest

def test_initial_state(client, app):

    result = client.get('/api/counter')
    assert b'1' in result.data

def test_set_counter(client, app):

    result = client.get('/api/set_counter/10')
    assert b'10' == result.data

def test_increment_get(client, app):

    client.get('/api/set_counter/1')
    client.get('/api/increment_counter/5')
    currentState = client.get('/api/counter')
    assert b'6' == currentState.data

def test_decrement_get(client, app):

    client.get('/api/set_counter/5')
    client.get('/api/decrement_counter/1')
    currentState = client.get('/api/counter')
    assert b'4' == currentState.data

def test_increment_post(client, app):

    client.get('/api/set_counter/1')
    client.post('/api/increment_counter', data=dict(
        amount=5
    ))
    currentState = client.get('/api/counter')
    assert b'6' == currentState.data

def test_decrement_post(client, app):

    client.get('/api/set_counter/5')
    client.post('/api/decrement_counter', data=dict(
        amount=1
    ))
    currentState = client.get('/api/counter')
    assert b'4' == currentState.data