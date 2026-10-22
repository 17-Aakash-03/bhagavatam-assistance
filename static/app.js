"use strict";

const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const micBtn = document.getElementById("mic");
const langSel = document.getElementById("lang");
const newChatBtn = document.getElementById("newChat");
const demoBanner = document.getElementById("demoBanner");

let history = [];        // [{role, content}] sent to the server
let busy = false;
let lastScene = "";
let sceneCounter = 0;

const STARTERS = [
  "I'm feeling depressed",
  "I need motivation",
  "I feel anxious and stressed",
  "I want peace of mind",
];

// ------------------------------------------------------------ animated pictures
const SKINS = ["#e8b88a", "#c98f62", "#a86f45", "#f1c9a0"];
const CLOTHES = [["#e9822b", "#c96a1a"], ["#4a8fd1", "#35709f"], ["#d9558a", "#b03e6d"], ["#4fa36a", "#38804f"], ["#8a63c9", "#6a4aa3"]];

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function bg(id, top, bottom) {
  return `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">` +
    `<stop offset="0" stop-color="${top}"/><stop offset="1" stop-color="${bottom}"/></linearGradient></defs>` +
    `<rect width="400" height="200" fill="url(#${id})"/>`;
}

// a simple person; (x, y) is where they touch the ground
function person(x, y, s, pose) {
  const skin = pick(SKINS), cl = pick(CLOTHES), c1 = cl[0], c2 = cl[1];
  const hair = `<path d="M-11 -2 Q0 -18 11 -2 Q0 -8 -11 -2Z" fill="#2b1d16"/>`;
  let body = "";
  if (pose === "stand" || pose === "up") {
    const arms = pose === "up"
      ? `<path d="M-13 -60 L-27 -88 M13 -60 L27 -88" stroke="${skin}" stroke-width="7" stroke-linecap="round" fill="none"/>`
      : `<path d="M-13 -60 L-20 -34 M13 -60 L20 -34" stroke="${skin}" stroke-width="7" stroke-linecap="round" fill="none"/>`;
    body = `<path d="M-6 -30 L-8 0 M6 -30 L8 0" stroke="${c2}" stroke-width="8" stroke-linecap="round" fill="none"/>` +
      `<path d="M-13 -62 Q0 -69 13 -62 L11 -26 L-11 -26Z" fill="${c1}"/>` + arms +
      `<circle cx="0" cy="-76" r="10" fill="${skin}"/><g transform="translate(0 -74)">${hair}</g>`;
  } else {
    const hands = pose === "namaste"
      ? `<path d="M-15 -50 Q-24 -32 -2 -33 M15 -50 Q24 -32 2 -33" stroke="${skin}" stroke-width="7" stroke-linecap="round" fill="none"/><circle cx="0" cy="-33" r="4.5" fill="${skin}"/>`
      : `<path d="M-15 -50 Q-30 -30 -19 -13 M15 -50 Q30 -30 19 -13" stroke="${skin}" stroke-width="7" stroke-linecap="round" fill="none"/>`;
    body = `<ellipse cx="0" cy="-6" rx="34" ry="11" fill="${c2}"/>` +
      `<path d="M-15 -52 Q0 -60 15 -52 L21 -12 Q0 -4 -21 -12Z" fill="${c1}"/>` + hands +
      `<circle cx="0" cy="-66" r="11" fill="${skin}"/><g transform="translate(0 -64)">${hair}</g>`;
  }
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="a-breathe">${body}</g></g>`;
}

function bird(y, dur, delay) {
  return `<g class="a-fly" style="animation-duration:${dur}s;animation-delay:${delay}s"><g transform="translate(0 ${y})">` +
    `<path d="M0 0 q5 -7 10 0 q5 -7 10 0" stroke="#4a3a35" fill="none" stroke-width="1.8" stroke-linecap="round"/></g></g>`;
}

function cloud(x, y, s, cls) {
  return `<g class="${cls}"><g transform="translate(${x} ${y}) scale(${s})" fill="#fff" opacity=".88">` +
    `<ellipse cx="0" cy="0" rx="28" ry="9"/><ellipse cx="15" cy="-7" rx="17" ry="10"/><ellipse cx="-15" cy="-5" rx="15" ry="8"/></g></g>`;
}

function waves(y, color, speed, amp) {
  let d = `M-60 ${y}`;
  for (let x = -60; x < 480; x += 50) d += ` q25 ${-amp} 50 0`;
  return `<g class="a-wave" style="animation-duration:${speed}s"><path d="${d}" fill="none" stroke="${color}" stroke-width="3" stroke-linecap="round"/></g>`;
}

function rays(cx, cy, r1, r2, n, color) {
  let out = "";
  for (let i = 0; i < n; i++) {
    const a = (i * 2 * Math.PI) / n;
    out += `<line x1="${(cx + Math.cos(a) * r1).toFixed(1)}" y1="${(cy + Math.sin(a) * r1).toFixed(1)}" x2="${(cx + Math.cos(a) * r2).toFixed(1)}" y2="${(cy + Math.sin(a) * r2).toFixed(1)}"/>`;
  }
  return `<g class="a-spin" stroke="${color}" stroke-width="4" stroke-linecap="round">${out}</g>`;
}

const SCENES = {
  sunrise: (u) => bg(u, "#ffe3b8", "#ffb08a") +
    `<g class="a-glow">${rays(270, 120, 48, 70, 14, "#ffd45e")}</g><circle cx="270" cy="120" r="38" fill="#ffd45e"/>` +
    cloud(90, 40, 1.1, "a-drift") + cloud(320, 55, .8, "a-drift2") + bird(60, 16, 0) + bird(85, 20, 6) +
    `<path d="M0 200 L0 150 Q90 118 180 150 T340 145 T400 140 L400 200Z" fill="#c9733a"/>` +
    `<path d="M0 200 L0 172 Q100 150 200 176 T400 166 L400 200Z" fill="#8f7a3a"/>` +
    person(110, 176, .95, "stand"),

  lotus: (u) => bg(u, "#dff1ff", "#fde4ef") +
    cloud(80, 38, 1, "a-drift") + cloud(330, 50, .8, "a-drift2") + bird(70, 18, 2) +
    `<rect y="120" width="400" height="80" fill="#8cc5d9"/>` + waves(135, "#bfe3f7", 7, 4) + waves(170, "#a9d6ea", 9, 4) +
    `<g class="a-bob"><ellipse cx="90" cy="150" rx="42" ry="8" fill="#4f9d6a"/></g><g class="a-bob" style="animation-delay:1s"><ellipse cx="320" cy="165" rx="48" ry="9" fill="#4f9d6a"/></g>` +
    `<g class="a-ripple"><ellipse cx="200" cy="170" rx="90" ry="14" fill="none" stroke="#fff" stroke-width="2"/></g>` +
    `<g class="a-ripple" style="animation-delay:2s"><ellipse cx="200" cy="170" rx="90" ry="14" fill="none" stroke="#fff" stroke-width="2"/></g>` +
    person(200, 168, 1, "sit") +
    [-62, -31, 31, 62].map((a) => `<ellipse cx="200" cy="146" rx="13" ry="30" fill="#f6a5c0" transform="rotate(${a} 200 172)"/>`).join("") +
    `<ellipse cx="200" cy="170" rx="46" ry="7" fill="#ff8fb3"/>`,

  river: (u) => bg(u, "#cfe8f7", "#eaf6ef") +
    `<path d="M0 125 L70 75 L130 112 L200 62 L280 118 L340 82 L400 118 L400 150 L0 150Z" fill="#a9c5b5"/>` +
    cloud(110, 38, 1, "a-drift") + cloud(310, 45, .8, "a-drift2") + bird(60, 15, 0) + bird(84, 19, 5) +
    `<rect y="150" width="400" height="50" fill="#5aa7d1"/>` + waves(162, "#d6efff", 5, 5) + waves(180, "#a6d4ee", 7, 5) + waves(195, "#d6efff", 6, 4) +
    `<path d="M0 150 L0 130 Q90 120 170 138 T300 140 T400 132 L400 152 Q200 140 0 152Z" fill="#5e9a68"/>` +
    `<g class="a-sway"><g stroke="#4b8a5a" stroke-width="3" stroke-linecap="round"><line x1="320" y1="150" x2="326" y2="112"/><line x1="332" y1="150" x2="330" y2="108"/><line x1="344" y1="150" x2="350" y2="114"/></g></g>` +
    person(110, 140, .95, "sit"),

  mountain: (u) => bg(u, "#bfe0ff", "#fff1d6") +
    `<g class="a-glow"><circle cx="60" cy="48" r="34" fill="#ffd96b" opacity=".35"/></g><circle cx="60" cy="48" r="20" fill="#ffd96b"/>` +
    cloud(150, 36, 1.1, "a-drift") + cloud(330, 60, .9, "a-drift2") + bird(55, 17, 1) +
    `<path d="M20 200 L150 62 L290 200Z" fill="#7a8fb0"/><path d="M130 200 L270 40 L420 200Z" fill="#5f7599"/>` +
    `<path d="M270 40 L246 72 L264 66 L274 78 L290 64Z" fill="#fff"/>` +
    `<path d="M0 200 L0 176 Q100 156 200 180 T400 174 L400 200Z" fill="#5e9a68"/>` +
    person(268, 48, .4, "up") + person(95, 182, .85, "stand"),

  lamp: (u) => bg(u, "#2f1b14", "#6e3b1e") +
    [[40, 30], [110, 55], [330, 35], [370, 90], [60, 100]].map((p, i) => `<circle class="a-twinkle" style="animation-delay:${i * .6}s" cx="${p[0]}" cy="${p[1]}" r="2" fill="#ffe9a8"/>`).join("") +
    `<g class="a-glow"><circle cx="270" cy="130" r="80" fill="#ffb347" opacity=".2"/><circle cx="270" cy="130" r="48" fill="#ffb347" opacity=".25"/></g>` +
    `<path d="M0 200 L0 176 Q200 168 400 176 L400 200Z" fill="#4a2a18"/>` +
    person(120, 182, 1.05, "namaste") +
    `<path d="M230 142 Q270 186 310 142Z" fill="#c8742e"/><ellipse cx="270" cy="142" rx="40" ry="6" fill="#e08c3b"/>` +
    `<g class="a-flicker"><path d="M270 98 C288 120 288 142 270 146 C252 142 252 120 270 98Z" fill="#ffcf5a"/><path d="M270 118 C278 130 278 140 270 143 C262 140 262 130 270 118Z" fill="#fff2b0"/></g>` +
    `<g class="a-bob"><circle cx="300" cy="85" r="2" fill="#ffd77a"/></g><g class="a-bob" style="animation-delay:1.2s"><circle cx="245" cy="75" r="1.6" fill="#ffd77a"/></g>`,

  moon: (u) => bg(u, "#16213e", "#3a4a7a") +
    [[40, 30], [90, 70], [150, 25], [260, 40], [330, 80], [360, 25], [60, 115], [300, 110], [210, 20], [380, 140]].map((p, i) => `<circle class="a-twinkle" style="animation-delay:${(i % 5) * .5}s" cx="${p[0]}" cy="${p[1]}" r="2" fill="#fff6d6"/>`).join("") +
    `<g class="a-glow"><circle cx="290" cy="62" r="52" fill="#fff3c4" opacity=".18"/></g><circle cx="290" cy="62" r="32" fill="#fff3c4"/><circle cx="304" cy="55" r="28" fill="#25335c"/>` +
    `<path d="M0 200 L0 160 Q100 132 200 160 T400 150 L400 200Z" fill="#1d2a4d"/>` +
    person(160, 168, 1, "sit") +
    `<g class="a-bob"><circle cx="70" cy="140" r="2.4" fill="#e8ff8a"/></g><g class="a-bob" style="animation-delay:1s"><circle cx="250" cy="150" r="2.4" fill="#e8ff8a"/></g><g class="a-bob" style="animation-delay:2s"><circle cx="330" cy="135" r="2.4" fill="#e8ff8a"/></g>`,

  tree: (u) => bg(u, "#d9f0d0", "#f7f3d6") +
    `<g class="a-glow"><circle cx="50" cy="42" r="32" fill="#ffd96b" opacity=".35"/></g><circle cx="50" cy="42" r="18" fill="#ffd96b"/>` +
    cloud(180, 36, 1, "a-drift") + bird(70, 16, 0) +
    `<ellipse cx="200" cy="190" rx="220" ry="26" fill="#7bbf7f"/>` +
    `<rect x="270" y="96" width="22" height="90" rx="6" fill="#8a5a2b"/>` +
    `<g class="a-sway"><circle cx="281" cy="76" r="50" fill="#4f9d5a"/><circle cx="244" cy="98" r="34" fill="#5fb06a"/><circle cx="318" cy="98" r="34" fill="#5fb06a"/></g>` +
    person(150, 184, 1, "sit") +
    `<g class="a-drift2"><g class="a-bob"><ellipse cx="205" cy="120" rx="6" ry="4" fill="#ff9b3d"/><ellipse cx="212" cy="120" rx="6" ry="4" fill="#ffb86b"/></g></g>`,

  ocean: (u) => bg(u, "#ffd9a8", "#9fcdea") +
    `<g class="a-glow"><circle cx="270" cy="100" r="60" fill="#fff0a8" opacity=".3"/></g><circle cx="270" cy="100" r="34" fill="#ffe27a"/>` +
    cloud(90, 40, 1, "a-drift") + bird(50, 14, 0) + bird(70, 18, 4) +
    `<rect y="100" width="400" height="100" fill="#5da6d6"/>` + waves(116, "#bfe3f7", 6, 4) + waves(140, "#a6d4ee", 8, 5) + waves(164, "#8fc4e6", 5, 5) +
    `<path d="M0 200 L0 170 Q120 158 240 176 T400 172 L400 200Z" fill="#f0d9a0"/>` +
    person(90, 180, .95, "stand"),
};

const SCENE_POOL = {
  sunrise: ["sunrise", "tree", "ocean"],
  lotus: ["lotus", "moon", "tree"],
  river: ["river", "ocean", "mountain"],
  mountain: ["mountain", "sunrise", "tree"],
  lamp: ["lamp", "moon", "lotus"],
};

function sceneFor(theme) {
  const pool = SCENE_POOL[theme] || Object.keys(SCENES);
  let options = pool.filter((n) => n !== lastScene);
  if (!options.length) options = pool;
  const name = options[Math.floor(Math.random() * options.length)];
  lastScene = name;
  sceneCounter += 1;
  const svg = `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${name} picture">` +
    SCENES[name]("g" + sceneCounter) + `</svg>`;
  const div = document.createElement("div");
  div.className = "scene";
  div.innerHTML = svg;
  return div;
}

