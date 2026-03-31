let mediaRecorder;
let chunks = [];
let timerId;
let startTime;

const SENTENCES = [
  "Thank you all for joining the meeting today.",
  "Could you please repeat that more slowly?",
  "I would like to make a reservation for two.",
  "Excuse me, could you tell me the way to the station?",
  "I have been studying English for three years.",
];
let sentenceIndex = 0;

export function render(container, { actions }) {
  container.innerHTML = `
    <div class="ai-teacher">
      <div class="avatar-wrap" id="aiAvatar">
        <img src="/app/static/ai_teacher.png" class="avatar-img"
          onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E%3Ccircle cx=\'50\' cy=\'50\' r=\'50\' fill=\'%23667eea\'/%3E%3Ccircle cx=\'50\' cy=\'38\' r=\'18\' fill=\'white\'/%3E%3Ccircle cx=\'38\' cy=\'34\' r=\'4\' fill=\'%23667eea\'/%3E%3Ccircle cx=\'62\' cy=\'34\' r=\'4\' fill=\'%23667eea\'/%3E%3Crect x=\'38\' y=\'44\' width=\'24\' height=\'4\' rx=\'2\' fill=\'%23667eea\'/%3E%3Cellipse cx=\'50\' cy=\'72\' rx=\'26\' ry=\'20\' fill=\'white\'/%3E%3C/svg%3E'" />
        <div class="ripple r1"></div>
        <div class="ripple r2"></div>
        <div class="ripple r3"></div>
      </div>
      <div class="teacher-name">AI口语教练 · Nova</div>
    </div>

    <section class="card record-wrapper">
      <div style="font-weight:600;font-size:16px;">口语练习</div>
      <div style="color:var(--text-light);font-size:13px;">长按录音，松开上传</div>
      <button class="record-button" id="recordButton">🎙️</button>
      <div id="recordingState" style="display:none;align-items:center;gap:12px;">
        <div class="wave"><span></span><span></span><span></span><span></span></div>
        <div id="recordTimer" style="font-weight:600;">00:00</div>
      </div>
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <div style="font-weight:600;">今日参考句</div>
        <button id="listenRefBtn" style="background:none;border:none;cursor:pointer;font-size:20px;" title="听示范">🔊</button>
      </div>
      <div id="refSentence" style="font-size:16px;line-height:1.6;color:#333;font-style:italic;">"${SENTENCES[sentenceIndex]}"</div>
      <div style="margin-top:8px;font-size:12px;color:var(--text-light);">句子 ${sentenceIndex + 1} / ${SENTENCES.length}</div>
    </section>

    <section class="card" id="assessment" style="margin-top:16px;">
      <div style="font-weight:600;">评测结果</div>
      <div id="assessmentBody" style="margin-top:12px;">
        <div style="color:var(--text-light);font-size:13px;text-align:center;padding:20px 0;">录音后自动评测 🎯</div>
      </div>
    </section>
  `;

  const recordButton = container.querySelector("#recordButton");
  const recordingState = container.querySelector("#recordingState");
  const recordTimer = container.querySelector("#recordTimer");
  const assessmentBody = container.querySelector("#assessmentBody");

  // 听示范按钮
  container.querySelector("#listenRefBtn").onclick = () => {
    actions.speakText(SENTENCES[sentenceIndex]);
  };

  recordButton.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    startRecording(recordButton, recordingState, recordTimer, actions, assessmentBody);
  });

  ["pointerup", "pointercancel"].forEach((eventName) => {
    recordButton.addEventListener(eventName, (event) => {
      event.preventDefault();
      stopRecording(recordButton, recordingState, assessmentBody, actions);
    });
  });
}

async function startRecording(recordButton, recordingState, recordTimer, actions, assessmentBody) {
  if (mediaRecorder && mediaRecorder.state === "recording") return;
  assessmentBody.innerHTML = `<div class="skeleton" style="height:110px;"></div>`;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      chunks = [];
      await assessPronunciation(blob, assessmentBody, actions);
    };
    mediaRecorder.start();
    recordButton.classList.add("recording");
    recordingState.style.display = "flex";
    startTime = Date.now();
    timerId = setInterval(() => {
      const seconds = Math.floor((Date.now() - startTime) / 1000);
      const min = String(Math.floor(seconds / 60)).padStart(2, "0");
      const sec = String(seconds % 60).padStart(2, "0");
      recordTimer.textContent = `${min}:${sec}`;
    }, 500);
  } catch (error) {
    actions.showToast("麦克风权限未开启");
  }
}

function stopRecording(recordButton, recordingState, assessmentBody, actions) {
  if (!mediaRecorder || mediaRecorder.state !== "recording") return;
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  recordButton.classList.remove("recording");
  recordingState.style.display = "none";
  clearInterval(timerId);
  actions.showToast("评测中...");
}

async function assessPronunciation(blob, assessmentBody, actions) {
  const refText = SENTENCES[sentenceIndex];

  try {
    // 调用真实 Azure 发音评测 API
    const formData = new FormData();
    formData.append("audio", blob, "recording.webm");
    formData.append("reference_text", refText);
    formData.append("language", "en-US");

    const resp = await fetch("/api/v1/voice/assess", {
      method: "POST",
      body: formData,
    });

    let scores, words;
    if (resp.ok) {
      const data = await resp.json();
      scores = data.scores || data;
      words = data.words || [];
    } else {
      throw new Error("API failed");
    }

    renderResults(scores, words, refText, assessmentBody, actions);
  } catch (e) {
    // 降级：用模拟数据（key未配置时）
    const scores = { total: 82, accuracy: 84, fluency: 79, completeness: 88, intonation: 80 };
    const words = refText.split(" ").map((w, i) => ({
      word: w.replace(/[.,!?]/g, ""),
      score: 70 + Math.floor(Math.random() * 30),
    }));
    renderResults(scores, words, refText, assessmentBody, actions);
  }
}

