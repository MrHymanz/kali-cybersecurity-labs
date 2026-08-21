const translations = {
  en: {
    brandSubtitle: "Guided cybersecurity practice", dashboard: "Dashboard", lessons: "Lessons", notes: "Notes",
    scopeTitle: "Lab scope active", scopeWarning: "Only explicitly permitted lab targets may be tested.", workspace: "LEARNING WORKSPACE",
    language: "Language", beginnerPath: "BEGINNER PATH", heroTitle: "Learn security by observing first.",
    heroBody: "Work through small, legal exercises. Every action is scoped, explained, and reviewable.", continueLesson: "Start lesson",
    progress: "Progress", permittedTarget: "Permitted target", safetyMode: "Safety mode", allowlisted: "Allowlisted",
    noFreeShell: "No unrestricted shell execution", currentModule: "CURRENT MODULE", availableLessons: "Available lessons",
    guidedLearning: "GUIDED LEARNING", lessonLibrary: "Lesson library", openLesson: "Open lesson", completed: "Completed", notStarted: "Not started",
    backToLessons: "Back to lessons", guidedLesson: "GUIDED LESSON", safeLabAction: "SAFE LAB ACTION",
    actionExplanation: "Request only the response headers from the explicitly permitted Juice Shop target.", runAction: "Run safe action",
    running: "Running…", result: "Result", yourTurn: "Your turn", interpretPrompt: "What can you conclude from this output, and what remains uncertain?",
    markComplete: "Mark this lesson complete", privateNotes: "PRIVATE NOTES", observations: "Your observations",
    notesPrivate: "Saved only on this computer and never added to Git.", notesPlaceholder: "Record facts, hypotheses, and questions...",
    saveNotes: "Save notes", saved: "Saved", notesHeading: "Private learning notes",
    notesIntro: "Open a lesson to record observations. Notes stay in .local/ and are excluded from Git.", openLessons: "Open lessons",
    speechOn: "Speech ready", speechOff: "Speech off", requestFailed: "Request failed", lessonComplete: "Lesson progress updated",
    speechSetupLabel: "SPEECH", speechSetupTitle: "Listen to lesson explanations", speechSetupBody: "Install the local Piper voice for your selected lesson language. The voice stays on this computer.",
    enableSpeech: "Enable speech", installingSpeech: "Installing voice…", speechEnabled: "Speech enabled"
  },
  nl: {
    brandSubtitle: "Begeleide cybersecuritytraining", dashboard: "Dashboard", lessons: "Lessen", notes: "Notities",
    scopeTitle: "Labscope actief", scopeWarning: "Test alleen expliciet toegestane labtargets.", workspace: "LEEROMGEVING",
    language: "Taal", beginnerPath: "BEGINNERSTRAJECT", heroTitle: "Leer security door eerst te observeren.",
    heroBody: "Werk met kleine, legale oefeningen. Iedere actie heeft een duidelijke scope, uitleg en controleerbaar resultaat.", continueLesson: "Start de les",
    progress: "Voortgang", permittedTarget: "Toegestaan target", safetyMode: "Veiligheidsmodus", allowlisted: "Toegestane acties",
    noFreeShell: "Geen onbeperkte shell-uitvoering", currentModule: "HUIDIGE MODULE", availableLessons: "Beschikbare lessen",
    guidedLearning: "BEGELEID LEREN", lessonLibrary: "Lesbibliotheek", openLesson: "Open les", completed: "Voltooid", notStarted: "Niet gestart",
    backToLessons: "Terug naar lessen", guidedLesson: "BEGELEIDE LES", safeLabAction: "VEILIGE LABACTIE",
    actionExplanation: "Vraag alleen de responseheaders op van het expliciet toegestane Juice Shop-target.", runAction: "Voer veilige actie uit",
    running: "Bezig…", result: "Resultaat", yourTurn: "Jij bent aan de beurt", interpretPrompt: "Wat kun je uit deze uitvoer concluderen en wat blijft onzeker?",
    markComplete: "Markeer deze les als voltooid", privateNotes: "PRIVÉNOTITIES", observations: "Jouw observaties",
    notesPrivate: "Alleen opgeslagen op deze computer en nooit toegevoegd aan Git.", notesPlaceholder: "Noteer feiten, hypotheses en vragen...",
    saveNotes: "Notities opslaan", saved: "Opgeslagen", notesHeading: "Persoonlijke leernotities",
    notesIntro: "Open een les om observaties vast te leggen. Notities blijven in .local/ en zijn uitgesloten van Git.", openLessons: "Open lessen",
    speechOn: "Spraak gereed", speechOff: "Spraak uit", requestFailed: "Opdracht mislukt", lessonComplete: "Lesvoortgang bijgewerkt",
    speechSetupLabel: "SPRAAK", speechSetupTitle: "Luister naar de lesuitleg", speechSetupBody: "Installeer de lokale Piper-stem voor de gekozen lestaal. De stem blijft op deze computer.",
    enableSpeech: "Spraak inschakelen", installingSpeech: "Stem installeren…", speechEnabled: "Spraak ingeschakeld"
  }
};

