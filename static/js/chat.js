/* ── Pillar 3: AI Legal Companion (Lex) ──────────────────────────── */

const form       = document.getElementById("chat-form");
const input      = document.getElementById("chat-input");
const messages   = document.getElementById("chat-messages");
const clearBtn   = document.getElementById("clear-chat-btn");
const sendBtn    = form?.querySelector(".send-btn");

let history = []; // [{role, content}]

// ── Auto-resize textarea ──────────────────────────────────────────
input?.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 120) + "px";
});

// ── Starter prompts ───────────────────────────────────────────────
document.querySelectorAll(".starter").forEach(btn => {
  btn.addEventListener("click", () => {
    if (input) {
      input.value = btn.textContent;
      input.dispatchEvent(new Event("input"));
      sendMessage();
    }
  });
});

// ── Clear chat ────────────────────────────────────────────────────
clearBtn?.addEventListener("click", () => {
  const kept = document.getElementById("welcome-msg");
  messages.innerHTML = "";
  if (kept) messages.appendChild(kept);
  history = [];
});

// ── Form submit ───────────────────────────────────────────────────
form?.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

input?.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── Send message ──────────────────────────────────────────────────
async function sendMessage() {
  const text = input?.value.trim();
  if (!text) return;

  // Append user bubble
  appendMessage("user", text);
  history.push({ role: "user", content: text });
  input.value = "";
  input.style.height = "auto";
  if (sendBtn) sendBtn.disabled = true;

  // Show typing indicator
  const typingId = appendTyping();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: history.slice(-10) }),
    });

    if (!res.ok) {
      const err = await res.json();
      removeTyping(typingId);
      appendMessage("lex", `⚠️ ${err.error || "Something went wrong. Please try again."}`);
      return;
    }

    // Stream the response via SSE
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    removeTyping(typingId);
    const lexBubble = appendMessage("lex", "", true); // empty, streaming
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      for (const line of chunk.split("\n")) {
        if (!line.startsWith("data: ")) continue;
        const payload = line.slice(6).trim();
        if (payload === "[DONE]") break;
        try {
          const { chunk: text } = JSON.parse(payload);
          fullText += text;
          lexBubble.innerHTML = formatMessage(fullText);
        } catch {}
      }
    }
    history.push({ role: "assistant", content: fullText });

  } catch (err) {
    removeTyping(typingId);
    appendMessage("lex", "⚠️ Connection error. Please check your internet and try again.");
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    input?.focus();
    scrollToBottom();
  }
}

// ── DOM helpers ───────────────────────────────────────────────────
function appendMessage(role, content, streaming = false) {
  const div = document.createElement("div");
  div.className = `msg msg-${role === "user" ? "user" : "lex"}`;

  if (role === "lex") {
    div.innerHTML = `
      <span class="msg-avatar" aria-hidden="true">🤖</span>
      <div class="msg-bubble">${streaming ? "" : formatMessage(content)}</div>`;
  } else {
    div.innerHTML = `<div class="msg-bubble">${escapeHtml(content)}</div>`;
  }

  messages.appendChild(div);
  scrollToBottom();
  return role === "lex" ? div.querySelector(".msg-bubble") : null;
}

function appendTyping() {
  const id = "typing-" + Date.now();
  const div = document.createElement("div");
  div.className = "msg msg-lex msg-typing";
  div.id = id;
  div.innerHTML = `
    <span class="msg-avatar" aria-hidden="true">🤖</span>
    <div class="msg-bubble">
      <div class="typing-dots" aria-label="Lex is typing">
        <span></span><span></span><span></span>
      </div>
    </div>`;
  messages.appendChild(div);
  scrollToBottom();
  return id;
}

function removeTyping(id) {
  document.getElementById(id)?.remove();
}

function scrollToBottom() {
  messages.scrollTop = messages.scrollHeight;
}

// ── Text formatters ───────────────────────────────────────────────
function escapeHtml(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function formatMessage(text) {
  // Convert markdown-lite to HTML
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p>").replace(/$/, "</p>")
    // Linkify phone numbers
    .replace(/(\d{1}-\d{3}-\d{3}-\d{4}|\d{3}-\d{3}-\d{4})/g,
      '<a href="tel:$1">$1</a>');
}
