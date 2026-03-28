export function renderTeacher(container, state, handlers) {
  container.innerHTML = `
    <div class="card">
      <div class="section-title" data-i18n="teacher.title">Teacher Assist</div>
      <div class="subtle" data-i18n="teacher.subtitle">Coming soon for premium instructors.</div>
      <div style="margin-top: 16px; font-weight: 600;">${handlers.t("teacher.featuresTitle")}</div>
      <ul style="margin-top: 8px; padding-left: 18px;">
        <li>${handlers.t("teacher.feature1")}</li>
        <li>${handlers.t("teacher.feature2")}</li>
        <li>${handlers.t("teacher.feature3")}</li>
        <li>${handlers.t("teacher.feature4")}</li>
        <li>${handlers.t("teacher.feature5")}</li>
      </ul>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="teacher.subscribe">Email Subscription</div>
      <div class="subtle" data-i18n="teacher.subscribeHint">Leave your email to get updates.</div>
      <div style="margin-top: 12px; display: flex; gap: 10px;">
        <input class="input" type="email" placeholder="teacher@school.com" />
        <button class="btn btn-primary" type="button" data-i18n="teacher.submit">Subscribe</button>
      </div>
    </div>
  `;
}
