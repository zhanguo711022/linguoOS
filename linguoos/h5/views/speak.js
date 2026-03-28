let mediaRecorder;
let chunks = [];
let timerId;
let startTime;

export function render(container, { actions }) {
  container.innerHTML = `
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
      <div style="font-weight:600;">今日参考句</div>
      <div style="font-size:18px;line-height:1.5;margin-top:10px;">
        "Thank you all for joining the meeting today. Let's align on the goals and next steps."
      </div>
    </section>

    <section class="card" id="assessment" style="margin-top:16px;">
      <div style="font-weight:600;">评测结果</div>
      <div id="assessmentBody" style="margin-top:12px;">
        <div class="skeleton" style="height:110px;"></div>
      </div>
    </section>
  `;

  const recordButton = container.querySelector("#recordButton");
  const recordingState = container.querySelector("#recordingState");
  const recordTimer = container.querySelector("#recordTimer");
  const assessmentBody = container.querySelector("#assessmentBody");

  recordButton.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    startRecording(recordButton, recordingState, recordTimer, actions, assessmentBody);
  });

  ["pointerup", "pointercancel", "pointerleave"].forEach((eventName) => {
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
  actions.showToast("上传录音并评测中...");
}

async function assessPronunciation(blob, assessmentBody, actions) {
  await new Promise((resolve) => setTimeout(resolve, 900));

  const scores = {
    total: 86,
    accuracy: 88,
    fluency: 82,
    completeness: 90,
    intonation: 84,
  };

  assessmentBody.innerHTML = `
    <div style="display:flex;align-items:center;gap:16px;">
      ${renderScoreArc(scores.total)}
      <div>
        <div style="font-weight:600;">总分 ${scores.total}</div>
        <div style="color:var(--text-light);font-size:12px;margin-top:4px;">发音更自信了！</div>
      </div>
    </div>
    <div class="score-grid">
      <div class="score-pill">准确性 ${scores.accuracy}</div>
      <div class="score-pill">流利度 ${scores.fluency}</div>
      <div class="score-pill">完整性 ${scores.completeness}</div>
      <div class="score-pill">语调 ${scores.intonation}</div>
    </div>
    <div style="margin-top:12px;font-size:13px;">
      <span style="color:#16a34a;">Thank you</span>
      <span style="color:#eab308;">joining</span>
      <span style="color:#dc2626;">meeting</span>
      <span style="color:#16a34a;">today</span>
    </div>
    <div style="margin-top:8px;color:var(--text-light);">💡 建议：注意 "meeting" 的 /t/ 收尾，提升清晰度。</div>
    <div style="display:flex;gap:10px;margin-top:14px;">
      <button class="secondary-button" id="retryBtn">再练一次</button>
      <button class="primary-button" id="nextBtn">下一句</button>
    </div>
  `;

  assessmentBody.querySelector("#retryBtn").addEventListener("click", () => {
    actions.showToast("准备重新录音");
  });
  assessmentBody.querySelector("#nextBtn").addEventListener("click", () => {
    actions.celebrate();
    actions.showToast("下一句已加载");
  });

  if (blob.size > 0) {
    actions.showToast("评测完成" );
  }
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
