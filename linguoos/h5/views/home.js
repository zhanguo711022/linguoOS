const API_BASE = "/api/v1/curriculum";

const state = {
  userId: null,
  levelId: null,
  modules: [],
  progress: {},
  currentQuestions: [],
  currentQuestionIndex: 0,
  correctCount: 0,
};

function getUserId() {
  const key = "linguoos_user_id";
  let userId = localStorage.getItem(key);
  if (!userId) {
    userId = `guest_${Math.random().toString(36).slice(2, 8)}`;
    localStorage.setItem(key, userId);
  }
  return userId;
}

function getLevelId() {
  return localStorage.getItem("linguoos_level_id") || "";
}

function setLevelId(levelId) {
  localStorage.setItem("linguoos_level_id", levelId);
}

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

async function apiPost(path, payload) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function render(container) {
  container.innerHTML = "";
  if (!state.levelId) {
    renderLevelPicker(container);
    return;
  }
  renderModuleList(container);
}

async function renderLevelPicker(container) {
  const levels = await apiGet("/levels");
  const header = document.createElement("div");
  header.className = "h5-hero";
  header.innerHTML = `
    <div class="h5-title">👋 欢迎来到 LinguoOS</div>
    <div class="h5-subtitle">选择你的起点</div>
  `;
  container.appendChild(header);

  const list = document.createElement("div");
  list.className = "h5-level-list";
  levels.forEach((level) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "h5-level-card";
    card.style.borderColor = level.color;
    card.innerHTML = `
      <div class="h5-level-row">
        <span class="h5-emoji">${level.emoji}</span>
        <div>
          <div class="h5-level-name">${level.name} <span class="h5-level-cefr">${level.cefr}</span></div>
          <div class="h5-level-zh">${level.name_zh} · ${level.desc}</div>
          <div class="h5-level-target">${level.target}</div>
        </div>
      </div>
    `;
    card.addEventListener("click", async () => {
      state.levelId = level.id;
      setLevelId(level.id);
      await apiPost("/progress", {
        user_id: state.userId,
        level_id: level.id,
        module_id: "__level__",
        completed: true,
        score: 0,
      });
      render(container);
    });
    list.appendChild(card);
  });
  container.appendChild(list);
}

async function renderModuleList(container) {
  const header = document.createElement("div");
  header.className = "h5-hero";
  header.innerHTML = `
    <button class="h5-back" type="button">← 返回</button>
    <div class="h5-title">选择今天练什么</div>
  `;
  header.querySelector(".h5-back").addEventListener("click", () => {
    localStorage.removeItem("linguoos_level_id");
    state.levelId = "";
    render(container);
  });
  container.appendChild(header);

  const [modules, progress] = await Promise.all([
    apiGet(`/modules/${state.levelId}`),
    apiGet(`/progress/${state.userId}`),
  ]);
  state.modules = modules;
  state.progress = progress.modules || {};

  const list = document.createElement("div");
  list.className = "h5-module-list";
  modules.forEach((module) => {
    const score = Math.round(state.progress[module.id] || 0);
    const card = document.createElement("button");
    card.type = "button";
    card.className = "h5-module-card";
    card.innerHTML = `
      <div class="h5-module-left">
        <span class="h5-emoji">${module.emoji}</span>
        <div>
          <div class="h5-module-name">${module.name_zh}</div>
          <div class="h5-module-desc">${module.desc}</div>
        </div>
      </div>
      <div class="h5-progress">
        ${renderProgressArc(score)}
        <div class="h5-progress-label">${score}%</div>
      </div>
    `;
    card.addEventListener("click", () => {
      renderExplain(container, module);
    });
    list.appendChild(card);
  });
  container.appendChild(list);
}

function renderProgressArc(percent) {
  const radius = 18;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percent / 100) * circumference;
  return `
    <svg width="48" height="48" viewBox="0 0 48 48" class="h5-progress-arc">
      <circle cx="24" cy="24" r="${radius}" stroke="#e6e6e6" stroke-width="4" fill="none"></circle>
      <circle cx="24" cy="24" r="${radius}" stroke="#4facfe" stroke-width="4" fill="none" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" stroke-linecap="round"></circle>
    </svg>
  `;
}

