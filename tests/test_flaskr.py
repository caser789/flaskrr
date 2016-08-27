# coding: utf-8
"""
    Flaskr Tests
    ~~~~~~~~~~~~~~~~~
"""

import os
import pytest
import tempfile
from context import logging, flaskr
logging.debug('in test')

@pytest.fixture
def client(request):
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    with flaskr.app.app_context():
        flaskr.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client

def login(client, username, passwd):
    return client.post('login', data=dict(
        username=username,
        password=passwd,
        ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_empty_db(client):
    """Start with a blank db"""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data

def test_login_logout(client):
    """make sure login and logout works"""
    rv = login(client, flaskr.app.config['USERNAME'],
            flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'] + 'x',
            flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, flaskr.app.config['USERNAME'],
            flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data




    

if __name__ == '__main__':
    pytest.main()
