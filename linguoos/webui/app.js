<<<<<<< HEAD
import { renderNav } from "./components/nav.js";
import { renderSession } from "./components/session.js";
import { practiceMarkup, bindPractice } from "./components/practice.js";
import { renderExplain, explainMarkup } from "./components/explain.js";
import { renderHistory } from "./components/history.js";
import { renderProfile } from "./components/profile.js";
import { renderStatus } from "./components/status.js";
import { renderTeacher } from "./components/teacher.js";

const STORAGE_KEYS = {
  userId: "linguoos.userId",
  visitorId: "linguoos.visitorId",
  language: "linguoos.language",
  moduleId: "linguoos.moduleId",
};

// Shared UI state for all views.
const state = {
  userId: localStorage.getItem(STORAGE_KEYS.userId) || "guest",
  visitorId: localStorage.getItem(STORAGE_KEYS.visitorId) || cryptoId(),
  language: localStorage.getItem(STORAGE_KEYS.language) || "zh",
  moduleId: localStorage.getItem(STORAGE_KEYS.moduleId) || "precision.generalization",
  modules: [],
  activeView: "session",
  chat: [],
  loading: false,
  busy: false,
  currentMode: null,
  lastMode: null,
  lastCorrect: null,
  sessionId: null,
  practice: null,
  explain: null,
  history: [],
  profile: null,
  status: null,
  health: null,
  metrics: null,
  events: [],
};

const toast = document.getElementById("toast");
const navRoot = document.getElementById("nav-root");
const views = {
  session: document.getElementById("view-session"),
  practice: document.getElementById("view-practice"),
  explain: document.getElementById("view-explain"),
  history: document.getElementById("view-history"),
  profile: document.getElementById("view-profile"),
  status: document.getElementById("view-status"),
  teacher: document.getElementById("view-teacher"),
};

localStorage.setItem(STORAGE_KEYS.visitorId, state.visitorId);

let navApi = null;
let statusTimer = null;

const defaultModules = [
  { id: "precision.generalization", label: "Generalization" },
  { id: "precision.structure", label: "Structure" },
  { id: "precision.logic", label: "Logic" },
  { id: "precision.usage", label: "Usage" },
  { id: "precision.sound", label: "Sound" },
];

state.modules = defaultModules;

