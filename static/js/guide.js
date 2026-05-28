/* ── Pillar 2: Action Guide — checklist, progress, letter gen ───── */

const SLUG  = window.GUIDE_SLUG;
const TOTAL = window.CHECKLIST_TOTAL || 0;
const STORAGE_KEY = `guide-progress-${SLUG}`;

// ── Persist & restore checklist ───────────────────────────────────
function saveProgress() {
  const checked = [...document.querySelectorAll(".check-input")]
    .map(cb => cb.checked);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(checked));
}

function restoreProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    document.querySelectorAll(".check-input").forEach((cb, i) => {
      if (saved[i]) {
        cb.checked = true;
        cb.closest(".checklist-item").classList.add("done");
      }
    });
    updateProgress();
  } catch {}
}

function updateProgress() {
  const done  = document.querySelectorAll(".check-input:checked").length;
  const fill  = document.getElementById("progress-fill");
  const label = document.getElementById("progress-label");
  const bar   = document.querySelector(".progress-bar");
  if (!fill || !label || !bar) return;

  const pct = TOTAL > 0 ? Math.round((done / TOTAL) * 100) : 0;
  fill.style.width = pct + "%";
  bar.setAttribute("aria-valuenow", done);
  label.textContent = `${done} of ${TOTAL} steps complete`;
}

document.querySelectorAll(".check-input").forEach(cb => {
  cb.addEventListener("change", () => {
    const item = cb.closest(".checklist-item");
    item.classList.toggle("done", cb.checked);
    saveProgress();
    updateProgress();
  });
});

restoreProgress();

// ── "Generate Letter" buttons ─────────────────────────────────────
document.querySelectorAll(".generate-letter-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const letterSection = document.getElementById("letter-section");
    if (letterSection) {
      letterSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// ── AI Letter generation ──────────────────────────────────────────
const genBtn = document.getElementById("gen-letter-btn");
genBtn?.addEventListener("click", async () => {
  const details = {
    "Your Name":      document.getElementById("lf-name")?.value,
    "Your Address":   document.getElementById("lf-address")?.value,
    "Other Party":    document.getElementById("lf-other-name")?.value,
    "Other Address":  document.getElementById("lf-other-address")?.value,
    "Amount":         document.getElementById("lf-amount")?.value,
    "Key Date":       document.getElementById("lf-date")?.value,
    "Extra Details":  document.getElementById("lf-details")?.value,
  };

  genBtn.disabled = true;
  genBtn.innerHTML = '<span class="spinner"></span> Generating…';

  try {
    const res  = await fetch("/api/generate-letter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ guide_slug: SLUG, details }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    const output = document.getElementById("letter-output");
    output.innerHTML = `<pre class="letter-pre">${escapeHtml(data.letter)}</pre>`;
    output.scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (err) {
    alert("Letter generation failed: " + err.message);
  } finally {
    genBtn.disabled = false;
    genBtn.textContent = "Generate Letter with AI ✨";
  }
});

// ── Copy letter ───────────────────────────────────────────────────
document.getElementById("copy-letter-btn")?.addEventListener("click", () => {
  const pre = document.querySelector(".letter-pre");
  if (!pre) return;
  navigator.clipboard.writeText(pre.textContent).then(() => {
    const btn = document.getElementById("copy-letter-btn");
    btn.textContent = "✓ Copied!";
    setTimeout(() => { btn.textContent = "📋 Copy Letter"; }, 2000);
  });
});

function escapeHtml(s) {
  return (s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