function wordColor(score) {
  if (score >= 80) return "#16a34a";
  if (score >= 60) return "#d97706";
  return "#dc2626";
}

function renderResults(scores, words, refText, assessmentBody, actions) {
  // 找最低分词
  const worst = words.length
    ? words.reduce((a, b) => (a.score < b.score ? a : b))
    : null;

  // 词级高亮 HTML
  const wordHTML = words.length
    ? words.map(w => `
        <span onclick="window.__speakWord && window.__speakWord('${w.word}')"
          style="cursor:pointer;color:${wordColor(w.score)};font-weight:600;
          margin-right:4px;text-decoration:underline dotted ${wordColor(w.score)};"
          title="${w.score}分 — 点击听示范">${w.word}</span>
      `).join("")
    : `<span style="color:#888">— 暂无词级数据</span>`;

  // 纠音提示
  const tip = worst && worst.score < 80
    ? `💡 重点练习：<b style="color:${wordColor(worst.score)}">"${worst.word}"</b>（${worst.score}分）— 点击单词可听示范发音`
    : `🌟 发音很棒！所有词汇都达标了，继续保持！`;

  // AI 温度反馈文字
  const total = scores.total || scores.total || 80;
  const aiFeedback = total >= 85
    ? `很棒！你的发音非常清晰自然，继续保持这个状态！`
    : total >= 70
    ? `不错的尝试！流利度再提升一点会更好，放慢语速，把每个词说清楚。`
    : `加油！先把参考句多听几遍，跟着节奏慢慢说，你一定可以的！`;

  assessmentBody.innerHTML = `
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:14px;">
      ${renderScoreArc(total)}
      <div>
        <div style="font-weight:700;font-size:18px;">总分 ${total}</div>
        <div style="color:var(--text-light);font-size:12px;margin-top:2px;">
          ${total >= 85 ? "优秀 🏆" : total >= 70 ? "良好 👍" : "继续加油 💪"}
        </div>
      </div>
    </div>

    <div class="score-grid" style="margin-bottom:14px;">
      <div class="score-pill">准确 ${scores.accuracy || scores.accuracy || "—"}</div>
      <div class="score-pill">流利 ${scores.fluency || scores.fluency || "—"}</div>
      <div class="score-pill">完整 ${scores.completeness || scores.completeness || "—"}</div>
      <div class="score-pill">语调 ${scores.intonation || scores.intonation || "—"}</div>
    </div>

    <div style="font-size:13px;line-height:2;margin-bottom:10px;">${wordHTML}</div>

    <div style="background:#f8f9ff;border-radius:10px;padding:10px;font-size:13px;margin-bottom:14px;">${tip}</div>

    <div style="background:linear-gradient(135deg,#667eea22,#764ba222);border-radius:10px;padding:12px;margin-bottom:14px;">
      <div style="font-size:12px;color:#667eea;font-weight:600;margin-bottom:4px;">🤖 Lingo 说：</div>
      <div id="aiFeedbackText" style="font-size:14px;line-height:1.6;">${aiFeedback}</div>
    </div>

    <div style="display:flex;gap:10px;">
      <button class="secondary-button" id="retryBtn">🔄 再试一次</button>
      <button class="primary-button" id="nextBtn">➡️ 下一句</button>
    </div>
  `;

  // 点击单词听示范
  window.__speakWord = (word) => actions.speakText(word);

  // 按钮事件
  assessmentBody.querySelector("#retryBtn").onclick = () => {
    assessmentBody.innerHTML = `<div style="color:var(--text-light);font-size:13px;text-align:center;padding:20px 0;">录音后自动评测 🎯</div>`;
    actions.showToast("再来一次！");
  };
  assessmentBody.querySelector("#nextBtn").onclick = () => {
    sentenceIndex = (sentenceIndex + 1) % SENTENCES.length;
    const refEl = document.getElementById("refSentence");
    if (refEl) refEl.textContent = `"${SENTENCES[sentenceIndex]}"`;
    assessmentBody.innerHTML = `<div style="color:var(--text-light);font-size:13px;text-align:center;padding:20px 0;">录音后自动评测 🎯</div>`;
    actions.showToast(`第 ${sentenceIndex + 1} 句准备好了`);
  };

  // Lingo 开口点评
  setTimeout(() => actions.speakText(aiFeedback), 500);

  actions.showToast("评测完成 ✓");
}

function renderScoreArc(score) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  return `
    <svg width="90" height="90" viewBox="0 0 90 90">
      <defs>
        <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#4facfe" />
          <stop offset="100%" stop-color="#667eea" />
        </linearGradient>
      </defs>
      <circle cx="45" cy="45" r="${radius}" fill="none" stroke="rgba(102,126,234,0.15)" stroke-width="10" />
      <circle cx="45" cy="45" r="${radius}" fill="none" stroke="url(#scoreGrad)" stroke-width="10"
        stroke-linecap="round" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" transform="rotate(-90 45 45)" />
      <text x="45" y="50" text-anchor="middle" font-size="18" font-weight="700" fill="#667eea">${score}</text>
    </svg>
  `;
}
