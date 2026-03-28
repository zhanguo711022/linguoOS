export function renderProfile(container, state, handlers) {
  const profile = state.profile;
  const metrics = profile?.metrics || {};
  const stats = profile?.stats || {};

  const dimensions = [
    { key: "precision", label: handlers.t("profile.precision") },
    { key: "structure", label: handlers.t("profile.structure") },
    { key: "logic", label: handlers.t("profile.logic") },
    { key: "usage", label: handlers.t("profile.usage") },
    { key: "sound", label: handlers.t("profile.sound") },
  ];

  container.innerHTML = `
    <div class="card">
      <div class="section-title" data-i18n="profile.title">Learner Profile</div>
      <div class="subtle" data-i18n="profile.subtitle">Performance snapshot by dimension.</div>
      <div style="margin-top: 16px; display: grid; gap: 12px;">
        ${dimensions
          .map((item) => {
            const value = normalize(metrics[item.key]);
            return `
              <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <span>${item.label}</span>
                  <span>${Math.round(value * 100)}%</span>
                </div>
                <div class="progress"><span style="width: ${value * 100}%;"></span></div>
              </div>
            `;
          })
          .join("")}
      </div>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="profile.statsTitle">Stats</div>
      <div class="grid-2" style="margin-top: 12px;">
        <div>
          <div class="subtle" data-i18n="profile.total">Total Practices</div>
          <div style="font-size: 22px; font-weight: 700;">${stats.total_practice || 0}</div>
        </div>
        <div>
          <div class="subtle" data-i18n="profile.accuracy">Accuracy</div>
          <div style="font-size: 22px; font-weight: 700;">${Math.round((stats.correct_rate || 0) * 100)}%</div>
        </div>
      </div>
    </div>
  `;
}

function normalize(value) {
  if (typeof value === "number") {
    if (value > 1) return Math.min(value / 100, 1);
    return Math.max(value, 0);
  }
  return 0.5;
}
