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
    enableSpeech: "Enable speech", installingSpeech: "Installing voice…", speechEnabled: "Speech enabled", settings: "Settings",
    aiTeacher: "AI TEACHER", reviewWithAi: "Discuss with AI", reviewing: "Reviewing…", aiNotConfigured: "Configure an AI backend in Settings first.",
    aiLocalSummary: "Review data stays with your configured local backend.", aiExternalSummary: "Selected lesson data is sent to your external AI provider.",
    useSubscription: "USE YOUR EXISTING SUBSCRIPTION", copyDiscussionTitle: "Discuss in ChatGPT or Codex", copyDiscussionIntro: "Copy your lesson context and notes, then paste them into an existing ChatGPT or Codex conversation. No API key is needed.", copyForDiscussion: "Copy for ChatGPT/Codex", copiedForDiscussion: "Lesson context and notes copied.", copyFailed: "Could not copy automatically. Select and copy your notes manually.", discussionPrompt: "Act as my cybersecurity teacher. Review my reasoning, distinguish facts from assumptions, give a hint before a solution, and finish with one control question. Only discuss the explicitly permitted lab target.", discussionLesson: "Lesson", discussionTarget: "Permitted target", discussionCommand: "Command", discussionOutput: "Command output", discussionNotes: "My observations and questions", notRunYet: "The command has not been run yet.", noNotesYet: "I have not written any notes yet.",
    aiSettingsLabel: "AI GUIDANCE", aiSettingsTitle: "Choose how to discuss your work", aiSettingsIntro: "Choose whether you want to copy work to an existing chat, or connect the lab directly to an API.",
    easiest: "Easiest", integrated: "Integrated", manualChoiceTitle: "Copy to ChatGPT or Codex", manualChoiceBody: "Use the copy button in a lesson and paste the text into your existing ChatGPT or Codex conversation. This uses your normal account and needs no API key.", apiChoiceTitle: "Connect an AI API", apiChoiceBody: "Receive feedback inside this webpage. OpenAI requires a separate Platform API key and API billing; ChatGPT Plus alone does not provide this. Ollama can run locally without an API account.", apiConfiguration: "API configuration",
    provider: "Provider", providerNone: "No AI", serverAddress: "Server address", model: "Model", apiKey: "API key", apiKeyPlaceholder: "Leave blank to keep the stored key",
    sharedData: "Data included in a review", shareLesson: "Lesson material", shareOutput: "Command output", shareNotes: "Your answer and notes", externalWarning: "This provider can send the selected lesson data outside this computer.",
    saveSettings: "Save settings", testConnection: "Test connection", settingsSaved: "AI settings saved.", testing: "Testing…", connectionOk: "Connection successful"
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
    enableSpeech: "Spraak inschakelen", installingSpeech: "Stem installeren…", speechEnabled: "Spraak ingeschakeld", settings: "Instellingen",
    aiTeacher: "AI-DOCENT", reviewWithAi: "Bespreek met AI", reviewing: "Beoordelen…", aiNotConfigured: "Configureer eerst een AI-backend bij Instellingen.",
    aiLocalSummary: "Beoordelingsgegevens blijven bij je ingestelde lokale backend.", aiExternalSummary: "Geselecteerde lesgegevens worden naar je externe AI-provider gestuurd.",
    useSubscription: "GEBRUIK JE BESTAANDE ABONNEMENT", copyDiscussionTitle: "Bespreek in ChatGPT of Codex", copyDiscussionIntro: "Kopieer je lescontext en notities en plak ze in een bestaand ChatGPT- of Codex-gesprek. Hiervoor is geen API-sleutel nodig.", copyForDiscussion: "Kopieer voor ChatGPT/Codex", copiedForDiscussion: "Lescontext en notities zijn gekopieerd.", copyFailed: "Automatisch kopiëren is mislukt. Selecteer en kopieer je notities handmatig.", discussionPrompt: "Gedraag je als mijn cybersecuritydocent. Beoordeel mijn redenering, onderscheid feiten van aannames, geef eerst een hint en eindig met één controlevraag. Bespreek uitsluitend het expliciet toegestane labtarget.", discussionLesson: "Les", discussionTarget: "Toegestaan target", discussionCommand: "Commando", discussionOutput: "Commando-uitvoer", discussionNotes: "Mijn observaties en vragen", notRunYet: "Het commando is nog niet uitgevoerd.", noNotesYet: "Ik heb nog geen notities geschreven.",
    aiSettingsLabel: "AI-BEGELEIDING", aiSettingsTitle: "Kies hoe je jouw werk bespreekt", aiSettingsIntro: "Kies of je werk naar een bestaand gesprek kopieert of het lab rechtstreeks met een API verbindt.",
    easiest: "Eenvoudigst", integrated: "Geïntegreerd", manualChoiceTitle: "Kopieer naar ChatGPT of Codex", manualChoiceBody: "Gebruik de kopieerknop in een les en plak de tekst in je bestaande ChatGPT- of Codex-gesprek. Dit gebruikt je normale account en vereist geen API-sleutel.", apiChoiceTitle: "Koppel een AI-API", apiChoiceBody: "Ontvang feedback binnen deze webpagina. OpenAI vereist een aparte Platform API-sleutel en API-facturering; alleen ChatGPT Plus is niet voldoende. Ollama kan lokaal zonder API-account draaien.", apiConfiguration: "API-configuratie",
    provider: "Provider", providerNone: "Geen AI", serverAddress: "Serveradres", model: "Model", apiKey: "API-sleutel", apiKeyPlaceholder: "Laat leeg om de opgeslagen sleutel te behouden",
    sharedData: "Gegevens in een beoordeling", shareLesson: "Lesmateriaal", shareOutput: "Commando-uitvoer", shareNotes: "Jouw antwoord en notities", externalWarning: "Deze provider kan de geselecteerde lesgegevens buiten deze computer versturen.",
    saveSettings: "Instellingen opslaan", testConnection: "Verbinding testen", settingsSaved: "AI-instellingen opgeslagen.", testing: "Testen…", connectionOk: "Verbinding geslaagd"
  }
};

