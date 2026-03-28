export function renderNav(container, state, handlers) {
  container.innerHTML = `
    <nav class="nav">
      <div class="nav-inner">
        <div class="logo">
          <div class="logo-mark">LO</div>
          <div>
            <div>LinguoOS</div>
            <div class="subtle" data-i18n="nav.tagline">Commercial Language Learning</div>
          </div>
        </div>
        <div class="nav-actions">
          <select id="moduleSelect" class="select"></select>
          <div class="nav-tabs" id="navTabs">
            <button data-view="session" class="is-active" data-i18n="nav.session">Session</button>
            <button data-view="practice" data-i18n="nav.practice">Practice</button>
            <button data-view="explain" data-i18n="nav.explain">Explain</button>
            <button data-view="history" data-i18n="nav.history">History</button>
            <button data-view="profile" data-i18n="nav.profile">Profile</button>
            <button data-view="status" data-i18n="nav.status">Status</button>
            <button data-view="teacher" data-i18n="nav.teacher">Teacher</button>
          </div>
        </div>
        <button id="langToggle" class="lang-toggle" type="button"></button>
        <span id="navLoading" class="spinner" style="display: none;"></span>
        <div class="user-badge" id="userBadge"></div>
      </div>
    </nav>
  `;

  const moduleSelect = container.querySelector("#moduleSelect");
  const navTabs = container.querySelector("#navTabs");
  const userBadge = container.querySelector("#userBadge");
  const navLoading = container.querySelector("#navLoading");
  const langToggle = container.querySelector("#langToggle");

  navTabs.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-view]");
    if (!button) return;
    handlers.onNavigate(button.dataset.view);
  });

  moduleSelect.addEventListener("change", (event) => {
    handlers.onModuleChange(event.target.value);
  });

  langToggle.addEventListener("click", () => {
    handlers.onLangToggle();
  });

  const update = () => {
    moduleSelect.innerHTML = state.modules
      .map(
        (module) =>
          `<option value="${module.id}" ${
            module.id === state.moduleId ? "selected" : ""
          }>${module.label}</option>`
      )
      .join("");

    userBadge.textContent = `ID: ${state.userId}`;
    langToggle.textContent = state.language === "zh" ? "中文" : "EN";
    navLoading.style.display = state.busy ? "inline-block" : "none";

    navTabs.querySelectorAll("button").forEach((button) => {
      button.classList.toggle("is-active", button.dataset.view === state.activeView);
    });
  };

  update();
  return { update };
}
