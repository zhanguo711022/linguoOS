import { render as renderHome } from "./views/home.js";
import { render as renderSpeak } from "./views/speak.js";
import { render as renderProgress } from "./views/progress.js";
import { render as renderTeacher } from "./views/teacher.js";

const routes = {
  "/app": renderHome,
  "/app/speak": renderSpeak,
  "/app/progress": renderProgress,
  "/app/teacher": renderTeacher,
};

const state = {
  user: { name: "Riley" },
  daily: { done: 4, target: 10 },
  modules: [
    { name: "AI口语", desc: "沉浸式对话练习", mastery: 72, color: "#4facfe" },
    { name: "精准表达", desc: "逻辑结构训练", mastery: 56, color: "#f093fb" },
    { name: "商务写作", desc: "高频表达模板", mastery: 38, color: "#667eea" },
    { name: "听力挑战", desc: "真实语速训练", mastery: 64, color: "#f5576c" },
  ],
  chat: [
    { role: "ai", text: "今天想练习哪种表达场景？" },
    { role: "user", text: "我想练习会议开场。" },
  ],
};

const appMain = document.getElementById("appMain");
const tabs = Array.from(document.querySelectorAll(".tab"));
const toast = document.getElementById("toast");

const actions = {
  navigate,
  showToast,
  celebrate,
  apiFetch,
  getVisitorId,
  speakText,
  updateChat,
};

function init() {
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => navigate(tab.dataset.route));
  });

  document.getElementById("settingsBtn").addEventListener("click", () => {
    showToast("设置功能即将上线");
  });

  window.addEventListener("popstate", () => {
    renderRoute(location.pathname);
  });

  renderRoute(location.pathname);
  registerServiceWorker();
}

function navigate(path) {
  if (location.pathname !== path) {
    history.pushState({}, "", path);
  }
  renderRoute(path);
}

function renderRoute(path) {
  const route = routes[path] || routes["/app"];
  tabs.forEach((tab) => {
    const isActive = tab.dataset.route === path || (path === "/app" && tab.dataset.route === "/app");
    tab.classList.toggle("active", isActive);
    tab.setAttribute("aria-selected", isActive ? "true" : "false");
  });

  appMain.innerHTML = "";
  const view = document.createElement("div");
  view.className = "view";
  appMain.appendChild(view);
  route(view, { state, actions });
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2200);
}

function celebrate() {
  for (let i = 0; i < 30; i += 1) {
    const dot = document.createElement("div");
    const hue = Math.floor(Math.random() * 360);
    dot.className = "confetti";
    dot.style.background = `hsl(${hue}, 80%, 60%)`;
    dot.style.left = `${50 + (Math.random() * 40 - 20)}%`;
    dot.style.top = `${40 + (Math.random() * 10 - 5)}%`;
    dot.style.setProperty("--x", `${Math.random() * 160 - 80}px`);
    dot.style.setProperty("--y", `${Math.random() * 200 - 40}px`);
    document.body.appendChild(dot);
    setTimeout(() => dot.remove(), 2000);
  }
}

function getVisitorId() {
  const key = "linguoos-visitor";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto.randomUUID ? crypto.randomUUID() : `visitor-${Date.now()}`;
  localStorage.setItem(key, id);
  return id;
}

let activeAudio = null;

async function speakText(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) return;
  try {
    const language = localStorage.getItem("linguoos-lang") || "zh";
    const response = await fetch("/api/v1/voice/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Visitor-Id": getVisitorId(),
      },
      body: JSON.stringify({ text: trimmed, language, voice: "nova" }),
    });
    if (!response.ok) {
      throw new Error("Voice request failed");
    }
    const blob = await response.blob();
    if (activeAudio) {
      activeAudio.pause();
      URL.revokeObjectURL(activeAudio.src);
    }
    const url = URL.createObjectURL(blob);
    activeAudio = new Audio(url);
    activeAudio.onended = () => URL.revokeObjectURL(url);
    await activeAudio.play();
  } catch (error) {
    showToast("语音播放失败");
  }
}

async function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("X-Visitor-Id", getVisitorId());
  const language = localStorage.getItem("linguoos-lang") || "zh";
  const fullUrl = url.includes("?") ? `${url}&lang=${language}` : `${url}?lang=${language}`;
  const response = await fetch(fullUrl, { ...options, headers });
  if (!response.ok) {
    throw new Error("Network error");
  }
  return response.json();
}

function updateChat(message) {
  state.chat.push(message);
}

function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/app/sw.js").catch(() => {
      showToast("离线缓存暂不可用");
    });
  }
}

init();
