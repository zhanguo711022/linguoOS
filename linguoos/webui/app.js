const $ = (id)=>document.getElementById(id);
const out = $("out");
const BASE = ""; // same origin

function show(title, data){
  out.textContent = `${title}\n\n` + JSON.stringify(data, null, 2);
}

async function getJSON(path){
  const r = await fetch(BASE + path);
  if(!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
}
async function postJSON(path, body){
  const r = await fetch(BASE + path, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  if(!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
}

// fixed module for demo
const moduleId = "precision.generalization";

$("btnCtx").onclick = async ()=>{
  const data = await getJSON("/api/v1/workspace/context");
  show("A. Workspace Context", data);
};

$("btnDecide1").onclick = async ()=>{
  const data = await postJSON("/api/v1/decision/next", {
    user_id:"demo", module_id:moduleId, last_mode:null, last_correct:null
  });
  show("B. Decision (first)", data);
};

$("btnGet").onclick = async ()=>{
  const data = await getJSON(`/api/v1/practice/next?module_id=${encodeURIComponent(moduleId)}`);
  show("C1. Practice · Get", data);
};

$("btnSubmitWrong").onclick = async ()=>{
  const data = await postJSON("/api/v1/practice/submit", {
    user_id:"demo",
    input_type:"text",
    payload:{content:"Students often learn much faster."},
    client_context:{client_type:"web",workspace_mode:"practice",timestamp:1730000000}
  });
  show("C2. Practice · Submit (Wrong)", data);
};

$("btnDecide2").onclick = async ()=>{
  const data = await postJSON("/api/v1/decision/next", {
    user_id:"demo", module_id:moduleId, last_mode:"practice", last_correct:false
  });
  show("D. Decision (after submit)", data);
};

$("btnExplain").onclick = async ()=>{
  const data = await getJSON(`/api/v1/explain/concept?module_id=${encodeURIComponent(moduleId)}`);
  show("E. Explain", data);
};

$("btnDemoFlow").onclick = async ()=>{
  const data = await getJSON(`/api/v1/demo/flow?module_id=${encodeURIComponent(moduleId)}&wrong_first=true`);
  show("Alt. Demo Flow (one-shot)", data);
};
