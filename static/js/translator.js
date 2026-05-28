/* ── Pillar 1: Translation Engine ────────────────────────────────── */

const tabUpload  = document.getElementById("tab-upload");
const tabPaste   = document.getElementById("tab-paste");
const panelUpload= document.getElementById("panel-upload");
const panelPaste = document.getElementById("panel-paste");
const dropZone   = document.getElementById("drop-zone");
const fileInput  = document.getElementById("file-input");
const fileNameEl = document.getElementById("file-name");
const textInput  = document.getElementById("text-input");
const charCount  = document.getElementById("char-count");
const translateBtn= document.getElementById("translate-btn");
const demoBtn    = document.getElementById("load-demo-btn");

let selectedFile = null;
let activeTab = "upload";

// ── Tab switching ─────────────────────────────────────────────────
function switchTab(tab) {
  activeTab = tab;
  if (tab === "upload") {
    tabUpload.setAttribute("aria-selected", "true");
    tabPaste.setAttribute("aria-selected", "false");
    tabUpload.classList.add("active"); tabPaste.classList.remove("active");
    panelUpload.hidden = false; panelPaste.hidden = true;
  } else {
    tabPaste.setAttribute("aria-selected", "true");
    tabUpload.setAttribute("aria-selected", "false");
    tabPaste.classList.add("active"); tabUpload.classList.remove("active");
    panelPaste.hidden = false; panelUpload.hidden = true;
  }
  updateBtn();
}
tabUpload.addEventListener("click", () => switchTab("upload"));
tabPaste.addEventListener("click",  () => switchTab("paste"));

// ── File handling ─────────────────────────────────────────────────
function setFile(file) {
  selectedFile = file;
  fileNameEl.textContent = `✓ ${file.name} (${(file.size/1024).toFixed(0)} KB)`;
  fileNameEl.hidden = false;
  updateBtn();
}
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") fileInput.click(); });
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault(); dropZone.classList.remove("drag-over");
  const f = e.dataTransfer.files[0];
  if (f) setFile(f);
});

textInput.addEventListener("input", () => {
  charCount.textContent = `${textInput.value.length.toLocaleString()} characters`;
  updateBtn();
});

function updateBtn() {
  const hasFile = activeTab === "upload" && selectedFile;
  const hasText = activeTab === "paste"  && textInput.value.trim().length >= 50;
  translateBtn.disabled = !(hasFile || hasText);
}

// ── Demo data (when AI is not configured) ─────────────────────────
const DEMO = {
  doc_type: "Rental Lease Agreement",
  summary: "This is a standard one-year residential lease. It includes several clauses that are weighted in the landlord's favor, particularly around rent increases, repairs, and early termination. Pay close attention to the automatic renewal clause.",
  red_flags: [
    "Automatic renewal clause — the lease renews for another year with only 30 days' notice required from you.",
    "Landlord can increase rent by up to 10% with only 30 days' notice.",
    "Early termination fee equals 2 months' rent — very high."
  ],
  action_items: [
    "Mark your calendar 60 days before lease ends to decide whether to renew.",
    "Ask landlord to negotiate the rent-increase cap before signing.",
    "Photograph the unit thoroughly before move-in and submit to landlord in writing."
  ],
  clauses: [
    {
      title: "Rent Payment",
      original: "Tenant shall pay the monthly rent of $1,200 on the first day of each calendar month…",
      plain_english: "You owe $1,200 rent every month, due on the 1st. If it's late, you pay an extra $60 after a 5-day grace period.",
      risk_level: "low",
      why_it_matters: "Standard clause — just make sure you know the grace period."
    },
    {
      title: "Automatic Renewal",
      original: "Unless Tenant provides written notice of non-renewal at least 30 days prior to expiration…",
      plain_english: "If you don't tell the landlord in writing 30 days before the lease ends that you're leaving, the lease automatically renews for another full year.",
      risk_level: "high",
      why_it_matters: "You could be locked in for another year if you forget to give notice."
    },
    {
      title: "Rent Increase",
      original: "Landlord reserves the right to increase monthly rent by no more than 10% upon 30 days written notice…",
      plain_english: "Your landlord can raise your rent by up to 10% every year as long as they tell you 30 days in advance.",
      risk_level: "medium",
      why_it_matters: "On $1,200 rent, this could mean a $120/month increase — try to negotiate a smaller cap."
    },
    {
      title: "Repairs & Maintenance",
      original: "Tenant shall be responsible for all repairs under $100. Landlord shall respond to repair requests within 14 business days…",
      plain_english: "You pay for any small fixes under $100. Your landlord has up to 14 business days (almost 3 weeks) to respond to repair requests.",
      risk_level: "medium",
      why_it_matters: "14 business days is a long wait for urgent repairs like plumbing leaks."
    },
    {
      title: "Early Termination",
      original: "In the event of early termination by Tenant, Tenant shall pay a fee equal to two months' rent…",
      plain_english: "If you need to leave before the lease ends, you owe the landlord $2,400 (two months' rent) as a penalty — on top of regular rent owed.",
      risk_level: "high",
      why_it_matters: "This is very high. Try to negotiate this down to one month before signing."
    }
  ]
};