// ------------------------------------------------------------ helpers
function el(tag, className, text) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined) e.textContent = text;
  return e;
}

function scrollDown() {
  chat.scrollTop = chat.scrollHeight;
}

function addUser(text, index) {
  const row = el("div", "msg user");
  row.dataset.index = String(index);
  const col = el("div", "ucol");
  row.appendChild(col);
  showUserBubble(row, col, text, index);
  chat.appendChild(row);
  scrollDown();
}

function showUserBubble(row, col, text, index) {
  col.innerHTML = "";
  col.appendChild(el("div", "bubble", text));
  const edit = el("button", "edit-btn", "✏️ Edit");
  edit.type = "button";
  edit.addEventListener("click", () => startEdit(row, col, text, index));
  col.appendChild(edit);
}

function startEdit(row, col, text, index) {
  if (busy) return;
  col.innerHTML = "";
  const box = el("textarea", "edit-box");
  box.value = text;
  box.rows = 2;
  col.appendChild(box);
  const bar = el("div", "edit-bar");
  const save = el("button", "chip", "Save and send");
  save.type = "button";
  const cancel = el("button", "chip", "Cancel");
  cancel.type = "button";
  bar.appendChild(save);
  bar.appendChild(cancel);
  col.appendChild(bar);
  box.focus();
  cancel.addEventListener("click", () => showUserBubble(row, col, text, index));
  save.addEventListener("click", () => {
    const newText = box.value.trim();
    if (!newText) return;
    stopSpeaking();
    // remove this message and everything after it, then ask again from here
    let node = row;
    while (node) {
      const next = node.nextSibling;
      node.remove();
      node = next;
    }
    history = history.slice(0, index);
    send(newText);
  });
}

