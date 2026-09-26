"use strict";

const $ = (sel, root = document) => root.querySelector(sel);
const STATUS_LABELS = {
  draft: "Nháp", analyzing: "Đang phân tích", storyboard_ready: "Chờ duyệt storyboard",
  rendering: "Đang render", done: "Hoàn thành", failed: "Lỗi",
};

let config = null;
let current = null;       // project JSON from the API
let pollTimer = null;
let storyboardDirty = false;

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map(d => d.msg).join("; ") : data.detail;
    throw new Error(detail || `Lỗi ${res.status}`);
  }
  return data;
}
const jsonBody = (obj) => ({ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(obj) });

function show(view) {
  for (const id of ["view-new", "view-project", "view-empty"]) $("#" + id).classList.toggle("hidden", id !== view);
}

// ------------------------------------------------------------------ project list

async function refreshList() {
  const projects = await api("/api/projects");
  const list = $("#project-list");
  list.innerHTML = "";
  for (const p of projects) {
    const li = document.createElement("li");
    li.textContent = p.name;
    const small = document.createElement("small");
    small.textContent = `${STATUS_LABELS[p.status] || p.status} · $${p.spent_usd.toFixed(2)}`;
    li.append(small);
    li.classList.toggle("active", current && current.id === p.id);
    li.onclick = () => openProject(p.id);
    list.append(li);
  }
}

// ------------------------------------------------------------------ new project

$("#btn-new").onclick = () => { current = null; stopPolling(); show("view-new"); refreshList(); };

$("#form-new").onsubmit = async (e) => {
  e.preventDefault();
  const btn = e.submitter;
  btn.disabled = true;
  try {
    const form = new FormData(e.target);
    for (const key of ["reference_video", "music"]) {
      const f = form.get(key);
      if (f && !f.name) form.delete(key);
    }
    const project = await api("/api/projects", { method: "POST", body: form });
    await api(`/api/projects/${project.id}/analyze`, { method: "POST" });
    e.target.reset();
    await openProject(project.id);
  } catch (err) {
    alert(err.message);
  } finally {
    btn.disabled = false;
  }
};

// ------------------------------------------------------------------ project view

async function openProject(id) {
  storyboardDirty = false;
  current = await api(`/api/projects/${id}`);
  show("view-project");
  renderProject(true);
  refreshList();
  schedulePoll();
}

function isBusy(p) { return p.status === "analyzing" || p.status === "rendering"; }

function stopPolling() { clearTimeout(pollTimer); pollTimer = null; }

function schedulePoll() {
  stopPolling();
  if (!current || !isBusy(current)) return;
  pollTimer = setTimeout(async () => {
    const id = current.id;
    const wasStatus = current.status;
    try {
      const fresh = await api(`/api/projects/${id}`);
      if (!current || current.id !== id) return;
      const storyboardArrived = wasStatus === "analyzing" && fresh.status !== "analyzing";
      current = fresh;
      renderProject(storyboardArrived && !storyboardDirty);
      if (!isBusy(fresh)) refreshList();
    } catch (err) { console.error(err); }
    schedulePoll();
  }, 2500);
}

function renderProject(rebuildStoryboard) {
  const p = current;
  $("#p-name").textContent = p.name;
  const status = $("#p-status");
  status.textContent = STATUS_LABELS[p.status] || p.status;
  status.className = "status " + p.status;
  $("#p-progress").textContent = p.progress || "";
  $("#p-error").textContent = p.error || "";
  $("#p-error").classList.toggle("hidden", !p.error);
  $("#p-spent").textContent = p.spent_usd ? `Đã chi ~ $${p.spent_usd.toFixed(2)}` : "";
  $("#btn-analyze").disabled = isBusy(p);

  const a = p.storyboard && p.storyboard.reference_analysis;
  $("#analysis").classList.toggle("hidden", !a);
  if (a) {
    const rows = [["Hook", a.hook], ["Cấu trúc", a.structure], ["Phong cách", a.style], ["Vì sao hiệu quả", a.why_it_works]];
    if (p.transcript) rows.push(["Lời thoại gốc", p.transcript]);
    const dl = $("#analysis-body");
    dl.innerHTML = "";
    for (const [k, v] of rows) {
      const dt = document.createElement("dt"); dt.textContent = k;
      const dd = document.createElement("dd"); dd.textContent = v; dd.style.whiteSpace = "pre-wrap";
      dl.append(dt, dd);
    }
  }

  const hasSb = !!p.storyboard;
  $("#storyboard").classList.toggle("hidden", !hasSb);
  $("#render").classList.toggle("hidden", !hasSb);
  if (hasSb && rebuildStoryboard) {
    buildStoryboardEditor(p.storyboard);
    fillRenderSettings(p.settings);
  }
  if (hasSb) updateEstimate(p.estimate);
  $("#btn-render").disabled = isBusy(p);
  $("#btn-save-sb").disabled = isBusy(p);

  renderSegments(p);

  $("#final").classList.toggle("hidden", !p.final_video);
  if (p.final_video) {
    const src = p.final_video + "?t=" + encodeURIComponent(p.progress + p.spent_usd);
    const video = $("#final-video");
    if (video.dataset.src !== src) { video.src = src; video.dataset.src = src; }
    $("#final-download").href = p.final_video;
    $("#final-download").setAttribute("download", `${p.name}.mp4`);
  }
}

