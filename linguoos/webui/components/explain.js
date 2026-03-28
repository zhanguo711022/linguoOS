export function renderExplain(container, state, handlers) {
  const explain = state.explain;
  container.innerHTML = `
    <div class="card">
      <div class="section-title" data-i18n="explain.title">Concept Explain</div>
      <div class="subtle" data-i18n="explain.subtitle">Core structure and examples.</div>
      ${explain ? buildExplainContent(explain, handlers) : `<div class="subtle">${handlers.t("explain.empty")}</div>`}
    </div>
  `;

  const continueButton = container.querySelector("[data-explain-continue]");
  if (continueButton) {
    continueButton.addEventListener("click", () => handlers.onContinue());
  }
}

export function explainMarkup(state, handlers) {
  if (!state.explain) {
    return `<div class="subtle">${handlers.t("explain.empty")}</div>`;
  }
  return buildExplainContent(state.explain, handlers, true);
}

function buildExplainContent(explain, handlers, compact) {
  const title = explain.title || explain.concept || handlers.t("explain.untitled");
  const oneLiner = explain.one_liner || explain.summary || "";
  const structure = explain.structure_template || explain.structure || [];
  const example = explain.example || explain.samples || "";

  const structureItems = Array.isArray(structure)
    ? structure.map((item) => `<li>${item}</li>`).join("")
    : `<li>${structure}</li>`;

  return `
    <div style="margin-top: 12px;">
      <div style="font-size: 18px; font-weight: 700; color: var(--primary);">${title}</div>
      <div class="subtle" style="margin-top: 6px;">${oneLiner}</div>
      <div style="margin-top: 12px;">
        <div class="subtle">${handlers.t("explain.structure")}</div>
        <ol style="margin-top: 8px; padding-left: 18px;">${structureItems}</ol>
      </div>
      ${
        example
          ? `<div class="card" style="margin-top: 12px; background: rgba(255, 107, 53, 0.1);">
              <div class="subtle">${handlers.t("explain.example")}</div>
              <div style="margin-top: 6px; font-weight: 600;">${example}</div>
            </div>`
          : ""
      }
      ${
        compact
          ? `<button class="btn btn-primary" type="button" data-explain-continue style="margin-top: 16px;">${handlers.t("explain.cta")}</button>`
          : `<button class="btn btn-primary" type="button" data-explain-continue style="margin-top: 16px;">${handlers.t("explain.cta")}</button>`
      }
    </div>
  `;
}
