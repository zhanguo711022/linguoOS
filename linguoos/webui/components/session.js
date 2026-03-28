export function renderSession(container, state, handlers) {
  container.innerHTML = `
    <div class="card">
      <div class="section-title" data-i18n="session.title">Learning Session</div>
      <div class="subtle" data-i18n="session.subtitle">Start a guided session with the engine.</div>
      <div class="grid-2" style="margin-top: 14px; align-items: center;">
        <div>
          <input id="sessionUserId" class="input" type="text" data-i18n-placeholder="session.userPlaceholder" />
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button id="sessionStart" class="btn btn-primary" type="button" data-i18n="session.start">Start Learning</button>
          <span id="sessionLoading" class="spinner" style="display: none;"></span>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="session.chatTitle">Dialog</div>
      <div class="chat" id="chatLog"></div>
      <div style="margin-top: 12px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <input id="sessionMessage" class="input" type="text" data-i18n-placeholder="session.messagePlaceholder" />
        <button id="sessionSend" class="btn btn-ghost" type="button" data-i18n="session.send">Send</button>
        <button id="sessionRecord" class="btn btn-ghost" type="button" data-i18n="session.record">Record</button>
        <button id="sessionSpeakLast" class="btn btn-ghost" type="button" data-i18n="session.speakLast">Speak Last</button>
      </div>
      <div id="sessionVoiceStatus" class="subtle" style="margin-top: 8px;"></div>
    </div>

    <div class="card">
      <div class="section-title" data-i18n="session.modeTitle">Action Zone</div>
      <div id="modePanel" class="mode-panel"></div>
    </div>
  `;

  const userInput = container.querySelector("#sessionUserId");
  const startButton = container.querySelector("#sessionStart");
  const chatLog = container.querySelector("#chatLog");
  const modePanel = container.querySelector("#modePanel");
  const sessionLoading = container.querySelector("#sessionLoading");
  const sessionMessage = container.querySelector("#sessionMessage");
  const sessionSend = container.querySelector("#sessionSend");
  const sessionRecord = container.querySelector("#sessionRecord");
  const sessionSpeakLast = container.querySelector("#sessionSpeakLast");
  const sessionVoiceStatus = container.querySelector("#sessionVoiceStatus");

  userInput.addEventListener("change", (event) => {
    handlers.onUserChange(event.target.value);
  });

  startButton.addEventListener("click", () => {
    handlers.onStart();
  });

  sessionSend.addEventListener("click", () => {
    handlers.onMessage(sessionMessage.value);
    sessionMessage.value = "";
  });

  if (sessionRecord) {
    sessionRecord.addEventListener("click", () => {
      if (handlers.onRecord) handlers.onRecord();
    });
  }

  if (sessionSpeakLast) {
    sessionSpeakLast.addEventListener("click", () => {
      if (handlers.onSpeakLast) handlers.onSpeakLast();
    });
  }

  const renderChat = () => {
    chatLog.innerHTML = state.chat
      .map(
        (item) =>
          `<div class="bubble ${item.role}">${item.content}</div>`
      )
      .join("");
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  const renderMode = () => {
    if (state.loading) {
      modePanel.innerHTML = `<div class="subtle"><span class="spinner"></span> ${handlers.t("session.loading")}</div>`;
      return;
    }

    if (!state.currentMode) {
      modePanel.innerHTML = `<div class="subtle">${handlers.t("session.idle")}</div>`;
      return;
    }

    handlers.renderMode(state.currentMode, modePanel);
  };

  const update = () => {
    userInput.value = state.userId;
    sessionLoading.style.display = state.loading ? "inline-block" : "none";
    renderChat();
    renderMode();
    if (sessionVoiceStatus) {
      sessionVoiceStatus.textContent = state.voiceStatus || "";
    }
  };

  update();
  return { update };
}
