export function practiceMarkup(state, handlers, contextId) {
  const practice = state.practice;
  if (!practice || !practice.question) {
    return `<div class="subtle">${handlers.t("practice.empty")}</div>`;
  }

  const prompt = practice.question.prompt || practice.question.question || practice.question.text || "";
  const inputType = practice.question.input_type || practice.question.type || practice.inputType || "choice";
  const choices = practice.question.choices || practice.question.options || [];

  const choiceButtons = choices
    .map(
      (choice, idx) => `
        <button class="choice-btn ${practice.selectedChoice === choice ? "is-selected" : ""}" data-choice="${choice}">
          ${String.fromCharCode(65 + idx)}. ${choice}
        </button>`
    )
    .join("");

  const inputArea =
    inputType === "rewrite" || inputType === "text"
      ? `<textarea class="input" rows="3" placeholder="${handlers.t("practice.answerPlaceholder")}" data-practice-input>${
          practice.answer || ""
        }</textarea>`
      : "";

  const submitButton = `
    <button class="btn btn-accent" type="button" data-practice-submit>
      ${handlers.t("practice.submit")}
    </button>`;

  const feedback = practice.feedback ? renderFeedback(practice.feedback) : "";
  const nextButton = practice.showNext
    ? `<button class="btn btn-primary" type="button" data-practice-next>${handlers.t("practice.next")}</button>`
    : "";

  return `
    <div>
      <div class="section-title">${handlers.t("practice.title")}</div>
      <div class="subtle" style="margin-bottom: 12px;">${handlers.t("practice.prompt")}</div>
      <div class="card" style="box-shadow: none; border-style: dashed;">
        <div>${prompt}</div>
      </div>
      ${
        choices.length
          ? `<div class="choice-list" data-choice-list>${choiceButtons}</div>`
          : ""
      }
      ${inputArea}
      <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center;">
        ${choices.length ? "" : submitButton}
        ${choices.length ? `<div class="subtle">${handlers.t("practice.tap")}</div>` : ""}
      </div>
      ${feedback}
      ${nextButton ? `<div style="margin-top: 12px;">${nextButton}</div>` : ""}
    </div>
  `;
}

export function bindPractice(container, state, handlers) {
  const choiceList = container.querySelector("[data-choice-list]");
  if (choiceList) {
    choiceList.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-choice]");
      if (!button) return;
      handlers.onChoice(button.dataset.choice);
    });
  }

  const submitButton = container.querySelector("[data-practice-submit]");
  if (submitButton) {
    submitButton.addEventListener("click", () => handlers.onSubmit());
  }

  const input = container.querySelector("[data-practice-input]");
  if (input) {
    input.addEventListener("input", (event) => handlers.onInput(event.target.value));
  }

  const nextButton = container.querySelector("[data-practice-next]");
  if (nextButton) {
    nextButton.addEventListener("click", () => handlers.onNext());
  }
}

function renderFeedback(feedback) {
  const items = [];

  if (feedback.why) {
    items.push({ icon: "❌", label: feedback.why });
  }
  if (feedback.example) {
    items.push({ icon: "💡", label: feedback.example });
  }
  if (feedback.how_to_avoid) {
    items.push({ icon: "✅", label: feedback.how_to_avoid });
  }

  if (Array.isArray(feedback.items)) {
    feedback.items.forEach((item) => {
      items.push({ icon: item.icon || "💡", label: item.text || item });
    });
  }

  if (!items.length && feedback.text) {
    items.push({ icon: "💡", label: feedback.text });
  }

  const mood = feedback.correct ? "correct" : feedback.correct === false ? "wrong" : "";

  return `
    <div class="feedback ${mood}">
      ${items
        .map(
          (item) => `
        <div class="feedback-item">
          <div>${item.icon}</div>
          <div>${item.label}</div>
        </div>
      `
        )
        .join("")}
    </div>
  `;
}
