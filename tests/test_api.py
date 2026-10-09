import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from backend import database
from backend.main import app

@pytest.fixture
def client(monkeypatch):
    with tempfile.TemporaryDirectory() as folder:
        monkeypatch.setattr(database,'DB_PATH',Path(folder)/'test.db')
        with TestClient(app) as c:
            yield c

def payload(**changes):
    return dict(title='Database Coursework',description='Draft report',due_date='2026-11-01',module='Databases',priority='high',status='pending',**changes) if not changes else {**payload(),**changes}

def test_full_crud(client):
    assert client.get('/assignments').json()==[]
    r=client.post('/assignments',json=payload()); assert r.status_code==201
    id=r.json()['id']
    assert client.get(f'/assignments/{id}').json()['description']=='Draft report'
    r=client.put(f'/assignments/{id}',json=payload(title='Updated',status='completed'))
    assert r.status_code==200 and r.json()['status']=='completed'
    assert client.get('/assignments').json()[0]['title']=='Updated'
    assert client.delete(f'/assignments/{id}').status_code==200
    assert client.get(f'/assignments/{id}').status_code==404
    assert client.delete(f'/assignments/{id}').status_code==404

@pytest.mark.parametrize('changes',[{'title':' '},{'due_date':'2026-02-30'},{'status':'in progress'},{'priority':'urgent'},{'title':'x'*121}])
def test_invalid(client,changes):
    assert client.post('/assignments',json=payload(**changes)).status_code==422
    assert client.get('/assignments').json()==[]

def test_update_missing(client):
    assert client.put('/assignments/999',json=payload()).status_code==404

def test_persistence_and_text(client):
    title="<script>alert('test')</script>"
    client.post('/assignments',json=payload(title=title))
    database.initialise()
    assert database.list_assignments()[0]['title']==title

def test_frontend_and_docs(client):
    assert client.get('/').status_code==200
    assert 'assignment-form' in client.get('/').text
    assert client.get('/docs').status_code==200
    assert client.get('/openapi.json').status_code==200
