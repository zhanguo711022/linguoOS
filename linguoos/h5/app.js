import { render as renderHome } from "./views/home.js?v=2";
import { render as renderSpeak } from "./views/speak.js";
import { render as renderProgress } from "./views/progress.js";
import { render as renderTeacher } from "./views/teacher.js";
import { render as renderScene } from "./views/scene.js";

const routes = {
  "/app": renderHome,
  "/app/speak": renderSpeak,
  "/app/scene": renderScene,
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
    showSettingsPanel();
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
  const avatar = document.getElementById('aiAvatar');
  if (avatar) avatar.classList.add('speaking');
  const trimmed = (text || "").trim();
  if (!trimmed) return;
  // 微信浏览器：先用同步解锁音频上下文
  try {
    var _unlock = new Audio();
    _unlock.src = 'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=';
    _unlock.volume = 0;
    _unlock.play().catch(function(){});
  } catch(e) {}
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
      activeAudio = null;
    }
    const url = URL.createObjectURL(blob);
    activeAudio = new Audio(url);
    // 数智人动画：播放时加 speaking class
    const avatar = document.getElementById("aiAvatar");
    if (avatar) avatar.classList.add("speaking");
    // 返回 Promise，播完才 resolve，彻底解决叠音
    return new Promise((resolve) => {
      activeAudio.onended = () => {
        URL.revokeObjectURL(url);
        activeAudio = null;
        if (avatar) avatar.classList.remove("speaking");
        resolve();
      };
      activeAudio.onerror = () => {
        if (avatar) avatar.classList.remove("speaking");
        resolve();
      };
      activeAudio.play().catch((e) => {        if (e && e.name === "NotAllowedError") showToast("请点击页面任意处后重试");
        if (avatar) avatar.classList.remove("speaking");
        resolve();
      });
    });
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

// ── Settings Panel ─────────────────────────────────────────────
function showSettingsPanel() {
  const existing = document.getElementById("settingsOverlay");
  if (existing) existing.remove();

  const token = localStorage.getItem("linguoos-token");
  const userEmail = localStorage.getItem("linguoos-email");
  const lang = localStorage.getItem("linguoos-lang");
  const level = localStorage.getItem("linguoos-level");

  const overlay = document.createElement("div");
  overlay.id = "settingsOverlay";
  overlay.style.cssText = `position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:flex-end;`;

  const panel = document.createElement("div");
  panel.style.cssText = `background:#fff;width:100%;border-radius:20px 20px 0 0;padding:24px 20px 40px;max-height:85vh;overflow-y:auto;`;

  const langLabels = {en:"英语",fr:"法语",ja:"日语",ko:"韩语",es:"西班牙语",ru:"俄语"};
  const levelLabels = {starter:"零基础",elementary:"初级",intermediate:"中级",upper:"中高级",advanced:"高级",ielts:"雅思/考试"};

  panel.innerHTML = `
    <div style="width:40px;height:4px;background:#e0e0e0;border-radius:2px;margin:0 auto 20px;"></div>
    <div style="font-size:17px;font-weight:700;margin-bottom:20px;">⚙️ 设置</div>

    ${token ? `
      <!-- 已登录 -->
      <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:12px;padding:14px;margin-bottom:16px;">
        <div style="font-size:13px;color:#166534;font-weight:600;">✅ 已登录</div>
        <div style="font-size:12px;color:#15803d;margin-top:4px;">${userEmail || "用户"}</div>
      </div>
      <button onclick="doLogout()" style="width:100%;padding:12px;background:#fee2e2;color:#dc2626;border:none;border-radius:10px;font-size:14px;font-weight:600;margin-bottom:12px;cursor:pointer;">退出登录</button>
    ` : `
      <!-- 未登录 -->
      <div id="authSection">
        <div style="display:flex;gap:8px;margin-bottom:16px;">
          <button id="tabLogin" onclick="switchAuthTab('login')" style="flex:1;padding:10px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;font-weight:600;cursor:pointer;">登录</button>
          <button id="tabRegister" onclick="switchAuthTab('register')" style="flex:1;padding:10px;background:#f3f4f6;color:#666;border:none;border-radius:10px;font-weight:600;cursor:pointer;">注册</button>
        </div>
        <div id="authForm">
          <input id="authEmail" type="email" placeholder="邮箱地址" style="width:100%;padding:12px;border:1.5px solid #e5e7eb;border-radius:10px;font-size:15px;margin-bottom:10px;box-sizing:border-box;"/>
          <input id="authPassword" type="password" placeholder="密码（6位以上）" style="width:100%;padding:12px;border:1.5px solid #e5e7eb;border-radius:10px;font-size:15px;margin-bottom:10px;box-sizing:border-box;"/>
          <div id="authError" style="color:#dc2626;font-size:13px;margin-bottom:8px;display:none;"></div>
          <button id="authSubmit" onclick="doAuth()" style="width:100%;padding:13px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;">登录</button>
        </div>
      </div>
    `}

    <!-- 当前设置 -->
    <div style="margin-top:20px;border-top:1px solid #f3f4f6;padding-top:16px;">
      <div style="font-size:13px;color:#888;margin-bottom:10px;">当前学习设置</div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-size:14px;">学习语言</span>
        <span style="font-size:14px;color:#667eea;font-weight:600;">${langLabels[lang] || "未选择"}</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <span style="font-size:14px;">当前级别</span>
        <span style="font-size:14px;color:#667eea;font-weight:600;">${levelLabels[level] || "未选择"}</span>
      </div>
      <button onclick="doReset()" style="width:100%;padding:11px;background:#f9fafb;color:#dc2626;border:1px solid #fecaca;border-radius:10px;font-size:13px;cursor:pointer;">🔄 重新选择语言和级别</button>
    </div>
  `;

  overlay.appendChild(panel);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.remove(); });
  document.body.appendChild(overlay);
}

