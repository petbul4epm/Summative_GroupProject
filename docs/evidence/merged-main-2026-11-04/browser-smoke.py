import subprocess, sys, time, json
from pathlib import Path
from datetime import date,timedelta
import httpx
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[3]
out=Path(__file__).parent;out.mkdir(exist_ok=True)
results=[];errors=[]
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
    raise RuntimeError('server failed')
def stop():process.terminate();process.wait(timeout=10)
def passed(name):results.append({'check':name,'result':'PASS'});print('PASS:',name,flush=True)
try:
    start()
    with sync_playwright() as pw:
        browser=pw.firefox.launch(headless=True)
        version=browser.version
        page=browser.new_page(viewport={'width':1280,'height':900})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('http://127.0.0.1:8765/app/')
        expect(page.locator('#mode-label')).to_have_text('Connected to FastAPI')
        expect(page.locator('#assignment-list')).to_contain_text('No assignments')
        passed('Connected FastAPI mode and empty list')
        page.locator('#title').fill('Browser smoke assignment')
        yesterday=(date.today()-timedelta(days=1)).isoformat()
        page.locator('#due_date').fill(yesterday)
        page.locator('#save').click()
        expect(page.locator('#message')).to_have_text('Assignment added.')
        expect(page.locator('#assignment-list h3')).to_have_text('Browser smoke assignment')
        expect(page.locator('#pending')).to_have_text('1')
        expect(page.locator('#overdue')).to_have_text('1')
        passed('Create one pending assignment with optional fields empty; overdue shown')
        page.get_by_text('View description',exact=True).click()
        expect(page.get_by_text('No description added.',exact=True)).to_be_visible()
        passed('Expand inline assignment details')
        page.get_by_role('button',name='Edit: Browser smoke assignment',exact=True).click()
        page.locator('#title').fill('Edited browser assignment')
        page.locator('#description').fill('Fictional QA data')
        page.locator('#save').click()
        expect(page.locator('#message')).to_have_text('Assignment updated.')
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        passed('Edit selected assignment and optional fields')
        page.locator('#filter').select_option('overdue')
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        page.get_by_role('button',name='Mark completed: Edited browser assignment',exact=True).click()
        expect(page.locator('#message')).to_have_text('Status updated.')
        expect(page.locator('#assignment-list')).to_contain_text('No assignments')
        expect(page.locator('#done')).to_have_text('1')
        expect(page.locator('#overdue')).to_have_text('0')
        page.locator('#filter').select_option('completed')
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        page.locator('#filter').select_option('pending')
        expect(page.locator('#assignment-list')).to_contain_text('No assignments')
        passed('Complete and filter by overdue/completed/pending')
        page.locator('#filter').select_option('all')
        page.reload()
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        expect(page.locator('#done')).to_have_text('1')
        passed('Browser refresh retains edits and completion')
        stop();start();page.reload()
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        expect(page.locator('#done')).to_have_text('1')
        passed('Server restart retains SQLite record in browser')
        page.screenshot(path=str(out/'desktop-persisted.png'),full_page=True)
        page.once('dialog',lambda d:d.dismiss())
        page.get_by_role('button',name='Delete: Edited browser assignment',exact=True).click()
        expect(page.locator('#assignment-list h3')).to_have_text('Edited browser assignment')
        passed('Cancel deletion retains record')
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        page.screenshot(path=str(out/'mobile-persisted.png'),full_page=True)
        passed('390px viewport has no horizontal overflow')
        page.once('dialog',lambda d:d.accept())
        with page.expect_response(lambda r:r.request.method=='DELETE') as info:
            page.get_by_role('button',name='Delete: Edited browser assignment',exact=True).click()
        assert info.value.status==204 and info.value.body()==b''
        expect(page.locator('#message')).to_have_text('Assignment deleted.')
        expect(page.locator('#assignment-list')).to_contain_text('No assignments')
        page.reload()
        expect(page.locator('#assignment-list')).to_contain_text('No assignments')
        passed('Browser delete returns empty HTTP 204 and stays deleted after refresh')
        assert not errors,errors
        passed('No browser JavaScript errors')
        page.screenshot(path=str(out/'mobile-deleted.png'),full_page=True)
        browser.close()
finally:
    if process and process.poll() is None:stop()
    report={'browser':'Firefox '+locals().get('version','unavailable'),'automated_by':'Codex on behalf of Petya Markova (petbul4epm)','commit':'9a988c769a5e181f714e059476a2d58f1759ae76','checks':results,'page_errors':errors}
    (out/'results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