const i18n = {
  zh: {
    "nav.tagline": "商业级语言教学平台",
    "nav.session": "会话",
    "nav.practice": "练习",
    "nav.explain": "讲解",
    "nav.history": "历史",
    "nav.profile": "档案",
    "nav.status": "状态",
    "nav.teacher": "老师",
    "session.title": "学习会话",
    "session.subtitle": "由引擎引导的学习流程。",
    "session.userPlaceholder": "输入用户ID",
    "session.start": "开始学习",
    "session.chatTitle": "对话记录",
    "session.modeTitle": "操作区",
    "session.loading": "正在加载...",
    "session.idle": "准备就绪，点击开始学习。",
    "session.messagePlaceholder": "输入消息与导师对话",
    "session.send": "发送",
    "practice.title": "练习任务",
    "practice.prompt": "题目提示",
    "practice.answerPlaceholder": "输入你的答案...",
    "practice.submit": "提交",
    "practice.next": "继续",
    "practice.tap": "点击选项即可提交",
    "practice.empty": "暂无练习内容。",
    "explain.title": "概念讲解",
    "explain.subtitle": "结构化要点与示例。",
    "explain.structure": "结构模板",
    "explain.example": "示例",
    "explain.cta": "我明白了，去练习",
    "explain.empty": "暂无讲解内容。",
    "explain.untitled": "概念",
    "history.title": "历史记录",
    "history.subtitle": "最近学习记录。",
    "history.clear": "清除历史",
    "history.empty": "暂无历史。",
    "profile.title": "学员档案",
    "profile.subtitle": "五维能力概览。",
    "profile.statsTitle": "学习统计",
    "profile.total": "总练习次数",
    "profile.accuracy": "正确率",
    "profile.precision": "精准度",
    "profile.structure": "结构",
    "profile.logic": "逻辑",
    "profile.usage": "用法",
    "profile.sound": "语音",
    "status.title": "系统状态",
    "status.subtitle": "实时健康监测。",
    "status.refresh": "刷新",
    "status.health": "健康",
    "status.version": "版本",
    "status.uptime": "运行时长",
    "status.provider": "提供方",
    "status.metrics": "指标",
    "status.events": "最近事件",
    "status.empty": "暂无指标数据。",
    "status.noEvents": "暂无事件。",
    "teacher.title": "老师介入",
    "teacher.subtitle": "高级教师功能即将上线。",
    "teacher.featuresTitle": "即将支持",
    "teacher.feature1": "实时学习监控",
    "teacher.feature2": "一键介入辅导",
    "teacher.feature3": "Telegram通知",
    "teacher.feature4": "Email通知",
    "teacher.feature5": "Webhook推送",
    "teacher.subscribe": "邮件订阅",
    "teacher.subscribeHint": "留下邮箱获取更新。",
    "teacher.submit": "订阅",
    "toast.error": "请求失败，请稍后重试。",
    "toast.sessionFallback": "会话接口暂不可用，已降级到标准流程。",
    "toast.clearConfirm": "确定清除历史记录？",
  },
  en: {
    "nav.tagline": "Commercial Language Learning",
    "nav.session": "Session",
    "nav.practice": "Practice",
    "nav.explain": "Explain",
    "nav.history": "History",
    "nav.profile": "Profile",
    "nav.status": "Status",
    "nav.teacher": "Teacher",
    "session.title": "Learning Session",
    "session.subtitle": "A guided flow driven by the engine.",
    "session.userPlaceholder": "Enter user ID",
    "session.start": "Start Learning",
    "session.chatTitle": "Dialog",
    "session.modeTitle": "Action Zone",
    "session.loading": "Loading...",
    "session.idle": "Ready. Tap start to begin learning.",
    "session.messagePlaceholder": "Type a message to the coach",
    "session.send": "Send",
    "practice.title": "Practice",
    "practice.prompt": "Prompt",
    "practice.answerPlaceholder": "Type your answer...",
    "practice.submit": "Submit",
    "practice.next": "Continue",
    "practice.tap": "Tap an option to submit",
    "practice.empty": "No practice available.",
    "explain.title": "Concept Explain",
    "explain.subtitle": "Structured insight and example.",
    "explain.structure": "Structure",
    "explain.example": "Example",
    "explain.cta": "Got it, go practice",
    "explain.empty": "No explanation available.",
    "explain.untitled": "Concept",
    "history.title": "History",
    "history.subtitle": "Recent activity.",
    "history.clear": "Clear",
    "history.empty": "No history yet.",
    "profile.title": "Learner Profile",
    "profile.subtitle": "Five-dimensional overview.",
    "profile.statsTitle": "Stats",
    "profile.total": "Total Practices",
    "profile.accuracy": "Accuracy",
    "profile.precision": "Precision",
    "profile.structure": "Structure",
    "profile.logic": "Logic",
    "profile.usage": "Usage",
    "profile.sound": "Sound",
    "status.title": "System Status",
    "status.subtitle": "Live health check.",
    "status.refresh": "Refresh",
    "status.health": "Health",
    "status.version": "Version",
    "status.uptime": "Uptime",
    "status.provider": "Provider",
    "status.metrics": "Metrics",
    "status.events": "Recent Events",
    "status.empty": "No metrics yet.",
    "status.noEvents": "No events yet.",
    "teacher.title": "Teacher Assist",
    "teacher.subtitle": "Premium instructor tools are coming.",
    "teacher.featuresTitle": "Planned Features",
    "teacher.feature1": "Real-time learner monitoring",
    "teacher.feature2": "One-tap intervention",
    "teacher.feature3": "Telegram alerts",
    "teacher.feature4": "Email notifications",
    "teacher.feature5": "Webhook delivery",
    "teacher.subscribe": "Email Subscription",
    "teacher.subscribeHint": "Leave your email to get updates.",
    "teacher.submit": "Subscribe",
    "toast.error": "Request failed. Please try again.",
    "toast.sessionFallback": "Session API unavailable, falling back to standard flow.",
    "toast.clearConfirm": "Clear history records?",
  },
};