const state = { language: "en", lessons: [], progress: {}, notes: {}, speechConfigured: false, activeLesson: null };
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

async function api(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `HTTP ${response.status}`);
  return body;
}

function t(key) { return translations[state.language][key] || key; }

function toast(message, isError = false) {
  const node = $("#toast");
  node.textContent = message;
  node.classList.toggle("error", isError);
  node.classList.add("show");
  window.setTimeout(() => node.classList.remove("show"), 3200);
}

function applyLanguage() {
  document.documentElement.lang = state.language;
  $$('[data-i18n]').forEach((node) => { node.textContent = t(node.dataset.i18n); });
  $$('[data-i18n-placeholder]').forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
  $("#languageSelect").value = state.language;
  $("#speechBadge").textContent = state.speechConfigured ? t("speechOn") : t("speechOff");
  $("#speechSetupPanel").classList.toggle("configured", state.speechConfigured);
  $("#configureSpeechButton").textContent = state.speechConfigured ? t("speechEnabled") : t("enableSpeech");
  $("#configureSpeechButton").disabled = state.speechConfigured;
  renderLessons();
  updateProgress();
}

function lessonCard(lesson) {
  const done = Boolean(state.progress[lesson.id]);
  return `<article class="lesson-card" data-lesson-id="${lesson.id}">
    <div class="lesson-number">01</div>
    <div class="lesson-meta"><span class="badge ${done ? "done" : ""}">${done ? t("completed") : t("notStarted")}</span><code>${lesson.target}</code></div>
    <h3>${escapeHtml(lesson.title)}</h3><p>${escapeHtml(lesson.summary)}</p>
    <button class="secondary-button open-lesson">${t("openLesson")} <span aria-hidden="true">→</span></button>
  </article>`;
}

function renderLessons() {
  const html = state.lessons.map(lessonCard).join("");
  $("#dashboardLessons").innerHTML = html;
  $("#lessonLibrary").innerHTML = html;
  $$(".open-lesson").forEach((button) => button.addEventListener("click", () => openLesson(button.closest("[data-lesson-id]").dataset.lessonId)));
}

function updateProgress() {
  const completed = state.lessons.filter((lesson) => state.progress[lesson.id]).length;
  const percent = state.lessons.length ? Math.round((completed / state.lessons.length) * 100) : 0;
  $("#progressValue").textContent = `${percent}%`;
  $("#progressBar").style.width = `${percent}%`;
}

function showView(name) {
  $$(".view").forEach((view) => view.classList.remove("active"));
  $(`#${name}View`).classList.add("active");
  $$(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === name));
  $("#pageTitle").textContent = name === "lesson" && state.activeLesson ? state.activeLesson.title : t(name === "lessons" ? "lessons" : name === "notes" ? "notes" : "dashboard");
  document.body.classList.remove("menu-open");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

function markdownToHtml(markdown) {
  const lines = markdown.split("\n");
  let html = "", inCode = false, inList = false;
  for (const rawLine of lines) {
    if (rawLine.startsWith("```")) {
      if (inList) { html += "</ul>"; inList = false; }
      html += inCode ? "</code></pre>" : "<pre><code>";
      inCode = !inCode; continue;
    }
    if (inCode) { html += `${escapeHtml(rawLine)}\n`; continue; }
    const line = escapeHtml(rawLine).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    if (/^- /.test(line)) { if (!inList) { html += "<ul>"; inList = true; } html += `<li>${line.slice(2).replace(/^\[ \] /, "")}</li>`; continue; }
    if (inList) { html += "</ul>"; inList = false; }
    if (line.startsWith("### ")) html += `<h3>${line.slice(4)}</h3>`;
    else if (line.startsWith("## ")) html += `<h2>${line.slice(3)}</h2>`;
    else if (line.startsWith("# ")) html += `<h1>${line.slice(2)}</h1>`;
    else if (line) html += `<p>${line}</p>`;
  }
  if (inList) html += "</ul>";
  return html;
}