function addTyping() {
  const row = el("div", "msg bot typing-row");
  row.appendChild(el("div", "bubble typing", "Thinking..."));
  chat.appendChild(row);
  scrollDown();
  return row;
}

function removeOldRegenButtons() {
  chat.querySelectorAll(".regen").forEach((b) => b.remove());
}

// ------------------------------------------------------------ speech (Listen)
let speaking = null;

function stopSpeaking() {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  if (speaking) speaking.classList.remove("on");
  speaking = null;
}

function listen(text, button) {
  if (!("speechSynthesis" in window)) {
    alert("Your browser does not support reading aloud.");
    return;
  }
  const wasThis = speaking === button;
  stopSpeaking();
  if (wasThis) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = langSel.value;
  u.onend = u.onerror = () => {
    button.classList.remove("on");
    if (speaking === button) speaking = null;
  };
  speaking = button;
  button.classList.add("on");
  window.speechSynthesis.speak(u);
}

// ------------------------------------------------------------ rendering a bot reply
function addBot(result) {
  removeOldRegenButtons();
  const row = el("div", "msg bot");
  const bubble = el("div", "bubble");
  if (result.mode === "crisis") bubble.classList.add("crisis");
  if (result.mode === "error") bubble.classList.add("error");

  String(result.message || "").split(/\n+/).forEach((para) => {
    if (para.trim()) bubble.appendChild(el("p", "", para.trim()));
  });

  const spoken = [result.message || ""];

  if (Array.isArray(result.steps) && result.steps.length) {
    bubble.appendChild(el("h4", "", "Small steps for today"));
    const ol = el("ol");
    result.steps.forEach((s) => {
      ol.appendChild(el("li", "", s));
      spoken.push(s);
    });
    bubble.appendChild(ol);
  }

  if (Array.isArray(result.verses)) {
    result.verses.forEach((v) => {
      const box = el("div", "verse");
      box.appendChild(el("div", "ref", v.ref));
      if (v.sanskrit) box.appendChild(el("div", "sanskrit", v.sanskrit));
      if (v.translit) box.appendChild(el("div", "translit", v.translit));
      box.appendChild(el("div", "meaning", v.meaning));
      if (v.context) box.appendChild(el("div", "context", "Context: " + v.context));
      const a = el("a", "", "Read the full verse and purport on Vedabase");
      a.href = v.url;
      a.target = "_blank";
      a.rel = "noopener";
      box.appendChild(a);
      bubble.appendChild(box);
    });
  }

  if (result.mode === "answer" && result.image_theme) {
    bubble.appendChild(sceneFor(result.image_theme));
  }

  const actions = el("div", "actions");
  const listenBtn = el("button", "", "🔊 Listen");
  listenBtn.type = "button";
  listenBtn.addEventListener("click", () => listen(spoken.join(". "), listenBtn));
  actions.appendChild(listenBtn);

  if (result.mode === "ask" || result.mode === "answer") {
    const regen = el("button", "regen", "🔄 Regenerate");
    regen.type = "button";
    regen.addEventListener("click", () => regenerate(row));
    actions.appendChild(regen);
  }
  bubble.appendChild(actions);

  row.appendChild(bubble);
  chat.appendChild(row);
  scrollDown();
  if (result.demo) demoBanner.hidden = false;
}

