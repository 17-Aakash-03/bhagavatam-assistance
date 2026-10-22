"use strict";

// ---------- animated background (same as the chat page) ----------
(function addBackground() {
  const bg = document.createElement("div");
  bg.className = "bg";
  bg.setAttribute("aria-hidden", "true");

  let petals = "";
  for (let i = 0; i < 12; i++) petals += `<use href="#pet" transform="rotate(${i * 30})"/>`;
  for (let i = 0; i < 12; i++) petals += `<use href="#pet" transform="rotate(${15 + i * 30}) scale(.5)"/>`;

  let sparks = "";
  for (let i = 0; i < 12; i++) {
    const left = 4 + i * 8;
    const size = 4 + (i % 4);
    const dur = 15 + ((i * 7) % 8);
    const delay = (i * 5) % 12;
    sparks += `<i style="left:${left}%; --s:${size}px; --d:${dur}s; --delay:${delay}s"></i>`;
  }

  bg.innerHTML =
    `<div class="stars"></div><div class="stars s2"></div><div class="sunglow"></div>` +
    `<svg class="mandala" viewBox="-300 -300 600 600" xmlns="http://www.w3.org/2000/svg">` +
    `<defs><path id="pet" d="M0 -120 C 30 -170, 30 -230, 0 -280 C -30 -230, -30 -170, 0 -120 Z"/></defs>` +
    `<g fill="none" stroke="#f4bd50" stroke-width="1.6">` +
    `<circle r="292"/><circle r="112"/><circle r="64"/><circle r="30"/>${petals}</g></svg>` +
    `<div class="om-big">ॐ</div>` + sparks;

  document.body.prepend(bg);
})();

// ---------- helpers ----------
function el(tag, className, text) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined) e.textContent = text;
  return e;
}

// read aloud (toggle on the same button)
let currentBtn = null;
function speak(text, lang, btn) {
  if (!("speechSynthesis" in window)) {
    alert("Your browser does not support reading aloud. Try Chrome or Edge.");
    return;
  }
  const same = currentBtn === btn;
  window.speechSynthesis.cancel();
  if (currentBtn) currentBtn.classList.remove("on");
  currentBtn = null;
  if (same) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = lang;
  u.onend = u.onerror = () => {
    btn.classList.remove("on");
    if (currentBtn === btn) currentBtn = null;
  };
  currentBtn = btn;
  btn.classList.add("on");
  window.speechSynthesis.speak(u);
}

// one verse card (used on Home and Verses pages)
function verseCard(v) {
  const card = el("article", "vcard");

  const top = el("div", "vtop");
  top.appendChild(el("span", "vref", v.ref));
  const tags = el("div", "vtags");
  (v.themes || []).forEach((t) => tags.appendChild(el("span", "tag", t)));
  top.appendChild(tags);
  card.appendChild(top);

  if (v.sanskrit) card.appendChild(el("p", "vsans", v.sanskrit));
  if (v.translit) card.appendChild(el("p", "vtrans", v.translit));
  card.appendChild(el("p", "vmean", v.meaning));

  const act = el("div", "vact");

  const en = el("button", "pill", "🔊 English");
  en.type = "button";
  en.addEventListener("click", () => speak(v.ref + ". " + v.meaning, "en-IN", en));
  act.appendChild(en);

  if (v.sanskrit) {
    const sa = el("button", "pill", "🔊 Sanskrit");
    sa.type = "button";
    sa.addEventListener("click", () => speak(v.sanskrit.replace(/॥[^॥]*॥/g, ""), "hi-IN", sa));
    act.appendChild(sa);
  }

  const ask = el("a", "pill", "💬 Ask about this");
  ask.href = "/chat?q=" + encodeURIComponent("What does " + v.ref + " teach? " + v.meaning);
  act.appendChild(ask);

  const web = el("a", "pill", "Vedabase ↗");
  web.href = v.url;
  web.target = "_blank";
  web.rel = "noopener";
  act.appendChild(web);

  card.appendChild(act);
  return card;
}