async function renderExplain(container, module) {
  const content = await apiGet(`/explain/${module.id}`);
  container.innerHTML = `
    <div class="h5-hero">
      <button class="h5-back" type="button">← 返回</button>
      <div class="h5-title">${content.title}</div>
      <div class="h5-subtitle">${content.one_liner}</div>
    </div>
    <div class="h5-steps">
      ${content.steps
        .map((step, index) => `<div class="h5-step"><span>${index + 1}</span>${step}</div>`)
        .join("")}
    </div>
    <pre class="h5-example">${content.example}</pre>
    <div class="h5-tip">${content.tip}</div>
    <button class="h5-primary" type="button">开始练习</button>
  `;
  container.querySelector(".h5-back").addEventListener("click", () => renderModuleList(container));
  container.querySelector(".h5-primary").addEventListener("click", () => renderPractice(container, module));
}

async function renderPractice(container, module) {
  state.currentQuestions = await apiGet(`/questions/${module.id}`);
  state.currentQuestionIndex = 0;
  state.correctCount = 0;
  renderQuestion(container, module);
}

function renderQuestion(container, module) {
  const question = state.currentQuestions[state.currentQuestionIndex];
  const progress = `${state.currentQuestionIndex + 1} / ${state.currentQuestions.length}`;
  container.innerHTML = `
    <div class="h5-hero">
      <button class="h5-back" type="button">← 返回</button>
      <div class="h5-title">${module.name_zh}</div>
      <div class="h5-subtitle">练习进度 ${progress}</div>
    </div>
    <div class="h5-question">
      <div class="h5-question-prompt">${question.prompt}</div>
      <div class="h5-options">
        ${question.options.map((option) => `<button class="h5-option" type="button">${option}</button>`).join("")}
      </div>
      <div class="h5-feedback"></div>
    </div>
  `;

  container.querySelector(".h5-back").addEventListener("click", () => renderModuleList(container));

  const feedback = container.querySelector(".h5-feedback");
  container.querySelectorAll(".h5-option").forEach((button) => {
    button.addEventListener("click", () => {
      const isCorrect = button.textContent === question.answer;
      if (isCorrect) {
        state.correctCount += 1;
        feedback.innerHTML = `<div class="h5-correct">✅ 正确！</div><button class="h5-primary" type="button">下一题</button>`;
        feedback.querySelector("button").addEventListener("click", () => {
          goNextQuestion(container, module);
        });
      } else {
        feedback.innerHTML = `
          <div class="h5-wrong">❌ 再试一次</div>
          <div class="h5-explain">${question.explanation}</div>
          <button class="h5-primary" type="button">再试一次</button>
        `;
        feedback.querySelector("button").addEventListener("click", () => renderQuestion(container, module));
      }
    });
  });
}

async function goNextQuestion(container, module) {
  if (state.currentQuestionIndex < state.currentQuestions.length - 1) {
    state.currentQuestionIndex += 1;
    renderQuestion(container, module);
    return;
  }
  const score = Math.round((state.correctCount / state.currentQuestions.length) * 100);
  await apiPost("/progress", {
    user_id: state.userId,
    level_id: state.levelId,
    module_id: module.id,
    completed: true,
    score,
  });
  container.innerHTML = `
    <div class="h5-hero">
      <div class="h5-title">模块完成</div>
      <div class="h5-subtitle">${module.name_zh} 完成度 ${score}%</div>
    </div>
    <div class="h5-complete">
      <div class="h5-badge">🎉</div>
      <div>你完成了 3 道题，继续保持！</div>
      <button class="h5-primary" type="button">返回模块</button>
    </div>
  `;
  container.querySelector(".h5-primary").addEventListener("click", () => renderModuleList(container));
}

export function initHome(containerId = "app") {
  const container = document.getElementById(containerId);
  if (!container) return;
  state.userId = getUserId();
  state.levelId = getLevelId();
  render(container);
}
