export function renderStatus(container, state, handlers) {
  const status = state.status || {};
  const health = state.health || {};
  const metrics = state.metrics || {};
  const events = state.events || [];

  container.innerHTML = `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
        <div>
          <div class="section-title" data-i18n="status.title">System Status</div>
          <div class="subtle" data-i18n="status.subtitle">Live health snapshot.</div>
        </div>
        <button class="btn btn-ghost" type="button" id="refreshStatus" data-i18n="status.refresh">Refresh</button>
      </div>
      <div class="grid-3" style="margin-top: 12px;">
        <div>
          <div class="subtle" data-i18n="status.health">Health</div>
          <div style="font-weight: 700;">${health.status || (health.ok ? "OK" : "-")}</div>
        </div>
        <div>
          <div class="subtle" data-i18n="status.version">Version</div>
          <div style="font-weight: 700;">${status.version || "-"}</div>
        </div>
        <div>
          <div class="subtle" data-i18n="status.uptime">Uptime</div>
          <div style="font-weight: 700;">${formatUptime(status.uptime)}</div>
        </div>
        <div>
          <div class="subtle" data-i18n="status.provider">Provider</div>
          <div style="font-weight: 700;">${status.provider || "-"}</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="status.metrics">Metrics</div>
      <div class="metrics">
        ${Object.keys(metrics).length ? renderMetrics(metrics) : `<div class="subtle">${handlers.t("status.empty")}</div>`}
      </div>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="status.events">Recent Events</div>
      <div class="timeline">
        ${
          events.length
            ? events
                .map(
                  (event) => `
              <div class="timeline-item">
                <div class="timeline-dot">⚡</div>
                <div>
                  <div style="font-weight: 600;">${event.name || event.type || "Event"}</div>
                  <div class="subtle">${formatTime(event.timestamp)} · ${event.detail || ""}</div>
                </div>
              </div>
            `
                )
                .join("")
            : `<div class="subtle">${handlers.t("status.noEvents")}</div>`
        }
      </div>
    </div>
  `;

  container.querySelector("#refreshStatus").addEventListener("click", () => handlers.onRefresh());
}

function renderMetrics(metrics) {
  return Object.entries(metrics)
    .map(
      ([key, value]) => `
      <div style="display: flex; justify-content: space-between;">
        <span>${key}</span>
        <span style="font-weight: 600;">${formatValue(value)}</span>
      </div>
    `
    )
    .join("");
}

function formatValue(value) {
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return value ?? "-";
}

function formatUptime(value) {
  if (!value) return "-";
  const total = Math.floor(value);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

function formatTime(value) {
  if (!value) return "";
  const date = new Date(value * 1000 || value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString();
}