function t(key) {
  return i18n[state.language][key] || key;
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("is-visible");
  setTimeout(() => toast.classList.remove("is-visible"), 2200);
}

function setBusy(isBusy) {
  state.busy = isBusy;
  renderNavUI();
}

async function apiGet(path, options = {}) {
  return apiFetch(path, { method: "GET" }, options);
}

async function apiPost(path, body, options = {}) {
  return apiFetch(
    path,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    options
  );
}

// Uniform API fetch with visitor header and toast error handling.
async function apiFetch(path, config, options = {}) {
  setBusy(true);
  try {
    const response = await fetch(path, {
      ...config,
      headers: {
        "X-Visitor-Id": state.visitorId,
        ...(config.headers || {}),
      },
    });

    if (!response.ok) {
      if (options.allowFail && response.status === options.allowFail) {
        return { __error: true, status: response.status };
      }
      throw new Error(`${response.status} ${response.statusText}`);
    }

    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    showToast(options.errorMessage || t("toast.error"));
    return { __error: true, detail: error.message };
  } finally {
    setBusy(false);
  }
}

function renderNavUI() {
  if (!navApi) return;
  navApi.update();
  applyI18n();
}

function renderAll() {
  renderNavUI();
  renderSession(views.session, state, {
    onUserChange: handleUserChange,
    onStart: startSession,
    renderMode: renderSessionMode,
    onMessage: handleSessionMessage,
    t,
  });
  renderPracticeView();
  renderExplain(views.explain, state, { onContinue: handleExplainContinue, t });
  renderHistory(views.history, state, { onClear: clearHistory, t });
  renderProfile(views.profile, state, { t });
  renderStatus(views.status, state, { onRefresh: refreshStatus, t });
  renderTeacher(views.teacher, state, { t });
  applyI18n();
}

function renderPracticeView() {
  views.practice.innerHTML = `
    <div class="card">
      ${practiceMarkup(state, { t, onChoice: handleChoice, onSubmit: handleSubmit, onInput: handleInput, onNext: fetchPractice }, "practice")}
    </div>
  `;
  bindPractice(views.practice, state, {
    onChoice: handleChoice,
    onSubmit: handleSubmit,
    onInput: handleInput,
    onNext: fetchPractice,
  });
}

// Render the session action zone based on decision mode.
function renderSessionMode(mode, container) {
  if (mode === "practice") {
    container.innerHTML = practiceMarkup(state, { t }, "session");
    bindPractice(container, state, {
      onChoice: handleChoice,
      onSubmit: handleSubmit,
      onInput: handleInput,
      onNext: handleDecisionNext,
    });
    return;
  }
  if (mode === "explain") {
    container.innerHTML = explainMarkup(state, { t });
    const button = container.querySelector("[data-explain-continue]");
    if (button) {
      button.addEventListener("click", handleExplainContinueSession);
    }
    return;
  }
  container.innerHTML = `<div class="subtle">${t("session.idle")}</div>`;
}

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.setAttribute("placeholder", t(node.dataset.i18nPlaceholder));
  });
}

function showView(view) {
  state.activeView = view;
  Object.entries(views).forEach(([key, section]) => {
    section.classList.toggle("is-active", key === view);
  });
  renderNavUI();
  renderAll();
  if (view === "status") {
    refreshStatus();
    if (!statusTimer) {
      statusTimer = setInterval(refreshStatus, 5000);
    }
  } else if (statusTimer) {
    clearInterval(statusTimer);
    statusTimer = null;
  }
  if (view === "history") {
    fetchHistory();
  }
  if (view === "profile") {
    fetchProfile();
  }
}