async function openLesson(lessonId) {
  try {
    const lesson = await api(`/api/lessons/${lessonId}`);
    state.activeLesson = lesson;
    $("#lessonTitle").textContent = lesson.title;
    $("#lessonContent").innerHTML = markdownToHtml(lesson.markdown);
    $("#commandPreview").textContent = lesson.command;
    $("#lessonNotes").value = state.notes[lessonId] || "";
    $("#completeCheckbox").checked = Boolean(state.progress[lessonId]);
    $("#resultPanel").classList.add("hidden");
    showView("lesson");
  } catch (error) { toast(error.message, true); }
}

async function runAction() {
  if (!state.activeLesson) return;
  const button = $("#runButton");
  button.disabled = true; button.firstElementChild.textContent = t("running");
  try {
    const result = await api("/api/run", { method: "POST", body: JSON.stringify({ lessonId: state.activeLesson.id, action: state.activeLesson.action }) });
    $("#commandOutput").textContent = result.output || "(no output)";
    $("#exitBadge").textContent = `exit ${result.exitCode}`;
    $("#exitBadge").classList.toggle("done", result.exitCode === 0);
    $("#resultPanel").classList.remove("hidden");
  } catch (error) { toast(`${t("requestFailed")}: ${error.message}`, true); }
  finally { button.disabled = false; button.firstElementChild.textContent = t("runAction"); }
}

async function saveNotes() {
  if (!state.activeLesson) return;
  try {
    const note = $("#lessonNotes").value;
    await api("/api/notes", { method: "POST", body: JSON.stringify({ lessonId: state.activeLesson.id, note }) });
    state.notes[state.activeLesson.id] = note;
    $("#saveStatus").textContent = t("saved");
    window.setTimeout(() => $("#saveStatus").textContent = "", 1800);
  } catch (error) { toast(error.message, true); }
}

async function setComplete() {
  if (!state.activeLesson) return;
  const complete = $("#completeCheckbox").checked;
  try {
    await api("/api/progress", { method: "POST", body: JSON.stringify({ lessonId: state.activeLesson.id, complete }) });
    state.progress[state.activeLesson.id] = complete; renderLessons(); updateProgress(); toast(t("lessonComplete"));
  } catch (error) { toast(error.message, true); }
}

async function speakLesson() {
  if (!state.speechConfigured) { toast(t("speechOff"), true); return; }
  const text = $("#lessonContent").innerText.slice(0, 1000);
  try { await api("/api/speak", { method: "POST", body: JSON.stringify({ text }) }); }
  catch (error) { toast(error.message, true); }
}

async function configureSpeech() {
  const button = $("#configureSpeechButton");
  button.disabled = true;
  button.textContent = t("installingSpeech");
  try {
    await api("/api/speech/configure", { method: "POST", body: JSON.stringify({ language: state.language }) });
    state.speechConfigured = true;
    applyLanguage();
    toast(t("speechEnabled"));
  } catch (error) {
    button.disabled = false;
    button.textContent = t("enableSpeech");
    toast(error.message, true);
  }
}

async function init() {
  try {
    Object.assign(state, await api("/api/state"));
    applyLanguage();
  } catch (error) { toast(error.message, true); }
}

$$('[data-view]').forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
$("#continueButton").addEventListener("click", () => state.lessons[0] && openLesson(state.lessons[0].id));
$("#backButton").addEventListener("click", () => showView("lessons"));
$("#runButton").addEventListener("click", runAction);
$("#saveNotesButton").addEventListener("click", saveNotes);
$("#completeCheckbox").addEventListener("change", setComplete);
$("#speakButton").addEventListener("click", speakLesson);
$("#configureSpeechButton").addEventListener("click", configureSpeech);
$("#menuButton").addEventListener("click", () => document.body.classList.toggle("menu-open"));
$("#languageSelect").addEventListener("change", async (event) => {
  try {
    await api("/api/language", { method: "POST", body: JSON.stringify({ language: event.target.value }) });
    Object.assign(state, await api("/api/state")); applyLanguage(); showView("dashboard");
  } catch (error) { toast(error.message, true); }
});
init();
