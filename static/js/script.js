/**
 * script.js — Sentimate Chat Interface
 * Handles: message sending, bot responses, typing indicator,
 *          TTS, voice input, language switching, auto-resize input,
 *          character counter, history loading.
 *
 * API endpoints (Flask):
 *   POST /get_response    { message }  → { response, language }
 *   GET  /get_history                  → { history }
 *   POST /speak_response  { text, language } → { audio_b64 }
 *   POST /save_language   { language } → { success }
 *   GET  /get_language                 → { language }
 */

/* ================================================================
   § 1  DOM REFERENCES
   ================================================================ */
const chatMessages   = document.getElementById('chat-messages');
const msgInput       = document.getElementById('msg-input');
const sendBtn        = document.getElementById('send-btn');
const micBtn         = document.getElementById('mic-btn');
const langSelect     = document.getElementById('lang-select');
const clearBtn       = document.getElementById('clear-btn');
const voiceBar       = document.getElementById('voice-bar');
const voiceBarText   = document.getElementById('voice-bar-text');
const charCounter    = document.getElementById('char-counter');
const toast          = document.getElementById('toast');

/* ================================================================
   § 2  STATE
   ================================================================ */
const MAX_CHARS    = 1000;  // Hard cap (mirrors Flask config)
let currentLang    = 'english';
let isRecording    = false;
let recognition    = null;
let hasMessages    = false;  // Track whether the welcome state is shown

/* ================================================================
   § 3  HELPERS — Toast notification
   ================================================================ */

/** Show a brief toast at bottom-right of screen. */
function showToast(msg, durationMs = 3000) {
  if (!toast) return;
  toast.querySelector('.toast-text').textContent = msg;
  toast.classList.remove('hidden');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.add('hidden'), durationMs);
}

/* ================================================================
   § 4  HELPERS — Time formatting
   ================================================================ */

/** Return a friendly time string like "2:34 PM". */
function timeNow() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/* ================================================================
   § 5  REMOVE WELCOME STATE
   ================================================================ */

/** Remove the empty-state welcome card the first time a message appears. */
function removeWelcomeState() {
  if (hasMessages) return;
  const emptyEl = chatMessages.querySelector('.empty-state');
  if (emptyEl) {
    emptyEl.style.transition = 'opacity .3s ease, transform .3s ease';
    emptyEl.style.opacity    = '0';
    emptyEl.style.transform  = 'scale(.95)';
    setTimeout(() => emptyEl.remove(), 300);
  }
  hasMessages = true;
}

/* ================================================================
   § 6  APPEND MESSAGE
   ================================================================ */

/**
 * Render a chat bubble.
 * @param {string} text       - Message content (plain-text or simple markdown)
 * @param {'user'|'bot'} role - Who sent it
 * @param {boolean} animate   - Whether to slide in (false for history replay)
 * @param {string}  timeStr   - Timestamp label
 */
function appendMessage(text, role, animate = true, timeStr = timeNow()) {
  removeWelcomeState();

  const row = document.createElement('div');
  row.className = `message ${role}${animate ? '' : ' no-anim'}`;

  // Avatar emoji
  const avatarIcon = role === 'user' ? '🧑' : '💜';
  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = avatarIcon;
  avatar.setAttribute('aria-hidden', 'true');

  // Bubble group
  const group = document.createElement('div');
  group.className = 'msg-group';

  // Bubble
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  // Preserve line-breaks; escape HTML to prevent XSS
  bubble.innerHTML = escapeHtml(text).replace(/\n/g, '<br>');

  // Timestamp
  const time = document.createElement('div');
  time.className = 'msg-time';
  time.setAttribute('aria-label', `Sent at ${timeStr}`);
  time.textContent = timeStr;

  group.appendChild(bubble);
  group.appendChild(time);
  row.appendChild(avatar);
  row.appendChild(group);
  chatMessages.appendChild(row);

  // Smooth scroll to latest message
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });

  return row;
}

/** Minimal HTML escaping to guard against XSS */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* ================================================================
   § 7  TYPING INDICATOR
   ================================================================ */
let typingEl = null;

function showTyping() {
  if (typingEl) return;   // Already visible
  removeWelcomeState();

  typingEl = document.createElement('div');
  typingEl.className = 'message bot typing-indicator';
  typingEl.setAttribute('aria-label', 'Sentimate is typing');
  typingEl.innerHTML = `
    <div class="msg-avatar" aria-hidden="true">💜</div>
    <div class="msg-group">
      <div class="bubble">
        <span class="typing-label">Sentimate is typing</span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>`;
  chatMessages.appendChild(typingEl);
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function hideTyping() {
  if (typingEl) { typingEl.remove(); typingEl = null; }
}

/* ================================================================
   § 8  AUTO-RESIZE TEXTAREA + CHARACTER COUNTER
   ================================================================ */

function resizeInput() {
  if (!msgInput) return;
  msgInput.style.height = 'auto';
  msgInput.style.height = Math.min(msgInput.scrollHeight, 140) + 'px';

  const len = msgInput.value.length;
  if (charCounter) {
    charCounter.textContent = `${len} / ${MAX_CHARS}`;
    charCounter.classList.toggle('warn',  len > MAX_CHARS * 0.85);
    charCounter.classList.toggle('error', len > MAX_CHARS);
  }
}

/* ================================================================
   § 9  SEND MESSAGE
   ================================================================ */

async function sendMessage() {
  const text = msgInput.value.trim();
  if (!text || text.length > MAX_CHARS) return;

  // Show user bubble, clear input
  appendMessage(text, 'user');
  msgInput.value = '';
  resizeInput();
  setSendDisabled(true);
  showTyping();

  try {
    const res = await fetch('/get_response', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ message: text }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.response || `HTTP ${res.status}`);
    }

    const data = await res.json();
    hideTyping();

    const botText = data.response || '…';
    appendMessage(botText, 'bot');

    // Auto-TTS if language preference is set
    if (data.language && data.language !== 'english') {
      currentLang = data.language;
    }

  } catch (err) {
    hideTyping();
    console.error('Chat error:', err);
    appendMessage('Sorry, something went wrong. Please try again. 💙', 'bot');
    showToast('Connection issue. Please try again.');
  } finally {
    setSendDisabled(false);
    msgInput.focus();
  }
}

