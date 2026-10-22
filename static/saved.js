"use strict";

// Saved chats: stored in this browser (localStorage). Works on top of app.js without changing it.
(function () {
  const KEY = "bhagavatam_saved_chats_v1";
  const MAX_CHATS = 50;
  let currentId = null;     // id of the chat that is open now
  let restoring = false;    // true while an old chat is being re-drawn

  // ------------------------------------------------ storage
  function load() {
    try {
      const data = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(data) ? data : [];
    } catch (e) {
      return [];
    }
  }
  function store(list) {
    try {
      localStorage.setItem(KEY, JSON.stringify(list));
    } catch (e) {
      console.warn("Could not save chats:", e);
    }
  }

  // ------------------------------------------------ read the current chat from the screen
  function collect() {
    const rows = Array.from(chat.children);
    const out = [];
    rows.forEach((row, i) => {
      if (row.classList.contains("user")) {
        const next = rows[i + 1];
        if (next && next._saved && next._saved.mode === "error") return;   // message that failed
        if (typeof row._text === "string") out.push({ role: "user", text: row._text });
      } else if (row._saved && row._saved.mode !== "error") {
        out.push({ role: "bot", result: row._saved });
      }
    });
    return out;
  }

  function makeTitle(items) {
    const first = items.find((i) => i.role === "user");
    const t = first ? first.text.replace(/\s+/g, " ").trim() : "New chat";
    return t.length > 45 ? t.slice(0, 45) + "…" : t;
  }

  function save() {
    const items = collect();
    if (!items.some((i) => i.role === "user")) return;
    const list = load();
    let c = list.find((x) => x.id === currentId);
    if (!c) {
      currentId = "c" + Date.now().toString(36);
      c = { id: currentId, title: makeTitle(items), created: Date.now() };
      list.unshift(c);
    }
    c.items = items;
    c.updated = Date.now();
    store(list.slice(0, MAX_CHATS));
    renderList();
  }

  // ------------------------------------------------ hook into app.js
  const _addUser = addUser;
  addUser = function (text, index) {
    _addUser(text, index);
    const row = chat.lastElementChild;
    if (row) row._text = text;
  };

  const _addBot = addBot;
  addBot = function (result) {
    _addBot(result);
    const row = chat.lastElementChild;
    if (row) row._saved = result;
    if (!restoring) save();
  };

  const _greet = greet;
  greet = function () {
    _greet();
    if (!restoring) currentId = null;   // "New chat" starts a fresh saved chat
    renderList();
  };

  // ------------------------------------------------ open / delete / rename
  function openChat(id) {
    if (busy) {
      alert("Please wait for the reply to finish.");
      return;
    }
    const c = load().find((x) => x.id === id);
    if (!c) return;
    restoring = true;
    try {
      stopSpeaking();
      greet();
      chat.querySelectorAll(".chips").forEach((x) => x.remove());
      currentId = id;
      c.items.forEach((it) => {
        if (it.role === "user") {
          addUser(it.text, history.length);
          history.push({ role: "user", content: it.text });
        } else {
          addBot(it.result);
          if (it.result.mode === "ask" || it.result.mode === "answer") {
            history.push({ role: "assistant", content: it.result.message });
          }
        }
      });
    } finally {
      restoring = false;
    }
    closeDrawer();
    renderList();
  }

  function deleteChat(id) {
    if (!confirm("Delete this saved chat?")) return;
    store(load().filter((x) => x.id !== id));
    if (id === currentId) greet();
    renderList();
  }

  function renameChat(id) {
    const list = load();
    const c = list.find((x) => x.id === id);
    if (!c) return;
    const name = prompt("Rename chat:", c.title);
    if (name && name.trim()) {
      c.title = name.trim().slice(0, 60);
      store(list);
      renderList();
    }
  }

  function clearAll() {
    if (!confirm("Delete ALL saved chats?")) return;
    store([]);
    greet();
    renderList();
  }

  // ------------------------------------------------ panel (drawer)
  const overlay = el("div", "drawer-ov");
  const drawer = el("aside", "drawer");
  drawer.setAttribute("aria-label", "Saved chats");

  const head = el("div", "drawer-head");
  head.appendChild(el("h2", "", "Saved chats"));
  const closeBtn = el("button", "drawer-x", "×");
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close");
  head.appendChild(closeBtn);

  const newBtn = el("button", "drawer-new", "＋ Start a new chat");
  newBtn.type = "button";

  const listEl = el("ul", "hlist");

  const foot = el("div", "drawer-foot");
  foot.appendChild(el("span", "", "Saved in this browser only"));
  const clearBtn = el("button", "", "Clear all");
  clearBtn.type = "button";
  foot.appendChild(clearBtn);

  drawer.appendChild(head);
  drawer.appendChild(newBtn);
  drawer.appendChild(listEl);
  drawer.appendChild(foot);
  document.body.appendChild(overlay);
  document.body.appendChild(drawer);

  function openDrawer() {
    renderList();
    overlay.classList.add("open");
    drawer.classList.add("open");
  }
  function closeDrawer() {
    overlay.classList.remove("open");
    drawer.classList.remove("open");
  }

  function renderList() {
    listEl.innerHTML = "";
    const list = load().sort((a, b) => (b.updated || 0) - (a.updated || 0));
    if (!list.length) {
      listEl.appendChild(el("li", "hempty", "No saved chats yet. Your conversations are saved here automatically."));
      return;
    }
    list.forEach((c) => {
      const li = el("li", "hitem" + (c.id === currentId ? " current" : ""));

      const open = el("button", "hopen");
      open.type = "button";
      open.appendChild(el("b", "", c.title));
      const when = new Date(c.updated || c.created).toLocaleString("en-IN", {
        day: "numeric", month: "short", hour: "2-digit", minute: "2-digit",
      });
      const count = (c.items || []).filter((i) => i.role === "user").length;
      open.appendChild(el("small", "", when + " · " + count + (count === 1 ? " message" : " messages")));
      open.addEventListener("click", () => openChat(c.id));

      const ren = el("button", "hsmall", "✏️");
      ren.type = "button";
      ren.title = "Rename";
      ren.addEventListener("click", () => renameChat(c.id));

      const del = el("button", "hsmall", "🗑️");
      del.type = "button";
      del.title = "Delete";
      del.addEventListener("click", () => deleteChat(c.id));

      li.appendChild(open);
      li.appendChild(ren);
      li.appendChild(del);
      listEl.appendChild(li);
    });
  }

  // History button in the header, next to "New chat"
  const histBtn = el("button", "", "🕘 History");
  histBtn.type = "button";
  histBtn.id = "histBtn";
  const nav = document.querySelector(".hnav");
  if (nav) nav.insertBefore(histBtn, document.getElementById("newChat"));

  histBtn.addEventListener("click", openDrawer);
  closeBtn.addEventListener("click", closeDrawer);
  overlay.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeDrawer(); });
  newBtn.addEventListener("click", () => {
    stopSpeaking();
    greet();
    closeDrawer();
  });
  clearBtn.addEventListener("click", clearAll);

  renderList();
})();