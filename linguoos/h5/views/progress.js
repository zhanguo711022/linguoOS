export function render(container) {
  const scores = {
    precision: 78,
    structure: 72,
    logic: 69,
    usage: 83,
    sound: 76,
  };

  container.innerHTML = `
    <section class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="font-weight:600;">本周学习热力图</div>
        <div style="color:var(--text-light);font-size:12px;">7天</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(7, 1fr);gap:6px;margin-top:12px;">
        ${[4, 7, 2, 8, 10, 6, 9]
          .map((value) => {
            const intensity = Math.min(1, value / 10);
            return `<div style="height:36px;border-radius:10px;background:rgba(102,126,234,${0.15 + intensity * 0.6});"></div>`;
          })
          .join("")}
      </div>
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="font-weight:600;">5维能力雷达</div>
      <div style="display:flex;justify-content:center;margin-top:12px;">${drawRadar(scores)}</div>
    </section>

    <section class="card" style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;">
      <div>
        <div style="font-weight:600;">连续学习天数</div>
        <div style="color:var(--text-light);font-size:12px;margin-top:4px;">坚持越久成长越快</div>
      </div>
      <div style="font-size:28px;font-weight:700;">🔥 12</div>
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="font-weight:600;">最近练习记录</div>
      <div class="timeline" style="margin-top:12px;">
        ${["晨间口语对话", "逻辑表达训练", "商务写作精进"]
          .map(
            (item, index) => `
          <div class="timeline-item">
            <div class="timeline-dot" style="background:${index === 0 ? "#4facfe" : "#667eea"};"></div>
            <div>
              <div style="font-weight:600;">${item}</div>
              <div style="color:var(--text-light);font-size:12px;">${index + 1} 小时前完成</div>
            </div>
          </div>
        `
          )
          .join("")}
      </div>
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="font-weight:600;margin-bottom:12px;">成就徽章</div>
      <div class="badge-row">
        <div class="badge">🚀 初级表达</div>
        <div class="badge">🔥 7日连续</div>
        <div class="badge" style="opacity:0.5;">🔒 语法大师</div>
      </div>
    </section>
  `;
}

function drawRadar(scores) {
  const labels = ["precision", "structure", "logic", "usage", "sound"];
  const values = labels.map((label) => scores[label]);
  const max = 100;
  const center = 120;
  const radius = 90;
  const angleStep = (Math.PI * 2) / labels.length;

  const points = values
    .map((value, i) => {
      const angle = -Math.PI / 2 + i * angleStep;
      const r = (value / max) * radius;
      return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
    })
    .join(" ");

  const grid = [0.2, 0.4, 0.6, 0.8, 1].map((ratio) => {
    const gridPoints = labels
      .map((_, i) => {
        const angle = -Math.PI / 2 + i * angleStep;
        const r = ratio * radius;
        return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
      })
      .join(" ");
    return `<polygon points="${gridPoints}" fill="none" stroke="rgba(102,126,234,0.2)" stroke-width="1" />`;
  });

  const labelNodes = labels
    .map((label, i) => {
      const angle = -Math.PI / 2 + i * angleStep;
      const r = radius + 16;
      const x = center + r * Math.cos(angle);
      const y = center + r * Math.sin(angle);
      const value = scores[label];
      return `<text x="${x}" y="${y}" text-anchor="middle" font-size="12" fill="#6b7280">${label}<tspan x="${x}" dy="14" fill="#667eea">${value}</tspan></text>`;
    })
    .join("");

  return `
    <svg width="240" height="240" viewBox="0 0 240 240">
      <defs>
        <linearGradient id="radarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#667eea" />
          <stop offset="100%" stop-color="#f093fb" />
        </linearGradient>
      </defs>
      ${grid.join("")}
      <polygon points="${points}" fill="url(#radarGrad)" opacity="0.3" stroke="#667eea" stroke-width="2" />
      ${labelNodes}
    </svg>
  `;
}
