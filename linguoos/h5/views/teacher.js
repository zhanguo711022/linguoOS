export function render(container, { actions }) {
  container.innerHTML = `
    <section class="banner">
      <div style="font-size:18px;font-weight:600;">老师在线辅助</div>
      <div style="margin-top:6px;opacity:0.9;">个人导师模式即将上线</div>
    </section>

    <section style="margin-top:16px;display:grid;gap:12px;">
      ${["💬 实时消息辅导", "📹 视频答疑（即将上线）", "📝 作业批改", "📊 个人学习报告"]
        .map(
          (item) => `
        <div class="lock-card">
          <div>${item}</div>
          <div>🔒</div>
        </div>
      `
        )
        .join("")}
    </section>

    <section class="card" style="margin-top:16px;">
      <div style="font-weight:600;">订阅老师功能通知</div>
      <div style="color:var(--text-light);font-size:12px;margin-top:4px;">留下联系方式，优先体验。</div>
      <form class="input-group" id="subscribeForm" style="margin-top:12px;">
        <input type="email" id="emailInput" placeholder="输入邮箱" required />
        <button class="primary-button" type="submit">提交</button>
      </form>
      <div id="subscribeResult" style="display:none;margin-top:10px;color:var(--text-light);"></div>
    </section>
  `;

  const form = container.querySelector("#subscribeForm");
  const result = container.querySelector("#subscribeResult");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    result.style.display = "block";
    result.textContent = "已登记，老师功能上线第一时间通知您！";
    actions.showToast("订阅成功" );
    form.reset();
  });
}
