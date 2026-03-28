export function renderHistory(container, state, handlers) {
  const items = state.history || [];
  container.innerHTML = `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
        <div>
          <div class="section-title" data-i18n="history.title">History</div>
          <div class="subtle" data-i18n="history.subtitle">Recent learning activity.</div>
        </div>
        <button class="btn btn-ghost" type="button" id="clearHistory" data-i18n="history.clear">Clear History</button>
      </div>
      <div class="timeline">
        ${
          items.length
            ? items
                .map(
                  (item) => `
            <div class="timeline-item">
              <div class="timeline-dot">${iconFor(item.type)}</div>
              <div>
                <div style="font-weight: 600;">${item.summary || item.title || ""}</div>
                <div class="subtle">${formatTime(item.timestamp)} · ${item.type || ""}</div>
              </div>
            </div>
          `
                )
                .join("")
            : `<div class="subtle">${handlers.t("history.empty")}</div>`
        }
      </div>
    </div>
  `;

  const clearButton = container.querySelector("#clearHistory");
  clearButton.addEventListener("click", () => handlers.onClear());
}

function iconFor(type) {
  const map = {
    practice: "📝",
    explain: "📘",
    decision: "🧭",
  };
  return map[type] || "📌";
}

function formatTime(value) {
  if (!value) return "";
  const date = new Date(value * 1000 || value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString();
}