$("#btn-analyze").onclick = async () => {
  if (current.storyboard && !confirm("Phân tích lại sẽ thay storyboard hiện tại. Tiếp tục?")) return;
  try {
    current = await api(`/api/projects/${current.id}/analyze`, { method: "POST" });
    storyboardDirty = false;
    renderProject(false);
    schedulePoll();
  } catch (err) { alert(err.message); }
};

// ------------------------------------------------------------------ storyboard editor

function buildStoryboardEditor(sb) {
  $("#sb-title").value = sb.title || "";
  const container = $("#shots");
  container.innerHTML = "";
  sb.shots.forEach(shot => container.append(shotElement(shot)));
  renumberShots();
}

function shotElement(shot) {
  const el = $("#tpl-shot").content.firstElementChild.cloneNode(true);
  $(".f-duration", el).value = shot.duration_s;
  $(".f-purpose", el).value = shot.purpose || "";
  $(".f-prompt", el).value = shot.prompt || "";
  $(".f-voiceover", el).value = shot.voiceover || "";
  if (shot.copy_reference_motion) {
    $(".f-ref-start", el).value = shot.copy_reference_motion.start_s;
    $(".f-ref-end", el).value = shot.copy_reference_motion.end_s;
  }
  $(".btn-remove", el).onclick = () => { el.remove(); renumberShots(); markDirty(); };
  el.addEventListener("input", markDirty);
  return el;
}

function renumberShots() {
  const shots = [...document.querySelectorAll("#shots .shot")];
  shots.forEach((el, i) => { $(".shot-no", el).textContent = `Cảnh ${i + 1}`; });
  const total = shots.reduce((sum, el) => sum + (parseFloat($(".f-duration", el).value) || 0), 0);
  $("#sb-duration").textContent = `· ${total.toFixed(1)} giây`;
}

function markDirty() { storyboardDirty = true; renumberShots(); $("#btn-save-sb").textContent = "Lưu storyboard *"; }

function readStoryboard() {
  const shots = [...document.querySelectorAll("#shots .shot")].map(el => {
    const start = $(".f-ref-start", el).value, end = $(".f-ref-end", el).value;
    return {
      duration_s: parseFloat($(".f-duration", el).value) || 3,
      purpose: $(".f-purpose", el).value,
      prompt: $(".f-prompt", el).value,
      voiceover: $(".f-voiceover", el).value,
      on_screen_text: "",
      copy_reference_motion: start !== "" && end !== "" ? { start_s: parseFloat(start), end_s: parseFloat(end) } : null,
    };
  });
  return { ...current.storyboard, title: $("#sb-title").value, shots };
}

$("#btn-add-shot").onclick = () => {
  $("#shots").append(shotElement({ duration_s: 3, purpose: "", prompt: "", voiceover: "" }));
  markDirty();
};

async function saveStoryboard() {
  current = await api(`/api/projects/${current.id}/storyboard`, {
    method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(readStoryboard()),
  });
  storyboardDirty = false;
  $("#btn-save-sb").textContent = "Lưu storyboard";
  renderProject(false);
}

$("#btn-save-sb").onclick = () => saveStoryboard().catch(err => alert(err.message));
$("#sb-title").addEventListener("input", markDirty);

// ------------------------------------------------------------------ render settings

function fillSelect(select, options, value) {
  select.innerHTML = "";
  for (const [val, label] of options) {
    const o = document.createElement("option");
    o.value = val; o.textContent = label;
    select.append(o);
  }
  if (value !== undefined && options.some(([v]) => v === value)) select.value = value;
}

function modelByKey(key) { return config.models.find(m => m.key === key); }

function fillRenderSettings(s) {
  fillSelect($("#r-model"), config.models.map(m => [m.key, m.label]), s.video_model);
  fillResolutions(s.resolution);
  $("#r-aspect").value = s.aspect_ratio;
  fillSelect($("#r-voice"), config.voices.map(v => [v, v]), s.voice);
  $("#r-voiceover").checked = s.voiceover;
  $("#r-subtitles").checked = s.subtitles;
}

function fillResolutions(value) {
  const m = modelByKey($("#r-model").value);
  fillSelect($("#r-resolution"), m.resolutions.map(r => [r, `${r} · ~$${m.usd_per_second[r].toFixed(3)}/giây`]), value || "720p");
  $("#r-model-notes").textContent = m.notes;
}