function handleUserChange(value) {
  state.userId = value || "guest";
  localStorage.setItem(STORAGE_KEYS.userId, state.userId);
  renderNavUI();
}

async function loadModules() {
  state.modules = defaultModules;
  const data = await apiGet("/api/v1/precision/modules");
  if (data && !data.__error && Array.isArray(data.modules)) {
    state.modules = data.modules.map((module) => ({
      id: module.id || module.module_id || module,
      label: module.label || module.name || module.id || module,
    }));
  }
  if (!state.modules.find((module) => module.id === state.moduleId)) {
    state.moduleId = state.modules[0]?.id || state.moduleId;
  }
  renderNavUI();
}

function handleModuleChange(moduleId) {
  state.moduleId = moduleId;
  localStorage.setItem(STORAGE_KEYS.moduleId, moduleId);
  showToast(`Module: ${moduleId}`);
}

function handleLangToggle() {
  state.language = state.language === "zh" ? "en" : "zh";
  localStorage.setItem(STORAGE_KEYS.language, state.language);
  renderAll();
}

async function startSession() {
  state.loading = true;
  renderAll();

  const sessionResponse = await apiPost(
    "/api/v1/session/start",
    {
      user_id: state.userId,
      module_id: state.moduleId,
      language: state.language,
    },
    { allowFail: 404, errorMessage: t("toast.error") }
  );

  if (sessionResponse && !sessionResponse.__error) {
    state.sessionId = sessionResponse.session_id || sessionResponse.id || null;
  } else if (sessionResponse?.status === 404 || sessionResponse?.__error) {
    showToast(t("toast.sessionFallback"));
  }

  await handleDecisionNext();
  state.loading = false;
  renderAll();
}

async function handleDecisionNext() {
  state.loading = true;
  renderAll();
  const data = await apiPost("/api/v1/decision/next", {
    user_id: state.userId,
    module_id: state.moduleId,
    last_mode: state.lastMode,
    last_correct: state.lastCorrect,
  });

  if (data && !data.__error) {
    const mode = data.mode || data.next_mode || data.workspace_mode || "practice";
    state.currentMode = mode;
    if (mode === "practice") {
      await fetchPractice();
    } else if (mode === "explain") {
      await fetchExplain();
    } else {
      state.currentMode = null;
    }
  }
  state.loading = false;
  renderAll();
}

async function fetchPractice() {
  state.loading = true;
  renderAll();
  const data = await apiGet(`/api/v1/practice/next?module_id=${encodeURIComponent(state.moduleId)}`);
  if (data && !data.__error) {
    state.practice = {
      question: data.question || data,
      answer: "",
      selectedChoice: "",
      feedback: null,
      inputType: data.input_type,
      showNext: false,
    };
    state.currentMode = "practice";
    state.chat.push({ role: "ai", content: data.prompt || data.question?.prompt || data.message || "" });
  }
  state.loading = false;
  renderAll();
}

async function fetchExplain() {
  state.loading = true;
  renderAll();
  const data = await apiGet(`/api/v1/explain/concept?module_id=${encodeURIComponent(state.moduleId)}`);
  if (data && !data.__error) {
    state.explain = data;
    state.currentMode = "explain";
    state.chat.push({ role: "ai", content: data.one_liner || data.summary || t("explain.title") });
  }
  state.loading = false;
  renderAll();
}

function handleChoice(choice) {
  state.practice = state.practice || {};
  state.practice.selectedChoice = choice;
  handleSubmit(choice);
}

function handleInput(value) {
  if (!state.practice) return;
  state.practice.answer = value;
}

