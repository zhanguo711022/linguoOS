const API_BASE = "/api/v1/curriculum";

const CATEGORY_MAP = {
  "基础": [
    "starter.phonics",
    "starter.greetings",
    "starter.numbers",
    "starter.daily",
  ],
  "语法": [
    "elementary.grammar",
    "elementary.questions",
    "advanced.complex",
  ],
  "表达": [
    "elementary.dialog",
    "elementary.routines",
    "upper.presentation",
    "ielts.speaking",
  ],
  "逻辑": [
    "intermediate.precision",
    "intermediate.logic",
    "upper.argument",
    "advanced.critical",
  ],
  "阅读写作": [
    "intermediate.reading",
    "upper.academic",
    "advanced.synthesis",
    "ielts.reading",
    "ielts.writing",
  ],
};

function getUserId() {
  return localStorage.getItem("linguoos_user_id") || "guest";
}

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function buildRadar(values) {
  const size = 260;
  const center = size / 2;
  const radius = 90;
  const labels = Object.keys(values);
  const points = labels.map((label, index) => {
    const angle = (Math.PI * 2 * index) / labels.length - Math.PI / 2;
    const ratio = values[label] / 100;
    const x = center + Math.cos(angle) * radius * ratio;
    const y = center + Math.sin(angle) * radius * ratio;
    return `${x},${y}`;
  });

  const axisLines = labels
    .map((label, index) => {
      const angle = (Math.PI * 2 * index) / labels.length - Math.PI / 2;
      const x = center + Math.cos(angle) * radius;
      const y = center + Math.sin(angle) * radius;
      return `<line x1="${center}" y1="${center}" x2="${x}" y2="${y}" stroke="#d9d9d9" />`;
    })
    .join("");

  const labelTags = labels
    .map((label, index) => {
      const angle = (Math.PI * 2 * index) / labels.length - Math.PI / 2;
      const x = center + Math.cos(angle) * (radius + 28);
      const y = center + Math.sin(angle) * (radius + 28);
      return `<text x="${x}" y="${y}" text-anchor="middle" font-size="12" fill="#333">${label}</text>`;
    })
    .join("");

  return `
    <svg class="h5-radar" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
      <circle cx="${center}" cy="${center}" r="${radius}" fill="#f6f8ff" stroke="#d9d9d9" />
      ${axisLines}
      <polygon points="${points.join(" ")}" fill="rgba(79,172,254,0.35)" stroke="#4facfe" stroke-width="2" />
      ${labelTags}
    </svg>
  `;
}

function computeRadarData(modules) {
  const values = {};
  Object.entries(CATEGORY_MAP).forEach(([label, ids]) => {
    const scores = ids.map((id) => modules[id]).filter((value) => value !== undefined);
    if (!scores.length) {
      values[label] = 0;
      return;
    }
    const sum = scores.reduce((total, value) => total + value, 0);
    values[label] = Math.round(sum / scores.length);
  });
  return values;
}

export async function initProgress(containerId = "app") {
  const container = document.getElementById(containerId);
  if (!container) return;
  const userId = getUserId();
  const progress = await apiGet(`/progress/${userId}`);
  if (!progress.level_id) {
    container.innerHTML = `
      <div class="h5-hero">
        <div class="h5-title">还没有学习记录</div>
        <div class="h5-subtitle">先去选择你的级别吧</div>
      </div>
    `;
    return;
  }

  const modules = progress.modules || {};
  const radarData = computeRadarData(modules);

  const moduleCards = Object.entries(modules)
    .map(([moduleId, score]) => {
      return `
        <div class="h5-module-progress">
          <div>${moduleId}</div>
          <div class="h5-progress-bar">
            <span style="width: ${score}%"></span>
          </div>
          <div>${Math.round(score)}%</div>
        </div>
      `;
    })
    .join("");

  container.innerHTML = `
    <div class="h5-hero">
      <div class="h5-title">学习进度</div>
      <div class="h5-subtitle">${progress.level_id} 级别</div>
    </div>
    <div class="h5-radar-wrap">
      ${buildRadar(radarData)}
    </div>
    <div class="h5-module-progress-list">
      ${moduleCards}
    </div>
  `;
}