function readRenderSettings() {
  return {
    ...current.settings,
    video_model: $("#r-model").value,
    resolution: $("#r-resolution").value,
    aspect_ratio: $("#r-aspect").value,
    voice: $("#r-voice").value,
    voiceover: $("#r-voiceover").checked,
    subtitles: $("#r-subtitles").checked,
  };
}

function updateEstimate(est) {
  if (!est) return;
  const segs = est.segments.map((s, i) =>
    `Clip ${i + 1}: cảnh ${s.shots.map(n => n + 1).join(", ")} · ${s.duration}s · $${s.usd.toFixed(2)}${s.video_reference ? " (có video tham chiếu ×0.6)" : ""}`
  ).join("<br>");
  $("#estimate").innerHTML =
    `Chi phí ước tính: <b>$${est.total_usd.toFixed(2)}</b> <span class="muted">(video $${est.video_usd.toFixed(2)} + giọng đọc $${est.voiceover_usd.toFixed(2)})</span><br>` +
    `<span class="muted small">${segs}<br>${est.note}</span>`;
}

async function refreshEstimate() {
  if (!current || !current.storyboard) return;
  try {
    if (storyboardDirty) return;  // estimate reflects the saved storyboard
    updateEstimate(await api(`/api/projects/${current.id}/estimate`, jsonBody(readRenderSettings())));
  } catch (err) { $("#estimate").textContent = err.message; }
}

$("#r-model").onchange = () => { fillResolutions($("#r-resolution").value); refreshEstimate(); };
for (const id of ["#r-resolution", "#r-aspect", "#r-voiceover"]) $(id).onchange = refreshEstimate;

$("#btn-render").onclick = async () => {
  try {
    if (storyboardDirty) await saveStoryboard();
    const est = await api(`/api/projects/${current.id}/estimate`, jsonBody(readRenderSettings()));
    const cost = config.demo_mode ? "DEMO_MODE: không tốn tiền." : `Chi phí ước tính ~ $${est.total_usd.toFixed(2)}.`;
    if (!confirm(`Render ${est.segments.length} clip bằng ${est.model} ${est.resolution}?\n${cost}`)) return;
    current = await api(`/api/projects/${current.id}/render`, jsonBody(readRenderSettings()));
    renderProject(false);
    schedulePoll();
  } catch (err) { alert(err.message); }
};

// ------------------------------------------------------------------ segments

function renderSegments(p) {
  $("#segments").classList.toggle("hidden", !p.segments.length);
  const list = $("#segment-list");
  // Keep open textareas while polling: only rebuild when something visible changed.
  const signature = JSON.stringify(p.segments.map(s => [s.status, s.local_path, s.error, s.prompt])) + isBusy(p);
  if (list.dataset.sig === signature) return;
  list.dataset.sig = signature;
  list.innerHTML = "";
  for (const s of p.segments) {
    const row = document.createElement("div");
    row.className = "segment";
    const left = document.createElement("div");
    if (s.local_path) {
      const v = document.createElement("video");
      v.src = s.local_path + "?t=" + encodeURIComponent(s.request_id || s.status);
      v.controls = true; v.playsInline = true;
      left.append(v);
    } else {
      left.textContent = s.status === "running" ? "⏳ Đang tạo…" : s.status === "failed" ? "❌ Lỗi" : "Chờ…";
    }
    const right = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = `Clip ${s.index + 1} · cảnh ${s.shot_indexes.map(n => n + 1).join(", ")} · ${s.duration}s`;
    const prompt = document.createElement("textarea");
    prompt.rows = 5; prompt.value = s.prompt;
    const btn = document.createElement("button");
    btn.textContent = "Tạo lại clip này";
    btn.disabled = isBusy(p);
    btn.onclick = async () => {
      const cost = modelByKey(p.settings.video_model).usd_per_second[p.settings.resolution] * s.duration;
      if (!config.demo_mode && !confirm(`Tạo lại clip ${s.index + 1}? ~ $${cost.toFixed(2)}`)) return;
      try {
        current = await api(`/api/projects/${p.id}/segments/${s.index}/regenerate`, jsonBody({ prompt: prompt.value }));
        renderProject(false);
        schedulePoll();
      } catch (err) { alert(err.message); }
    };
    right.append(title, prompt, btn);
    if (s.error) {
      const e = document.createElement("p");
      e.className = "error small"; e.textContent = s.error;
      right.append(e);
    }
    row.append(left, right);
    list.append(row);
  }
}

// ------------------------------------------------------------------ boot

(async function boot() {
  config = await api("/api/config");
  const missing = [];
  if (!config.demo_mode) {
    if (!config.has_fal_key) missing.push("FAL_KEY");
    if (!config.has_anthropic_key) missing.push("ANTHROPIC_API_KEY");
  }
  $("#mode-badge").textContent = config.demo_mode ? "DEMO MODE — không gọi API" : missing.length ? `Thiếu ${missing.join(", ")} trong .env` : "";
  await refreshList();
})();
