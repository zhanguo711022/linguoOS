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
      actions.updateChat({ role: "ai", text: "很好！可以试着加一句礼貌的开场，比如：感谢大家今天的时间。" });
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
