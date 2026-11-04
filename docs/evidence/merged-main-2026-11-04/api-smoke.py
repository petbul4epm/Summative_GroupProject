import subprocess, sys, time, json
from pathlib import Path
import httpx

root=Path(__file__).resolve().parents[3]
results=[]
client=httpx.Client(base_url='http://127.0.0.1:8765',trust_env=False)
process=None
def start():
    global process
    process=subprocess.Popen([sys.executable,'-m','uvicorn','backend.main:app','--port','8765'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(100):
        try:
            if client.get('/').status_code==200:return
        except httpx.ConnectError:pass
        time.sleep(.1)
    raise RuntimeError('server failed to start')
def stop():
    process.terminate();process.wait(timeout=10)
def check(name,condition):
    assert condition,name
    results.append({'check':name,'result':'PASS'})
try:
    start()
    check('Frontend, JS, CSS and docs served by live FastAPI',all(client.get(p).status_code==200 for p in ['/app/','/app/script.js','/app/style.css','/docs']))
    check('Initial API list empty',client.get('/assignments').json()==[])
    r=client.post('/assignments',json={'title':'Smoke assignment','due_date':'2026-11-03'})
    a=r.json(); ident=a['id']
    check('Create returns 201 with pending status and null optional fields',r.status_code==201 and a['status']=='pending' and a['description'] is None and a['module'] is None)
    check('View created assignment',client.get(f'/assignments/{ident}').json()==a)
    a.update(title='Smoke assignment edited',description='Fictional verification data',module='QA',priority='high')
    r=client.put(f'/assignments/{ident}',json=a)
    check('Edit returns 200 and saves fields',r.status_code==200 and r.json()['title']==a['title'])
    a['status']='completed';r=client.put(f'/assignments/{ident}',json=a)
    check('Complete returns 200 with completed status',r.status_code==200 and r.json()['status']=='completed')
    check('Fresh GET retains edited fields and completion',client.get(f'/assignments/{ident}').json()==a)
    stop();start()
    check('Real server restart retains SQLite record and completion',client.get(f'/assignments/{ident}').json()==a)
    second=client.post('/assignments',json={'title':'Keep this record','due_date':'2026-11-04'}).json()
    r=client.delete(f'/assignments/{ident}')
    check('Delete returns HTTP 204 and empty response body',r.status_code==204 and r.content==b'')
    check('Deleted record returns 404 and other record unchanged',client.get(f'/assignments/{ident}').status_code==404 and client.get('/assignments').json()==[second])
    client.delete('/assignments/'+str(second['id']))
    stop();start()
    check('Deletion survives server restart',client.get('/assignments').json()==[])
finally:
    if process and process.poll() is None:stop()
    Path(__file__).with_name('api-smoke-results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
