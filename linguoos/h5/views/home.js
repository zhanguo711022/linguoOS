export function render(container, { state, actions }) {
  container.innerHTML = `
    <section class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
        <div>
          <div style="font-size:18px;font-weight:600;">好早上，${state.user.name}！🌟</div>
          <div style="color:var(--text-light);margin-top:6px;">今天继续练习精准表达吗？</div>
        </div>
        <button class="primary-button" id="continueBtn">继续学习</button>
      </div>
      <div style="margin-top:14px;font-size:13px;color:var(--text-light);">
        今日已练${state.daily.done}题，目标${state.daily.target}题
        <div class="progress-bar"><span style="width:${Math.min(100, (state.daily.done / state.daily.target) * 100)}%"></span></div>
      </div>
    </section>

    <section style="margin-top:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <div style="font-weight:600;">推荐模块</div>
        <button class="ghost-button" id="shuffleBtn">换一批</button>
      </div>
      <div class="module-scroll" id="moduleScroll"></div>
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="font-weight:600;">AI 对话练习</div>
      <div class="chat-area" id="chatArea"></div>
      <div id="aiExplainArea" style="margin-top:12px;display:none;"></div>
      <div class="chat-input">
        <input id="chatInput" placeholder="输入你的回答或提问" />
        <button class="ghost-button" id="sendBtn">发送</button>
        <button class="ghost-button" id="recordBtn">🎙️</button>
      </div>
    </section>
  `;

  const moduleScroll = container.querySelector("#moduleScroll");
  state.modules.forEach((mod, index) => {
    const card = document.createElement("button");
    card.className = "module-card";
    card.innerHTML = `
      <div style="font-weight:600;">${mod.name}</div>
      <div style="color:var(--text-light);font-size:12px;margin-top:4px;">${mod.desc}</div>
      <div class="module-arc">${renderArc(mod.mastery, mod.color, index)}</div>
    `;
    card.addEventListener("click", () => {
      actions.showToast(`进入${mod.name}练习`);
    });
    moduleScroll.appendChild(card);
  });

  const chatArea = container.querySelector("#chatArea");
  const aiExplainArea = container.querySelector("#aiExplainArea");
  const chatInput = container.querySelector("#chatInput");
  const sendBtn = container.querySelector("#sendBtn");
  const recordBtn = container.querySelector("#recordBtn");
  const continueBtn = container.querySelector("#continueBtn");
  const shuffleBtn = container.querySelector("#shuffleBtn");

  function renderChat() {
    chatArea.innerHTML = "";
    state.chat.forEach((msg) => {
      const row = document.createElement("div");
      row.className = `chat-row ${msg.role}`;
      const bubble = document.createElement("div");
      bubble.className = `chat-bubble ${msg.role}`;
      bubble.textContent = msg.text;
      if (msg.thinking) {
        bubble.innerHTML = `<span class="thinking"><span></span><span></span><span></span></span>`;
      }
      if (msg.role === "ai") {
        const avatar = document.createElement("div");
        avatar.className = "chat-avatar";
        avatar.textContent = "🤖";
        row.appendChild(avatar);
        row.appendChild(bubble);
      } else {
        const avatar = document.createElement("div");
        avatar.className = "chat-avatar";
        avatar.textContent = "👤";
        row.appendChild(bubble);
        row.appendChild(avatar);
      }
      chatArea.appendChild(row);
    });
  }

  function sendMessage() {
    const value = chatInput.value.trim();
    if (!value) return;
    actions.updateChat({ role: "user", text: value });
    chatInput.value = "";
    actions.updateChat({ role: "ai", text: "", thinking: true });
    renderChat();
    setTimeout(() => {
      state.chat.pop();
      const lastAiQuestion = [...state.chat].reverse().find((msg) => msg.role === "ai")?.text || "";
      const correctAnswer = "Thank you all for joining the meeting today. Let's align on the goals and next steps.";
      const correctionText = `The answer is: ${correctAnswer}`;
      actions.updateChat({ role: "ai", text: correctionText });
      handleWrongAnswer(lastAiQuestion, value, correctAnswer);
      renderChat();
    }, 900);
  }

  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  });

  recordBtn.addEventListener("click", () => {
    actions.showToast("按住口语练习按钮试试" );
  });

  continueBtn.addEventListener("click", () => {
    actions.celebrate();
    actions.showToast("继续学习吧！" );
  });

  shuffleBtn.addEventListener("click", () => {
    actions.showToast("已为你更新练习模块");
  });

  renderChat();

  async function handleWrongAnswer(question, wrongAnswer, correctAnswer) {
    aiExplainArea.style.display = "none";
    aiExplainArea.innerHTML = "";
    try {
      const result = await actions.apiFetch("/api/v1/tutor/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: question || "Please answer the prompt.",
          wrong_answer: wrongAnswer,
          correct_answer: correctAnswer,
          module_id: "home-chat",
          language: localStorage.getItem("linguoos-lang") || "zh",
        }),
      });
      renderExplainCard(result);
      if (actions.speakText && result?.explanation) {
        actions.speakText(result.explanation);
      }
    } catch (error) {
      actions.showToast("AI 讲解暂不可用");
    }
  }

  function renderExplainCard(result = {}) {
    const explanation = result.explanation || "";
    const correctPattern = result.correct_pattern || "";
    const encouragement = result.encouragement || "";
    const followUpQuestion = result.follow_up_question || "";
    const followUpOptions = Array.isArray(result.follow_up_options) ? result.follow_up_options : [];
    const followUpAnswer = result.follow_up_answer || "";
    const hasFollowUp = followUpQuestion && followUpOptions.length;

    aiExplainArea.style.display = "block";
    aiExplainArea.innerHTML = `
      <div class="card" style="box-shadow: none;border:1px solid rgba(102,126,234,0.15);">
        <div style="font-weight:600;">Lingo 讲解</div>
        <div style="margin-top:8px;font-size:13px;line-height:1.5;">${explanation}</div>
        <div style="margin-top:8px;font-size:13px;line-height:1.5;color:var(--text-light);">${correctPattern}</div>
        <div style="margin-top:8px;font-size:13px;line-height:1.5;">${encouragement}</div>
        ${
          hasFollowUp
            ? `<div style="margin-top:12px;">
                <div style="font-weight:600;">${followUpQuestion}</div>
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;">
                  ${followUpOptions
                    .map(
                      (option) =>
                        `<button class="secondary-button" data-follow-option="${option}">${option}</button>`
                    )
                    .join("")}
                </div>
                <div id="followUpAnswer" style="display:none;margin-top:8px;color:var(--text-light);font-size:12px;">
                  参考答案：${followUpAnswer}
                </div>
              </div>`
            : ""
        }
        <div id="nextBtnWrap" style="margin-top:12px;display:${hasFollowUp ? "none" : "block"};">
          <button class="primary-button" id="nextBtn">继续</button>
        </div>
      </div>
    `;

    const nextBtn = aiExplainArea.querySelector("#nextBtn");
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        actions.showToast("继续下一题");
      });
    }

    if (hasFollowUp) {
      const optionButtons = Array.from(aiExplainArea.querySelectorAll("[data-follow-option]"));
      const answerNode = aiExplainArea.querySelector("#followUpAnswer");
      const nextWrap = aiExplainArea.querySelector("#nextBtnWrap");
      optionButtons.forEach((button) => {
        button.addEventListener("click", () => {
          optionButtons.forEach((btn) => btn.classList.remove("is-selected"));
          button.classList.add("is-selected");
          if (answerNode) answerNode.style.display = "block";
          if (nextWrap) nextWrap.style.display = "block";
        });
      });
    }
  }
}

function renderArc(percentage, color, index) {
  const radius = 28;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;
  const gradientId = `grad-${index}`;
  return `
    <svg width="72" height="72" viewBox="0 0 72 72">
      <defs>
        <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="${color}" />
          <stop offset="100%" stop-color="#764ba2" />
        </linearGradient>
      </defs>
      <circle cx="36" cy="36" r="${radius}" fill="none" stroke="rgba(102,126,234,0.15)" stroke-width="8" />
      <circle cx="36" cy="36" r="${radius}" fill="none" stroke="url(#${gradientId})" stroke-width="8"
        stroke-linecap="round" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" transform="rotate(-90 36 36)" />
      <text x="36" y="40" text-anchor="middle" font-size="14" font-weight="600" fill="${color}">${percentage}%</text>
    </svg>
  `;
}
