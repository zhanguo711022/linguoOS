// ── LinguoOS home.js ── onboarding → level → module → practice + 今日任务 ──

let _state = {};  // 当前学习状态

export function render(container, { state, actions }) {
  _state = state;

  // 判断用户状态
  const savedLevel = localStorage.getItem("linguoos-level");
  if (!savedLevel) {
    renderOnboarding(container, actions);
  } else {
    const savedModule = localStorage.getItem("linguoos-module");
    if (!savedModule) {
      renderLevelSelect(container, actions, savedLevel);
    } else {
      renderHome(container, actions, savedLevel, savedModule);
    }
  }
}

// ────────────────────────────────────────────
// 1. Onboarding（首次进入）
// ────────────────────────────────────────────
async function renderOnboarding(container, actions) {
  container.innerHTML = `
    <div style="min-height:80vh;display:flex;flex-direction:column;justify-content:flex-end;padding:24px 16px 40px;">
      <div id="bubbleArea" style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:12px;"></div>
      <div id="levelCardArea" style="display:none;margin-top:20px;"></div>
    </div>`;

  const bubbleArea = container.querySelector("#bubbleArea");

  async function addBubble(text, isAI = true, delay = 0) {
    await new Promise(r => setTimeout(r, delay));
    const div = document.createElement("div");
    div.style.cssText = `
      max-width:85%;align-self:${isAI ? "flex-start" : "flex-end"};
      background:${isAI ? "linear-gradient(135deg,#667eea,#764ba2)" : "#f0f0f5"};
      color:${isAI ? "white" : "#333"};
      padding:12px 16px;border-radius:${isAI ? "4px 16px 16px 16px" : "16px 16px 4px 16px"};
      font-size:14px;line-height:1.6;animation:fadeIn 0.3s ease;
    `;
    div.textContent = text;
    bubbleArea.appendChild(div);
    bubbleArea.scrollTop = bubbleArea.scrollHeight;
  }

  await addBubble("你好！我是 Lingo，你的 AI 语言老师 👋", true, 300);
  window._onboardSpeak = () => actions.speakText("Hello! I am Lingo, your AI language teacher. Welcome to LinguoOS!");
  document.addEventListener("click", () => { if(window._onboardSpeak){ window._onboardSpeak(); window._onboardSpeak=null; } }, {once:true});

  await addBubble("学语言最好的方式：先听、再说、然后读写 🎧", true, 1800);
  await addBubble("我会用这个顺序带你学，每天只需要 10 分钟 ⏱️", true, 2400);
  await addBubble("先告诉我，你现在的英语水平怎么样？", true, 3200);

  // 显示级别选择
  const levelCardArea = container.querySelector("#levelCardArea");
  levelCardArea.style.display = "block";
  levelCardArea.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      ${[
        {id:"starter",    label:"零基础",    desc:"从字母开始",  emoji:"🌱"},
        {id:"elementary", label:"初级",      desc:"日常对话",    emoji:"📗"},
        {id:"intermediate",label:"中级",     desc:"精准表达",    emoji:"📘"},
        {id:"upper",      label:"中高级",    desc:"学术写作",    emoji:"📙"},
        {id:"advanced",   label:"高级",      desc:"修辞辩论",    emoji:"🏆"},
        {id:"ielts",      label:"雅思/考试", desc:"备考强化",    emoji:"🎓"},
      ].map(l => `
        <button onclick="window._selectLevel('${l.id}')"
          style="background:white;border:2px solid #eee;border-radius:14px;padding:14px 10px;
          cursor:pointer;text-align:center;transition:all 0.2s;">
          <div style="font-size:24px">${l.emoji}</div>
          <div style="font-weight:700;font-size:14px;margin-top:4px">${l.label}</div>
          <div style="color:#888;font-size:11px">${l.desc}</div>
        </button>
      `).join("")}
    </div>`;

  window._selectLevel = async (levelId) => {
    localStorage.setItem("linguoos-level", levelId);
    await addBubble(`太好了！我为你准备 ${levelId} 级的课程 🎯`, true, 0);
    actions.speakText("Perfect! Let me pick your first lesson.");
    setTimeout(() => renderLevelSelect(container, actions, levelId), 1200);
  };
}

// ────────────────────────────────────────────
// 2. 选模块
// ────────────────────────────────────────────
async function renderLevelSelect(container, actions, levelId) {
  container.innerHTML = `<div style="padding:16px"><div class="skeleton" style="height:40px;margin-bottom:16px;"></div><div class="skeleton" style="height:200px;"></div></div>`;

  try {
    const resp = await fetch(`/api/v1/curriculum/modules/${levelId}`, {
      headers: {"X-Visitor-Id": getVisitorId()}
    });
    const data = await resp.json();
    const modules = Array.isArray(data) ? data : (data.modules || []);

    // 获取进度
    let progress = {};
    try {
      const pr = await fetch("/api/v1/progress/summary", { headers: {"X-Visitor-Id": getVisitorId()} });
      const pd = await pr.json();
      progress = pd.modules || {};
    } catch(e) {}

    // 打卡 streak
    const today = new Date().toDateString();
    const lastDate = localStorage.getItem("linguoos-last-date");
    let streak = parseInt(localStorage.getItem("linguoos-streak") || "0");
    if (lastDate !== today) {
      const yesterday = new Date(Date.now() - 86400000).toDateString();
      streak = lastDate === yesterday ? streak + 1 : 1;
      localStorage.setItem("linguoos-streak", streak);
      localStorage.setItem("linguoos-last-date", today);
    }

    // 找今日任务（第一个未完成模块）
    const todayModule = modules.find(m => (progress[m.id] || 0) < 80) || modules[0];
    const todayScore = todayModule ? Math.round(progress[todayModule.id] || 0) : 0;

    container.innerHTML = `
      <div style="padding:16px;">
        <!-- 今日任务卡片 -->
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:16px;margin-bottom:16px;color:white;">
          <div style="font-size:11px;opacity:0.8;margin-bottom:2px">📅 今日任务</div>
          <div style="font-size:15px;font-weight:700;margin-bottom:10px">
            ${todayScore > 0 ? "继续学习：" : "开始学习："}<span id="todayTaskName">${todayModule?.name || "—"}</span>
          </div>
          <div style="background:rgba(255,255,255,0.25);border-radius:99px;height:6px;overflow:hidden;">
            <div style="background:white;border-radius:99px;height:6px;width:${todayScore}%;transition:width 0.8s ease;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;opacity:0.85;">
            <span>${todayScore}% 完成</span>
            <span>🔥 连续 ${streak} 天</span>
          </div>
        </div>

        <!-- 模块列表 -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <div style="font-weight:700;font-size:16px;">选择模块开始练习</div>
          <button onclick="localStorage.removeItem('linguoos-level');location.reload()"
            style="background:none;border:none;color:#888;font-size:12px;cursor:pointer;">切换级别</button>
        </div>

        <div id="moduleList" style="display:flex;flex-direction:column;gap:10px;"></div>
      </div>`;

    const moduleList = container.querySelector("#moduleList");
    modules.forEach(mod => {
      const score = Math.round(progress[mod.id] || 0);
      const isLocked = false; // 暂全开放
      const isDone = score >= 80;
      const btnLabel = isDone ? "复习" : score > 0 ? "继续" : "开始";
      const btnColor = isDone ? "#43e97b" : "#667eea";

      const card = document.createElement("div");
      card.style.cssText = "background:white;border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:14px;box-shadow:0 2px 8px rgba(0,0,0,0.06);";
      card.innerHTML = `
        <div style="flex:1;min-width:0;">
          <div style="font-weight:600;font-size:14px;display:flex;align-items:center;gap:6px;">
            ${isDone ? "✅" : isLocked ? "🔒" : "📖"} ${mod.name}
          </div>
          <div style="color:#888;font-size:12px;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${mod.description || ""}</div>
          <div style="margin-top:8px;background:#f0f0f5;border-radius:99px;height:4px;overflow:hidden;">
            <div style="background:${btnColor};height:4px;border-radius:99px;width:${score}%;transition:width 0.6s;"></div>
          </div>
        </div>
        <button style="background:${btnColor};color:white;border:none;border-radius:10px;padding:8px 14px;font-size:13px;font-weight:600;cursor:pointer;flex-shrink:0;"
          onclick="window._startModule('${mod.id}','${mod.name}')">
          ${btnLabel}
        </button>`;
      moduleList.appendChild(card);
    });

    window._startModule = (modId, modName) => {
      localStorage.setItem("linguoos-module", modId);
      localStorage.setItem("linguoos-module-name", modName);
      renderPractice(container, actions, levelId, modId);
    };

  } catch(e) {
    container.innerHTML = `<div style="padding:32px;text-align:center;color:#888;">加载失败，请重试<br><button onclick="location.reload()" style="margin-top:12px;padding:8px 20px;border-radius:8px;border:1px solid #ddd;cursor:pointer;">重试</button></div>`;
  }
}

// ────────────────────────────────────────────
// 3. 练习
// ────────────────────────────────────────────
async function renderPractice(container, actions, levelId, moduleId) {
  container.innerHTML = `<div style="padding:16px"><div class="skeleton" style="height:300px;"></div></div>`;

  try {
    // 并行获取讲解 + 题目
    const [exResp, qResp] = await Promise.all([
      fetch(`/api/v1/curriculum/explain/${moduleId}`, { headers: {"X-Visitor-Id": getVisitorId()} }),
      fetch(`/api/v1/curriculum/questions/${moduleId}`, { headers: {"X-Visitor-Id": getVisitorId()} }),
    ]);
    const exData = await exResp.json();
    const qData = await qResp.json();

    const ex = Array.isArray(exData) ? exData[0] : (exData.explanation || exData);
    const questions = Array.isArray(qData) ? qData : (qData.questions || []);

    const modName = localStorage.getItem("linguoos-module-name") || moduleId;
    let current = 0;
    let correct = 0;

    function showQ(q, idx) {
      const total = questions.length;
      container.innerHTML = `
        <div style="padding:16px;">
          <!-- 返回按钮 -->
          <button onclick="window._backToModules()" style="background:none;border:none;color:#667eea;font-size:13px;cursor:pointer;margin-bottom:12px;">← 返回模块列表</button>

          <!-- 讲解卡片 -->
          <div style="background:linear-gradient(135deg,#667eea22,#764ba222);border-radius:14px;padding:14px;margin-bottom:16px;border:1px solid #667eea33;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
              <div style="font-size:12px;color:#667eea;font-weight:600;">📖 ${modName}</div>
              <button id="listenBtn"
                style="background:rgba(102,126,234,0.15);border:none;border-radius:99px;padding:5px 12px;font-size:12px;color:#667eea;cursor:pointer;">
                🔊 听老师讲解
              </button>
            </div>
            <div style="font-size:13px;line-height:1.7;color:#444;">${ex.one_liner || ex.content || "今天我们来学习这个模块的核心知识点。"}</div>
            ${ex.example ? `<div style="margin-top:8px;font-size:12px;color:#888;font-style:italic;">例：${ex.example}</div>` : ""}
          </div>

          <!-- 进度 -->
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div style="font-size:13px;color:#888;">第 ${idx+1} / ${total} 题</div>
            <div style="font-size:13px;color:#43e97b;font-weight:600;">✓ ${correct} 题正确</div>
          </div>
          <div style="background:#f0f0f5;border-radius:99px;height:4px;margin-bottom:16px;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#667eea,#43e97b);height:4px;border-radius:99px;width:${Math.round(idx/total*100)}%;transition:width 0.4s;"></div>
          </div>

          <!-- 题目 -->
          <div id="practiceArea">
            <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:20px;">
              <div class="q-prompt-text" style="font-size:16px;font-weight:600;line-height:1.6;flex:1;">${q.prompt}</div>
              <button onclick="speakText && speakText(this.previousElementSibling.textContent)"
                style="background:none;border:none;cursor:pointer;font-size:20px;flex-shrink:0;">🔊</button>
            </div>
            <div id="options"></div>
            <div id="fb" style="margin-top:16px;"></div>
            <button id="nextBtn" style="display:none;width:100%;margin-top:14px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:12px;padding:14px;font-size:15px;font-weight:600;cursor:pointer;">
              ${idx + 1 < total ? "下一题 →" : "完成练习 🎉"}
            </button>
          </div>
        </div>`;

      // 听讲解按钮
      const listenBtn = container.querySelector("#listenBtn");
      listenBtn.onclick = async () => {
        if (listenBtn.disabled) return;
        listenBtn.disabled = true;
        listenBtn.style.opacity = "0.5";
        const text = [ex.one_liner || ex.content, ex.example].filter(Boolean).join(". ");
        await actions.speakText(text);
        listenBtn.disabled = false;
        listenBtn.style.opacity = "1";
      };

      // 选项
      const opts = container.querySelector("#options");
      (q.options || []).forEach(opt => {
        const btn = document.createElement("button");
        btn.style.cssText = `
          display:block;width:100%;text-align:left;padding:13px 16px;margin-bottom:10px;
          background:#f8f9ff;border:2px solid #eee;border-radius:12px;
          font-size:14px;cursor:pointer;white-space:normal;word-break:break-word;line-height:1.5;`;
        btn.textContent = opt;
        btn.onclick = async () => {
          opts.querySelectorAll("button").forEach(b => b.disabled = true);
          const ok = opt === q.answer;
          if (ok) correct++;
          btn.style.background = ok ? "#e8f8f0" : "#fff0f0";
          btn.style.borderColor = ok ? "#43e97b" : "#f5576c";

          // 标出正确答案
          if (!ok) {
            opts.querySelectorAll("button").forEach(b => {
              if (b.textContent === q.answer) {
                b.style.background = "#e8f8f0";
                b.style.borderColor = "#43e97b";
              }
            });
          }

          // 反馈
          const fb = container.querySelector("#fb");
          fb.innerHTML = ok
            ? `<div style="color:#2d8a4e;font-weight:600;">✅ 正确！</div>`
            : `<div style="color:#c0392b;font-weight:600;margin-bottom:8px;">❌ 答案是：${q.answer}</div>
               <div style="color:#888;font-size:13px;">${q.explanation || ""}</div>`;

          // 如果答错，调 AI 解释
          if (!ok && q.prompt) {
            fb.innerHTML += `<div style="color:#aaa;font-size:12px;margin-top:8px;">🤖 Lingo 正在分析...</div>`;
            try {
              const r = await fetch("/api/v1/tutor/explain", {
                method: "POST",
                headers: {"Content-Type":"application/json","X-Visitor-Id":getVisitorId()},
                body: JSON.stringify({
                  question: q.prompt,
                  wrong_answer: opt,
                  correct_answer: q.answer,
                  module_id: moduleId,
                  language: "en"
                })
              });
              const ai = await r.json();
              if (ai.explanation) {
                fb.innerHTML += `
                  <div style="margin-top:10px;background:#f8f9ff;border-radius:10px;padding:12px;border:1px solid #667eea33;">
                    <div style="font-size:12px;color:#667eea;font-weight:600;margin-bottom:4px;">🤖 Lingo 说：</div>
                    <div style="font-size:13px;line-height:1.6;">${ai.explanation}</div>
                    ${ai.encouragement ? `<div style="margin-top:6px;font-size:12px;color:#f093fb;">${ai.encouragement}</div>` : ""}
                  </div>`;
                actions.speakText(ai.explanation);
              }
            } catch(e) {
              actions.speakText(ok ? "Correct! Well done!" : `The answer is: ${q.answer}`);
            }
          } else {
            actions.speakText(ok ? "Correct! Well done!" : `The answer is: ${q.answer}`);
          }

          container.querySelector("#nextBtn").style.display = "block";
        };
        opts.appendChild(btn);
      });

      // 下一题 / 完成
      container.querySelector("#nextBtn").onclick = () => {
        if (idx + 1 < total) {
          showQ(questions[idx + 1], idx + 1);
        } else {
          showResult(correct, total);
        }
      };
    }

    function showResult(correct, total) {
      const pct = Math.round(correct / total * 100);
      container.innerHTML = `
        <div style="padding:32px 16px;text-align:center;">
          <div style="font-size:48px;margin-bottom:12px;">${pct >= 80 ? "🏆" : pct >= 60 ? "👍" : "💪"}</div>
          <div style="font-size:22px;font-weight:700;margin-bottom:8px;">${correct} / ${total} 正确</div>
          <div style="font-size:15px;color:#888;margin-bottom:24px;">
            ${pct >= 80 ? "太棒了！模块完成！" : pct >= 60 ? "不错，继续加油！" : "多练几次你会更好！"}
          </div>
          <div style="background:#f8f9ff;border-radius:16px;padding:20px;margin-bottom:24px;">
            <div style="font-size:32px;font-weight:800;color:#667eea;">${pct}%</div>
            <div style="font-size:13px;color:#888;margin-top:4px;">本次得分</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <button onclick="renderPractice_global()" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:12px;padding:14px;font-size:15px;font-weight:600;cursor:pointer;">再练一次 🔄</button>
            <button onclick="window._backToModules()" style="background:#f8f9ff;border:2px solid #eee;border-radius:12px;padding:14px;font-size:15px;font-weight:600;cursor:pointer;">选其他模块 📚</button>
          </div>
        </div>`;

      actions.speakText(pct >= 67 ? "Well done! You are making great progress!" : "Keep going! Practice makes perfect!");

      if (pct >= 80) {
        actions.celebrate();
        actions.showToast(`🎉 模块完成！${modName} 达人解锁！`);
      }
    }

    window._backToModules = () => {
      localStorage.removeItem("linguoos-module");
      localStorage.removeItem("linguoos-module-name");
      renderLevelSelect(container, actions, levelId);
    };
    window.renderPractice_global = () => renderPractice(container, actions, levelId, moduleId);

    if (questions.length > 0) {
      showQ(questions[0], 0);
    } else {
      container.innerHTML = `<div style="padding:32px;text-align:center;color:#888;">暂无题目</div>`;
    }

  } catch(e) {
    container.innerHTML = `<div style="padding:32px;text-align:center;color:#888;">加载失败<br><button onclick="location.reload()" style="margin-top:12px;padding:8px 20px;border-radius:8px;border:1px solid #ddd;cursor:pointer;">重试</button></div>`;
  }
}

// ────────────────────────────────────────────
// 4. 已选模块后的首页（含今日任务）
// ────────────────────────────────────────────
function renderHome(container, actions, levelId, moduleId) {
  renderLevelSelect(container, actions, levelId);
}

function getVisitorId() {
  let id = localStorage.getItem("linguoos-visitor-id");
  if (!id) { id = crypto.randomUUID(); localStorage.setItem("linguoos-visitor-id", id); }
  return id;
}
