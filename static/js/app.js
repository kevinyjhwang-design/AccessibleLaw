/* ── Service Worker registration ───────────────────────────────── */
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js").catch(() => {});
}

/* ── Mobile nav toggle ──────────────────────────────────────────── */
const navToggle = document.getElementById("nav-toggle");
const mainNav   = document.getElementById("main-nav");
navToggle?.addEventListener("click", () => {
  const open = mainNav.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", open);
});
// Close on outside click
document.addEventListener("click", (e) => {
  if (mainNav?.classList.contains("open") &&
      !mainNav.contains(e.target) && !navToggle.contains(e.target)) {
    mainNav.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  }
});

/* ── Live search ────────────────────────────────────────────────── */
const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");

if (searchInput && searchResults) {
  let debounceTimer;

  searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
      return;
    }
    debounceTimer = setTimeout(() => fetchSearch(q), 220);
  });

  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
    }
  });

  document.addEventListener("click", (e) => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.hidden = true;
    }
  });

  async function fetchSearch(q) {
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      renderSearchResults(data.results || []);
    } catch {
      searchResults.hidden = true;
    }
  }

  function renderSearchResults(results) {
    searchResults.innerHTML = "";
    if (results.length === 0) {
      searchResults.hidden = true;
      return;
    }
    results.forEach((r) => {
      const a = document.createElement("a");
      a.href = `/law/${r.id}`;
      a.className = "search-result-item";
      a.setAttribute("role", "option");
      a.innerHTML = `
        <span class="search-result-cat">${r.category}</span>
        <strong>${r.title}</strong>
      `;
      searchResults.appendChild(a);
    });
    searchResults.hidden = false;
  }
}

/* ── Case Finder ────────────────────────────────────────────────── */
const findBtn        = document.getElementById("find-btn");
const storyInput     = document.getElementById("story-input");
const resultsSection = document.getElementById("results-section");
const resultsContainer = document.getElementById("results-container");
const noResults      = document.getElementById("no-results-section");
const cardTemplate   = document.getElementById("result-card-template");

if (findBtn && storyInput) {
  findBtn.addEventListener("click", runCaseFinder);
  storyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) runCaseFinder();
  });
}

async function runCaseFinder() {
  const query = storyInput.value.trim();
  if (!query) {
    storyInput.focus();
    return;
  }

  findBtn.disabled = true;
  findBtn.innerHTML = '<span class="spinner" aria-hidden="true"></span>Looking…';

  resultsSection.hidden = true;
  noResults.hidden = true;
  resultsContainer.innerHTML = "";

  try {
    const res  = await fetch("/api/match-case", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    const matches = data.matches || [];

    if (matches.length === 0) {
      noResults.hidden = false;
    } else {
      matches.forEach((m) => {
        const card = cardTemplate.content.cloneNode(true);
        if (m.year)     card.querySelector(".result-year").textContent = m.year;
        if (m.location) card.querySelector(".result-location").textContent = m.location;
        card.querySelector(".result-summary").textContent = m.summary;
        card.querySelector(".result-outcome-text").textContent = m.outcome;
        if (m.follow_up) {
          const fq = card.querySelector(".result-followup");
          fq.hidden = false;
          fq.querySelector(".result-followup-text").textContent = m.follow_up;
        }
        resultsContainer.appendChild(card);
      });
      resultsSection.hidden = false;
      resultsSection.querySelector("h2").focus();
    }
  } catch {
    noResults.hidden = false;
  } finally {
    findBtn.disabled = false;
    findBtn.textContent = "Find Similar Stories";
  }
}