if (demoBtn) {
  demoBtn.addEventListener("click", (e) => {
    e.preventDefault();
    renderResults(DEMO);
  });
}

// ── Translate action ──────────────────────────────────────────────
translateBtn.addEventListener("click", async () => {
  const formData = new FormData();
  if (activeTab === "upload" && selectedFile) {
    formData.append("file", selectedFile);
  } else {
    formData.append("text", textInput.value);
  }

  showLoading();

  try {
    const res  = await fetch("/api/translate", { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Translation failed.");
    renderResults(data);
  } catch (err) {
    showError(err.message);
  }
});

// ── Render results ────────────────────────────────────────────────
function renderResults(data) {
  document.getElementById("results-placeholder").hidden = true;
  document.getElementById("results-loading").hidden     = true;
  document.getElementById("results-error").hidden       = true;
  document.getElementById("results-content").hidden     = false;

  // Doc type badge
  const badge = document.getElementById("doc-type-badge");
  badge.textContent = data.doc_type || "Legal Document";

  // Summary
  document.getElementById("summary-box").textContent = data.summary || "";

  // Red flags
  const rfBox  = document.getElementById("red-flags-box");
  const rfList = document.getElementById("red-flags-list");
  if (data.red_flags && data.red_flags.length) {
    rfList.innerHTML = data.red_flags.map(f => `<li>${f}</li>`).join("");
    rfBox.hidden = false;
  }

  // Action items
  const aiBox  = document.getElementById("action-items-box");
  const aiList = document.getElementById("action-items-list");
  if (data.action_items && data.action_items.length) {
    aiList.innerHTML = data.action_items.map(a => `<li>${a}</li>`).join("");
    aiBox.hidden = false;
  }

  // Clauses
  const container = document.getElementById("clauses-container");
  container.innerHTML = "";
  const template  = document.getElementById("clause-template");
  (data.clauses || []).forEach(clause => {
    const card = template.content.cloneNode(true);
    card.querySelector(".clause-title").textContent = clause.title;

    const badge = card.querySelector(".risk-badge");
    const rl = clause.risk_level || "low";
    badge.textContent = rl.charAt(0).toUpperCase() + rl.slice(1) + " Risk";
    badge.classList.add(`risk-${rl}`);

    card.querySelector(".clause-original-text").textContent = clause.original;
    card.querySelector(".clause-plain-text").textContent    = clause.plain_english;
    card.querySelector(".clause-why").textContent           = clause.why_it_matters ? `→ ${clause.why_it_matters}` : "";
    container.appendChild(card);
  });

  // Scroll to results
  document.getElementById("results-content").scrollIntoView({ behavior: "smooth", block: "start" });
}

function showLoading() {
  document.getElementById("results-placeholder").hidden = true;
  document.getElementById("results-content").hidden     = true;
  document.getElementById("results-error").hidden       = true;
  document.getElementById("results-loading").hidden     = false;
}

function showError(msg) {
  document.getElementById("results-loading").hidden = true;
  document.getElementById("results-content").hidden = true;
  document.getElementById("results-error").hidden   = false;
  document.getElementById("error-message").textContent = msg;
}

window.resetTranslator = function() {
  document.getElementById("results-error").hidden       = true;
  document.getElementById("results-placeholder").hidden = false;
};

// ── Copy & Print ──────────────────────────────────────────────────
document.getElementById("copy-btn")?.addEventListener("click", () => {
  const summary = document.getElementById("summary-box").textContent;
  const flags   = [...document.querySelectorAll("#red-flags-list li")].map(l => "⚠ " + l.textContent).join("\n");
  const actions = [...document.querySelectorAll("#action-items-list li")].map(l => "✓ " + l.textContent).join("\n");
  navigator.clipboard.writeText(`Summary:\n${summary}\n\nRed Flags:\n${flags}\n\nAction Items:\n${actions}`)
    .then(() => { const btn = document.getElementById("copy-btn"); btn.textContent = "✓ Copied!"; setTimeout(() => { btn.textContent = "📋 Copy Summary"; }, 2000); });
});
document.getElementById("print-btn")?.addEventListener("click", () => window.print());