// ------------------------------------------------------------ talking to the server
async function ask(regen) {
  busy = true;
  sendBtn.disabled = true;
  const typing = addTyping();
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history, regen: !!regen }),
    });
    const result = await res.json();
    typing.remove();
    addBot(result);
    if (result.mode === "ask" || result.mode === "answer") {
      history.push({ role: "assistant", content: result.message });
    } else {
      // error or crisis: do not keep it in the conversation memory
      if (result.mode === "error") history.pop();
    }
  } catch (err) {
    typing.remove();
    addBot({ mode: "error", message: "Sorry, I could not reach the app server. Please check that it is running." });
    history.pop();
  } finally {
    busy = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

function send(text) {
  text = (text || "").trim();
  if (!text || busy) return;
  stopSpeaking();
  chat.querySelectorAll(".chips").forEach((c) => c.remove());
  removeOldRegenButtons();
  addUser(text, history.length);
  history.push({ role: "user", content: text });
  input.value = "";
  input.style.height = "auto";
  ask(false);
}

function regenerate(row) {
  if (busy) return;
  stopSpeaking();
  // forget the last assistant reply and ask again for the same user message
  if (history.length && history[history.length - 1].role === "assistant") history.pop();
  row.remove();
  ask(true);
}

// ------------------------------------------------------------ greeting and new chat
function greet() {
  chat.innerHTML = "";
  history = [];
  lastScene = "";
  const row = el("div", "msg bot");
  const bubble = el("div", "bubble");
  bubble.appendChild(el("p", "",
    "Namaste 🙏 Tell me what is on your heart, or ask me anything, such as \"What is motivation?\" " +
    "I will ask a few gentle questions, then share guidance with verses from the Śrīmad-Bhāgavatam."));
  const chips = el("div", "chips");
  STARTERS.forEach((t) => {
    const c = el("button", "chip", t);
    c.type = "button";
    c.addEventListener("click", () => send(t));
    chips.appendChild(c);
  });
  bubble.appendChild(chips);
  row.appendChild(bubble);
  chat.appendChild(row);
}

newChatBtn.addEventListener("click", () => {
  stopSpeaking();
  greet();
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  send(input.value);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send(input.value);
  }
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 120) + "px";
});

// ------------------------------------------------------------ voice typing
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let listening = false;

if (!SR) {
  micBtn.disabled = true;
  micBtn.title = "Voice typing is not supported in this browser (try Chrome or Edge)";
} else {
  micBtn.addEventListener("click", () => {
    if (listening && recognition) {
      recognition.stop();
      return;
    }
    recognition = new SR();
    recognition.lang = langSel.value;
    recognition.interimResults = false;
    recognition.onstart = () => {
      listening = true;
      micBtn.classList.add("on");
    };
    recognition.onend = () => {
      listening = false;
      micBtn.classList.remove("on");
    };
    recognition.onerror = () => {
      listening = false;
      micBtn.classList.remove("on");
    };
    recognition.onresult = (e) => {
      const said = Array.from(e.results).map((r) => r[0].transcript).join(" ");
      input.value = (input.value ? input.value + " " : "") + said;
      input.dispatchEvent(new Event("input"));
    };
    recognition.start();
  });
}

greet();

// ------------------------------------------------------------ open from Home / Verses page with a ready question: /chat?q=...
const startQuestion = new URLSearchParams(window.location.search).get("q");
if (startQuestion) {
  window.history.replaceState(null, "", "/chat");
  setTimeout(() => send(startQuestion), 300);
}