let _authMode = "login";
window.switchAuthTab = function(mode) {
  _authMode = mode;
  const loginBtn = document.getElementById("tabLogin");
  const regBtn = document.getElementById("tabRegister");
  const submitBtn = document.getElementById("authSubmit");
  if (!loginBtn) return;
  if (mode === "login") {
    loginBtn.style.background = "linear-gradient(135deg,#667eea,#764ba2)";
    loginBtn.style.color = "white";
    regBtn.style.background = "#f3f4f6";
    regBtn.style.color = "#666";
    submitBtn.textContent = "登录";
  } else {
    regBtn.style.background = "linear-gradient(135deg,#667eea,#764ba2)";
    regBtn.style.color = "white";
    loginBtn.style.background = "#f3f4f6";
    loginBtn.style.color = "#666";
    submitBtn.textContent = "注册";
  }
};

window.doAuth = async function() {
  const email = document.getElementById("authEmail")?.value?.trim();
  const password = document.getElementById("authPassword")?.value;
  const errDiv = document.getElementById("authError");
  const submitBtn = document.getElementById("authSubmit");
  if (!email || !password) { errDiv.textContent="请填写邮箱和密码"; errDiv.style.display="block"; return; }
  if (password.length < 6) { errDiv.textContent="密码至少6位"; errDiv.style.display="block"; return; }
  errDiv.style.display = "none";
  submitBtn.disabled = true;
  submitBtn.textContent = "请稍候...";
  try {
    const url = _authMode === "login" ? "/api/v1/auth/login" : "/api/v1/auth/register";
    const r = await fetch(url, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({email, password})
    });
    const data = await r.json();
    if (!data.ok) throw new Error(data.error?.message || "操作失败");
    const token = _authMode === "login" ? data.data.token : null;
    if (_authMode === "register") {
      // 注册成功后自动登录
      const r2 = await fetch("/api/v1/auth/login", {
        method: "POST", headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email, password})
      });
      const d2 = await r2.json();
      if (d2.ok) {
        localStorage.setItem("linguoos-token", d2.data.token);
        localStorage.setItem("linguoos-email", email);
      }
    } else {
      localStorage.setItem("linguoos-token", token);
      localStorage.setItem("linguoos-email", email);
    }
    document.getElementById("settingsOverlay")?.remove();
    showToast(_authMode === "register" ? "✅ 注册成功，已自动登录！" : "✅ 登录成功！");
  } catch(e) {
    errDiv.textContent = e.message;
    errDiv.style.display = "block";
    submitBtn.disabled = false;
    submitBtn.textContent = _authMode === "login" ? "登录" : "注册";
  }
};

window.doLogout = function() {
  localStorage.removeItem("linguoos-token");
  localStorage.removeItem("linguoos-email");
  document.getElementById("settingsOverlay")?.remove();
  showToast("已退出登录");
};

window.doReset = function() {
  localStorage.removeItem("linguoos-lang");
  localStorage.removeItem("linguoos-level");
  localStorage.removeItem("linguoos-module");
  document.getElementById("settingsOverlay")?.remove();
  location.reload();
};

function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/app/sw.js").catch(() => {
      showToast("离线缓存暂不可用");
    });
  }
}

init();