async function handleSubmit(answerOverride) {
  if (!state.practice || !state.practice.question) return;
  const answer = answerOverride || state.practice.answer || state.practice.selectedChoice || "";
  if (!answer) return;

  state.loading = true;
  renderAll();

  const question = state.practice.question;
  const response = await apiPost("/api/v1/practice/submit", {
    user_id: state.userId,
    question_id: question.id || question.question_id || question.uid || null,
    answer,
    correct: null,
    payload: {
      prompt: question.prompt || question.question || "",
      choices: question.choices || question.options || [],
      module_id: state.moduleId,
    },
  });

  if (response && !response.__error) {
    const feedback = {
      correct: response.correct,
      why: response.why || response.feedback?.why,
      example: response.example || response.feedback?.example,
      how_to_avoid: response.how_to_avoid || response.feedback?.how_to_avoid,
      text: response.message || response.feedback?.text,
      items: response.feedback?.items,
    };
    state.practice.feedback = feedback;
    state.practice.showNext = true;
    state.lastMode = "practice";
    state.lastCorrect = response.correct ?? null;
    state.chat.push({ role: "user", content: answer });
  }

  state.loading = false;
  renderAll();
}

async function handleSessionMessage(content) {
  const trimmed = (content || "").trim();
  if (!trimmed) return;
  if (!state.sessionId) {
    showToast(t("toast.sessionFallback"));
    return;
  }
  state.chat.push({ role: "user", content: trimmed });
  renderAll();
  const response = await apiPost(
    "/api/v1/session/message",
    { session_id: state.sessionId, content: trimmed },
    { allowFail: 404 }
  );
  if (response && !response.__error) {
    const reply = response.reply || response.message || response.content || t("session.loading");
    state.chat.push({ role: "ai", content: reply });
    renderAll();
  } else if (response?.status === 404) {
    showToast(t("toast.sessionFallback"));
  }
}

function handleExplainContinue() {
  state.lastMode = "explain";
  state.lastCorrect = null;
  showView("practice");
  fetchPractice();
}

function handleExplainContinueSession() {
  state.lastMode = "explain";
  state.lastCorrect = null;
  handleDecisionNext();
}

async function fetchHistory() {
  const data = await apiGet(`/api/v1/history/recent?user_id=${encodeURIComponent(state.userId)}&limit=20`);
  if (data && !data.__error) {
    state.history = data.items || data.history || data || [];
    renderAll();
  }
}

async function clearHistory() {
  const confirmText = t("toast.clearConfirm");
  if (!window.confirm(confirmText)) return;
  const data = await apiPost("/api/v1/history/clear", { user_id: state.userId });
  if (data && !data.__error) {
    state.history = [];
    renderAll();
  }
}

async function fetchProfile() {
  const data = await apiGet(`/api/v1/profile/${encodeURIComponent(state.userId)}`);
  if (data && !data.__error) {
    state.profile = data;
    renderAll();
  }
}

async function refreshStatus() {
  const [healthData, statusData, metricsData, eventsData] = await Promise.all([
    apiGet("/api/v1/system/health"),
    apiGet("/api/v1/system/status"),
    apiGet("/api/v1/system/metrics"),
    apiGet("/api/v1/system/events/recent?limit=10"),
  ]);
  if (healthData && !healthData.__error) state.health = healthData;
  if (statusData && !statusData.__error) state.status = statusData;
  if (metricsData && !metricsData.__error) state.metrics = metricsData;
  if (eventsData && !eventsData.__error) state.events = eventsData.events || eventsData.items || eventsData || [];
  renderAll();
}

function cryptoId() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (char) => {
    const rand = (crypto.getRandomValues(new Uint8Array(1))[0] % 16) | 0;
    const value = char === "x" ? rand : (rand & 0x3) | 0x8;
    return value.toString(16);
  });
}

navApi = renderNav(navRoot, state, {
  onNavigate: showView,
  onLangToggle: handleLangToggle,
  onModuleChange: handleModuleChange,
});

loadModules();
showView("session");
renderAll();
=======
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
>>>>>>> origin/main
