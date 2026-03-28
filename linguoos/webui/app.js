const $ = (id) => document.getElementById(id);
const out = $("out");

const storage = {
  get userId() {
    return localStorage.getItem("linguo_user_id") || "";
  },
  set userId(v) {
    localStorage.setItem("linguo_user_id", v || "");
  },
  get visitorId() {
    return localStorage.getItem("linguo_visitor_id") || "";
  },
  set visitorId(v) {
    localStorage.setItem("linguo_visitor_id", v || "");
  },
};

function uuid() {
  if (crypto?.randomUUID) return crypto.randomUUID();
  return "v-" + Math.random().toString(36).slice(2) + Date.now();
}

function ensureSession() {
  if (!storage.visitorId) storage.visitorId = uuid();
  if (!storage.userId) storage.userId = `user-${storage.visitorId.slice(0, 8)}`;
  $("userId").value = storage.userId;
  $("visitorId").value = storage.visitorId;
}

function show(title, data) {
  out.textContent = `${title}\n\n` + JSON.stringify(data, null, 2);
}

function activeUserId() {
  const v = ($("userId").value || "").trim();
  return v || storage.userId;
}

async function request(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    "X-Visitor-Id": ($("visitorId").value || storage.visitorId || "").trim(),
    ...(options.headers || {}),
  };
  const res = await fetch(path, { ...options, headers });
  const data = await res.json().catch(() => ({ ok: false, detail: "Non-JSON response" }));
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}: ${JSON.stringify(data)}`);
  }
  return data;
}

async function getJSON(path) {
  return request(path, { method: "GET", headers: { "Content-Type": "application/json" } });
}

async function postJSON(path, body) {
  return request(path, { method: "POST", body: JSON.stringify(body) });
}

async function deleteJSON(path) {
  return request(path, { method: "DELETE", headers: { "Content-Type": "application/json" } });
}

function setupLogoFallback() {
  const v = $("logoVideo");
  const i = $("logoImage");
  const fallback = () => {
    v.style.display = "none";
    i.style.display = "block";
  };
  v.addEventListener("error", fallback);
  // if autoplay fails on some browsers, keep static visible.
  v.play().catch(fallback);
}

function bindActions() {
  $("btnRegister").onclick = async () => {
    storage.userId = activeUserId();
    storage.visitorId = ($("visitorId").value || storage.visitorId || uuid()).trim();
    $("userId").value = storage.userId;
    $("visitorId").value = storage.visitorId;
    const data = await postJSON("/api/v1/profile/update", {
      user_id: storage.userId,
      language: $("language").value || "en",
      current_stage: Number($("stage").value || 2),
    });
    show("Register / Session Ready", {
      user_id: storage.userId,
      visitor_id: storage.visitorId,
      backend: data,
    });
  };

  $("btnWhoAmI").onclick = () => {
    show("Current Session", {
      user_id: activeUserId(),
      visitor_id: ($("visitorId").value || storage.visitorId || "").trim(),
      module_id: $("moduleId").value,
    });
  };

  $("btnProfileGet").onclick = async () => {
    const uid = encodeURIComponent(activeUserId());
    const data = await getJSON(`/api/v1/profile/current?user_id=${uid}`);
    $("language").value = data.language || "en";
    $("stage").value = data.current_stage ?? 2;
    show("Profile Current", data);
  };

  $("btnProfileSave").onclick = async () => {
    const data = await postJSON("/api/v1/profile/update", {
      user_id: activeUserId(),
      language: $("language").value || "en",
      current_stage: Number($("stage").value || 2),
    });
    show("Profile Saved", data);
  };

  $("btnCtx").onclick = async () => {
    show("A. Workspace Context", await getJSON("/api/v1/workspace/context"));
  };

  $("btnDecide1").onclick = async () => {
    const data = await postJSON("/api/v1/decision/next", {
      user_id: activeUserId(),
      module_id: $("moduleId").value,
      last_mode: null,
      last_correct: null,
    });
    show("B. Decision (first)", data);
  };

  $("btnGet").onclick = async () => {
    const data = await getJSON(`/api/v1/practice/next?module_id=${encodeURIComponent($("moduleId").value)}`);
    show("C1. Practice · Get", data);
  };

  $("btnSubmitWrong").onclick = async () => {
    const data = await postJSON("/api/v1/practice/submit", {
      user_id: activeUserId(),
      input_type: "text",
      payload: {
        module_id: $("moduleId").value,
        content: "Students often learn much faster.",
      },
      client_context: { client_type: "web", workspace_mode: "practice", timestamp: Math.floor(Date.now() / 1000) },
    });
    show("C2. Practice · Submit (Wrong)", data);
  };

  $("btnDecide2").onclick = async () => {
    const data = await postJSON("/api/v1/decision/next", {
      user_id: activeUserId(),
      module_id: $("moduleId").value,
      last_mode: "practice",
      last_correct: false,
    });
    show("D. Decision (after submit)", data);
  };

  $("btnExplain").onclick = async () => {
    const data = await getJSON(`/api/v1/explain/concept?module_id=${encodeURIComponent($("moduleId").value)}`);
    show("E. Explain", data);
  };

  $("btnDemoFlow").onclick = async () => {
    const data = await getJSON(`/api/v1/demo/flow?module_id=${encodeURIComponent($("moduleId").value)}&wrong_first=true`);
    show("One-shot Demo Flow", data);
  };

  $("btnStatus").onclick = async () => show("System Status", await getJSON("/api/v1/system/status"));
  $("btnMetrics").onclick = async () => show("System Metrics", await getJSON("/api/v1/system/metrics"));
  $("btnEvents").onclick = async () => show("System Events", await getJSON("/api/v1/system/events/recent?limit=25"));
  $("btnProvider").onclick = async () => show("System Provider", await getJSON("/api/v1/system/provider"));
  $("btnHist").onclick = async () => {
    const uid = encodeURIComponent(activeUserId());
    show("History (recent)", await getJSON(`/api/v1/history/recent?user_id=${uid}`));
  };
  $("btnHistClear").onclick = async () => {
    const uid = encodeURIComponent(activeUserId());
    show("History Cleared", await deleteJSON(`/api/v1/history/clear?user_id=${uid}`));
  };
}

window.addEventListener("error", (e) => {
  show("UI Error", { message: e.message });
});

(async function init() {
  try {
    ensureSession();
    setupLogoFallback();
    bindActions();
    show("Ready", { user_id: activeUserId(), visitor_id: storage.visitorId });
  } catch (e) {
    show("Init Failed", { error: String(e) });
  }
})();
