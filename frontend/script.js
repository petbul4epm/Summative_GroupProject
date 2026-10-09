// Student 2: frontend state, safe DOM rendering and FastAPI integration.
// Demo is explicit over HTTP; opening the file directly also enables demo mode.
const demoMode = location.protocol === 'file:' || new URLSearchParams(location.search).get('demo') === '1';
const DEMO_KEY = 'edutrack-frontend-demo-v1';
let demoRecords = [];
try { demoRecords = JSON.parse(localStorage.getItem(DEMO_KEY) || '[]'); }
catch { demoRecords = []; }
if (!Array.isArray(demoRecords)) demoRecords = [];
let assignments = [], editingId = null;
function demoRequest(path, options) {
  const method = options.method || 'GET';
  const id = path ? Number(path.slice(1)) : null;
  const index = demoRecords.findIndex(a => a.id === id);
  if (method === 'GET') return structuredClone(demoRecords);
  const data = options.body ? JSON.parse(options.body) : null;
  if (data) {
    data.title = data.title.trim(); data.module = data.module.trim();
    if (!data.title) throw new Error('Please enter a title.');
  }
  let result;
  if (method === 'POST') {
    result = {...data, id: Math.max(0,...demoRecords.map(a=>a.id))+1};
    demoRecords.push(result);
  } else if (index < 0) throw new Error('Assignment not found.');
  else if (method === 'PUT') {result = {...data,id}; demoRecords[index] = result;}
  else if (method === 'DELETE') {demoRecords.splice(index,1); result = {deleted:true};}
  else throw new Error('Unsupported action.');
  try { localStorage.setItem(DEMO_KEY,JSON.stringify(demoRecords)); }
  catch { throw new Error('Browser storage unavailable. Demo changes will last only for this session.'); }
  return structuredClone(result);
}
const list = document.querySelector('#assignment-list');
const message = document.querySelector('#message');
const form = document.querySelector('#assignment-form');
const filter = document.querySelector('#filter');
async function api(path='', options={}) {
  if (demoMode) return demoRequest(path, options);
  const response = await fetch('/assignments'+path, options);
  const data = await response.json();
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map(e=>e.loc.slice(1).join('.')+': '+e.msg).join('; ') : data.detail;
    throw new Error(detail || 'Request failed.');
  }
  return data;
}
function node(tag,text,css) {
  const el=document.createElement(tag);
  if(text!==undefined) el.textContent=text;
  if(css) el.className=css;
  return el;
}
function todayISO() {
  const d=new Date();
  return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');
}
function isOverdue(a) { return a.status==='pending' && a.due_date<todayISO(); }
function resetForm() {
  editingId=null; form.reset();
  document.querySelector('#form-heading').textContent='Add assignment';
  document.querySelector('#save').textContent='Add assignment';
  document.querySelector('#cancel').hidden=true;
}
function edit(a) {
  editingId=a.id;
  ['title','description','module','due_date','priority','status'].forEach(k=>{form.elements[k].value=a[k];});
  document.querySelector('#form-heading').textContent='Edit assignment';
  document.querySelector('#save').textContent='Save changes';
  document.querySelector('#cancel').hidden=false;
  form.elements.title.focus();
}
function render() {
  const complete=assignments.filter(a=>a.status==='completed').length;
  const percentage=assignments.length?Math.round(complete/assignments.length*100):0;
  document.querySelector('#total').textContent=assignments.length;
  document.querySelector('#done').textContent=complete;
  document.querySelector('#pending').textContent=assignments.length-complete;
  document.querySelector('#overdue').textContent=assignments.filter(isOverdue).length;
  document.querySelector('#percentage').textContent=percentage+'%';
  document.querySelector('#progress').value=percentage;
  document.querySelector('#progress').textContent=percentage+'%';
  list.replaceChildren();
  const visible=assignments.filter(a=>filter.value==='all'||(filter.value==='overdue'?isOverdue(a):a.status===filter.value));
  if(!visible.length) list.append(node('li','No assignments in this view.'));
  visible.forEach(a=>{
    const row=node('li',undefined,'task'+(a.status==='completed'?' complete':''));
    row.append(node('h3',a.title),node('p',(a.module||'No module')+' · Due '+a.due_date+' · Priority: '+a.priority+' · '+a.status));
    if(isOverdue(a)) row.append(node('p','Overdue','overdue'));
    const details=node('details'); details.append(node('summary','View description'),node('p',a.description||'No description added.')); row.append(details);
    const actions=node('div',undefined,'actions');
    const editButton=node('button','Edit'); editButton.onclick=()=>edit(a);
    const toggle=node('button',a.status==='completed'?'Mark pending':'Mark completed');
    toggle.onclick=()=>mutate(toggle,'/'+a.id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({...a,status:a.status==='completed'?'pending':'completed'})},'Status updated.',a.id);
    const remove=node('button','Delete','delete');
    remove.onclick=()=>{if(confirm('Delete '+a.title+'?')) mutate(remove,'/'+a.id,{method:'DELETE'},'Assignment deleted.',a.id);};
    [editButton,toggle,remove].forEach(b=>b.setAttribute('aria-label',b.textContent+': '+a.title));
    actions.append(editButton,toggle,remove); row.append(actions); list.append(row);
  });
}
async function load(){assignments=await api();render();}
async function mutate(button,path,options,success,id){
  button.disabled=true;
  try {await api(path,options); if(editingId===id) resetForm(); await load(); message.textContent=success;}
  catch(e){message.textContent=e.message;}
  finally{button.disabled=false;}
}
form.addEventListener('submit',async event=>{
  event.preventDefault(); const button=document.querySelector('#save');button.disabled=true;
  const wasEditing=editingId!==null;
  try{
    await api(wasEditing?'/'+editingId:'',{method:wasEditing?'PUT':'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
    resetForm();await load();message.textContent=wasEditing?'Assignment updated.':'Assignment added.';form.elements.title.focus();
  }catch(e){message.textContent=e.message;}finally{button.disabled=false;}
});
document.querySelector('#cancel').onclick=resetForm;
filter.onchange=render;
document.querySelector('#mode-label').textContent = demoMode ? 'Browser demo · saved on this device' : 'Connected to FastAPI';
load().catch(()=>{message.textContent='Cannot connect. Start Sergiu’s FastAPI server or open index.html?demo=1 for the browser demo.';});