const state = { language: "en", lessons: [], progress: {}, notes: {}, speechConfigured: false, aiSettings: {}, activeLesson: null };
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
  renderAiSettings();
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
  $("#pageTitle").textContent = name === "lesson" && state.activeLesson ? state.activeLesson.title : t(["lessons", "notes", "settings"].includes(name) ? name : "dashboard");
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
    $("#aiFeedback").classList.add("hidden");
    $("#aiFeedback").textContent = "";
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

function discussionText() {
  const lesson = state.activeLesson;
  const outputVisible = !$("#resultPanel").classList.contains("hidden");
  const output = outputVisible ? $("#commandOutput").textContent.trim() : t("notRunYet");
  const note = $("#lessonNotes").value.trim() || t("noNotesYet");
  return `${t("discussionPrompt")}\n\n${t("discussionLesson")}: ${lesson.title}\n${t("discussionTarget")}: ${lesson.target}\n${t("discussionCommand")}: ${lesson.command}\n\n${t("discussionOutput")}:\n${output}\n\n${t("discussionNotes")}:\n${note}`;
}

async function copyDiscussion() {
  if (!state.activeLesson) return;
  const value = discussionText();
  try {
    if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(value);
    else {
      const area = document.createElement("textarea"); area.value = value; area.style.position = "fixed"; area.style.opacity = "0";
      document.body.appendChild(area); area.select();
      if (!document.execCommand("copy")) throw new Error("copy failed");
      area.remove();
    }
    toast(t("copiedForDiscussion"));
  } catch (error) { toast(t("copyFailed"), true); }
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

function renderAiSettings() {
  const settings = state.aiSettings || {};
  const provider = settings.provider || "none";
  $("#aiProvider").value = provider;
  $("#aiBaseUrl").value = settings.baseUrl || (provider === "ollama" ? "http://127.0.0.1:11434" : "");
  $("#aiModel").value = settings.model || "";
  $("#sendLesson").checked = settings.sendLesson !== false;
  $("#sendOutput").checked = settings.sendOutput !== false;
  $("#sendNotes").checked = settings.sendNotes !== false;
  const needsUrl = ["ollama", "openai-compatible"].includes(provider);
  const needsKey = ["openai", "openai-compatible"].includes(provider);
  $("#baseUrlField").classList.toggle("hidden", !needsUrl);
  $("#apiKeyField").classList.toggle("hidden", !needsKey);
  $("#externalWarning").classList.toggle("hidden", !["openai", "openai-compatible"].includes(provider));
  $("#testAiButton").disabled = provider === "none";
  $("#reviewButton").disabled = provider === "none";
  $("#aiPrivacySummary").textContent = provider === "none" ? t("aiNotConfigured") : provider === "ollama" ? t("aiLocalSummary") : t("aiExternalSummary");
}

async function saveAiSettings(event) {
  event.preventDefault();
  const payload = {
    provider: $("#aiProvider").value, baseUrl: $("#aiBaseUrl").value, model: $("#aiModel").value,
    apiKey: $("#aiApiKey").value, sendLesson: $("#sendLesson").checked,
    sendOutput: $("#sendOutput").checked, sendNotes: $("#sendNotes").checked
  };
  try {
    state.aiSettings = await api("/api/ai/settings", { method: "POST", body: JSON.stringify(payload) });
    $("#aiApiKey").value = ""; $("#aiSettingsStatus").textContent = t("settingsSaved"); renderAiSettings();
  } catch (error) { toast(error.message, true); }
}

async function testAi() {
  const button = $("#testAiButton"); button.disabled = true; button.textContent = t("testing");
  try {
    const result = await api("/api/ai/test", { method: "POST", body: "{}" });
    $("#aiSettingsStatus").textContent = `${t("connectionOk")}: ${result.reply}`;
  } catch (error) { toast(error.message, true); }
  finally { button.textContent = t("testConnection"); button.disabled = (state.aiSettings.provider || "none") === "none"; }
}

async function reviewWithAi() {
  if (!state.activeLesson || (state.aiSettings.provider || "none") === "none") { toast(t("aiNotConfigured"), true); return; }
  const button = $("#reviewButton"); button.disabled = true; button.textContent = t("reviewing");
  try {
    const result = await api("/api/ai/review", { method: "POST", body: JSON.stringify({
      lessonId: state.activeLesson.id, note: $("#lessonNotes").value, output: $("#commandOutput").textContent
    }) });
    $("#aiFeedback").textContent = result.feedback; $("#aiFeedback").classList.remove("hidden");
  } catch (error) { toast(error.message, true); }
  finally { button.disabled = false; button.textContent = t("reviewWithAi"); }
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
$("#copyDiscussionButton").addEventListener("click", copyDiscussion);
$("#completeCheckbox").addEventListener("change", setComplete);
$("#speakButton").addEventListener("click", speakLesson);
$("#configureSpeechButton").addEventListener("click", configureSpeech);
$("#aiSettingsForm").addEventListener("submit", saveAiSettings);
$("#testAiButton").addEventListener("click", testAi);
$("#reviewButton").addEventListener("click", reviewWithAi);
$("#aiProvider").addEventListener("change", () => { state.aiSettings = { ...state.aiSettings, provider: $("#aiProvider").value, baseUrl: $("#aiBaseUrl").value, model: $("#aiModel").value }; renderAiSettings(); });
$("#menuButton").addEventListener("click", () => document.body.classList.toggle("menu-open"));
$("#languageSelect").addEventListener("change", async (event) => {
  try {
    await api("/api/language", { method: "POST", body: JSON.stringify({ language: event.target.value }) });
    Object.assign(state, await api("/api/state")); applyLanguage(); showView("dashboard");
  } catch (error) { toast(error.message, true); }
});
init();
