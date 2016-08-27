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
    pass

def logout(client):
    pass

def test_empty_db(client):
    """Start with a blank db"""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
    

if __name__ == '__main__':
    pytest.main()