function setSendDisabled(disabled) {
  if (sendBtn) sendBtn.disabled = disabled;
}

/* ================================================================
   § 10  VOICE INPUT (Web Speech API)
   ================================================================ */

function initVoice() {
  if (!micBtn) return;

  // Check browser support
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    micBtn.disabled = true;
    micBtn.title    = 'Voice input not supported in this browser';
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous    = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    isRecording = true;
    micBtn.classList.add('recording');
    micBtn.title = 'Listening… click to stop';
    setVoiceBar('🎙️ Listening…');
  };

  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    if (msgInput) {
      msgInput.value = transcript;
      resizeInput();
    }
  };

  recognition.onerror = (e) => {
    console.warn('Voice error:', e.error);
    showToast('Voice input failed. Please try again.');
    stopRecording();
  };

  recognition.onend = () => stopRecording();

  micBtn.addEventListener('click', () => {
    if (isRecording) {
      recognition.stop();
    } else {
      recognition.lang = currentLang === 'tamil' ? 'ta-IN' : 'en-US';
      recognition.start();
    }
  });
}

function stopRecording() {
  isRecording = false;
  if (micBtn) {
    micBtn.classList.remove('recording');
    micBtn.title = 'Voice input';
  }
  hideVoiceBar();
}

function setVoiceBar(text) {
  if (!voiceBar) return;
  if (voiceBarText) voiceBarText.textContent = text;
  voiceBar.classList.add('visible');
}

function hideVoiceBar() {
  if (voiceBar) voiceBar.classList.remove('visible');
}

/* ================================================================
   § 11  LANGUAGE PREFERENCE
   ================================================================ */

async function loadLanguage() {
  try {
    const res  = await fetch('/get_language');
    const data = await res.json();
    currentLang = data.language || 'english';
    if (langSelect) langSelect.value = currentLang;
  } catch (_) { /* non-critical */ }
}

async function saveLanguage(lang) {
  try {
    await fetch('/save_language', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ language: lang }),
    });
    currentLang = lang;
    showToast(`Language set to ${lang} 🌐`);
  } catch (_) {
    showToast('Could not save language preference.');
  }
}

/* ================================================================
   § 12  CLEAR CHAT (UI only)
   ================================================================ */

function clearChat() {
  if (!chatMessages) return;
  chatMessages.innerHTML = '';
  hasMessages = false;
  insertWelcomeState();
}

function insertWelcomeState() {
  chatMessages.innerHTML = `
    <div class="empty-state" aria-label="Welcome to Sentimate">
      <div class="empty-icon">💙</div>
      <h3>Hi there, I'm Sentimate</h3>
      <p>Your warm AI companion — here to listen, chat, and brighten your day. What's on your mind?</p>
      <div class="suggestions" role="list" aria-label="Conversation starters">
        <button class="chip" role="listitem">How are you today?</button>
        <button class="chip" role="listitem">Tell me something uplifting 😊</button>
        <button class="chip" role="listitem">I feel a bit lonely</button>
        <button class="chip" role="listitem">Let's play a word game!</button>
      </div>
    </div>`;
  // Re-attach chip click handlers
  attachChipHandlers();
}

/* ================================================================
   § 13  SUGGESTION CHIPS
   ================================================================ */

function attachChipHandlers() {
  chatMessages.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if (msgInput) msgInput.value = chip.textContent.replace(/[\u{1F600}-\u{1F6FF}]/gu, '').trim();
      sendMessage();
    });
  });
}

/* ================================================================
   § 14  LOAD CHAT HISTORY
   ================================================================ */

async function loadChatHistory() {
  try {
    const res  = await fetch('/get_history?limit=40');
    if (!res.ok) return;
    const data = await res.json();
    const hist = data.history || [];

    if (hist.length === 0) return;   // Show welcome state

    // Remove welcome placeholder, replay history silently
    const emptyEl = chatMessages.querySelector('.empty-state');
    if (emptyEl) emptyEl.remove();
    hasMessages = true;

    hist.forEach(item => {
      // History items: { role: 'user'|'bot', message, timestamp }
      const role = item.role === 'user' ? 'user' : 'bot';
      const ts   = item.timestamp
        ? new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        : '';
      appendMessage(item.message, role, false, ts);
    });

  } catch (err) {
    console.warn('Could not load history:', err);
  }
}

/* ================================================================
   § 15  EVENT LISTENERS
   ================================================================ */

/** Send on Enter (Shift+Enter = new line) */
function onInputKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function bindEvents() {
  if (msgInput) {
    msgInput.addEventListener('input',   resizeInput);
    msgInput.addEventListener('keydown', onInputKeydown);
  }

  if (sendBtn)   sendBtn.addEventListener('click',  sendMessage);

  if (langSelect) {
    langSelect.addEventListener('change', () => saveLanguage(langSelect.value));
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (confirm('Clear chat history from view?')) clearChat();
    });
  }
}

/* ================================================================
   § 16  INIT
   ================================================================ */

async function init() {
  bindEvents();
  initVoice();
  await loadLanguage();
  await loadChatHistory();

  // Focus the input after load
  if (msgInput) setTimeout(() => msgInput.focus(), 400);
}

// Kick off when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
