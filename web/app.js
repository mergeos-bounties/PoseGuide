const CATALOG_URLS = ["data/catalog.json", "web/data/catalog.json"];
const SKELETON_EDGES = [
  ["nose", "l_shoulder"],
  ["nose", "r_shoulder"],
  ["l_shoulder", "r_shoulder"],
  ["l_shoulder", "l_elbow"],
  ["l_elbow", "l_wrist"],
  ["r_shoulder", "r_elbow"],
  ["r_elbow", "r_wrist"],
  ["l_shoulder", "l_hip"],
  ["r_shoulder", "r_hip"],
  ["l_hip", "r_hip"],
  ["l_hip", "l_knee"],
  ["l_knee", "l_ankle"],
  ["r_hip", "r_knee"],
  ["r_knee", "r_ankle"],
];

const TAG_HINTS = {
  balcony: ["urban", "balcony", "cityscape", "outdoor"],
  beach: ["beach", "outdoor", "golden_hour", "portrait"],
  city: ["urban", "cityscape", "street", "outdoor"],
  forest: ["forest", "outdoor", "romantic", "portrait"],
  home: ["indoor", "home", "window", "soft_light"],
  office: ["indoor", "business", "confident", "studio"],
  studio: ["studio", "indoor", "portrait", "confident"],
  street: ["street", "urban", "motion", "daylight"],
  wall: ["urban", "wall", "street", "casual"],
  window: ["indoor", "window", "soft_light", "portrait"],
};

const state = {
  catalog: null,
  selectedTags: new Set(),
  catalogFilterTags: new Set(),
  backgroundTags: new Set(),
  backgroundName: "",
  backgroundImage: null,
  lastResults: [],
  currentView: "recommend",
};

const els = {};

document.addEventListener("DOMContentLoaded", init);

async function init() {
  bindElements();
  wireEvents();
  state.catalog = await loadCatalog();
  populateScenes();
  selectScene(state.catalog.scenes[0].id);
  setStatus("Offline catalog ready");
  await recommend();
  renderCatalogView();
}

function bindElements() {
  els.status = document.getElementById("runStatus");
  els.source = document.getElementById("sourceLabel");
  els.scenePreset = document.getElementById("scenePreset");
  els.tagChips = document.getElementById("tagChips");
  els.customTags = document.getElementById("customTags");
  els.addTags = document.getElementById("addTags");
  els.backgroundFile = document.getElementById("backgroundFile");
  els.useApi = document.getElementById("useApi");
  els.apiUrl = document.getElementById("apiUrl");
  els.topK = document.getElementById("topK");
  els.recommend = document.getElementById("recommend");
  els.results = document.getElementById("resultsList");
  els.canvas = document.getElementById("poseCanvas");
  els.tabRecommend = document.getElementById("tabRecommend");
  els.tabCatalog = document.getElementById("tabCatalog");
  els.viewRecommend = document.getElementById("viewRecommend");
  els.viewCatalog = document.getElementById("viewCatalog");
  els.catalogTagChips = document.getElementById("catalogTagChips");
  els.catalogGrid = document.getElementById("catalogGrid");
  els.catalogCount = document.getElementById("catalogCount");
}

function wireEvents() {
  els.scenePreset.addEventListener("change", () => {
    selectScene(els.scenePreset.value);
    recommend();
  });
  els.addTags.addEventListener("click", () => {
    addCustomTags();
    recommend();
  });
  els.customTags.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addCustomTags();
      recommend();
    }
  });
  els.backgroundFile.addEventListener("change", handleBackground);
  els.useApi.addEventListener("change", recommend);
  els.topK.addEventListener("change", recommend);
  els.recommend.addEventListener("click", recommend);
  els.tabRecommend.addEventListener("click", () => switchView("recommend"));
  els.tabCatalog.addEventListener("click", () => switchView("catalog"));
}

function switchView(view) {
  state.currentView = view;
  els.tabRecommend.className = view === "recommend" ? "tab active" : "tab";
  els.tabCatalog.className = view === "catalog" ? "tab active" : "tab";
  els.viewRecommend.classList.toggle("hidden", view !== "recommend");
  els.viewCatalog.classList.toggle("hidden", view !== "catalog");
}

async function loadCatalog() {
  for (const url of CATALOG_URLS) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
    }
  }
  throw new Error("PoseGuide web catalog could not be loaded");
}

function populateScenes() {
  els.scenePreset.replaceChildren(
    ...state.catalog.scenes.map((scene) => {
      const option = document.createElement("option");
      option.value = scene.id;
      option.textContent = scene.name;
      return option;
    })
  );
}

function selectScene(sceneId) {
  const scene = state.catalog.scenes.find((item) => item.id === sceneId) || state.catalog.scenes[0];
  els.scenePreset.value = scene.id;
  state.selectedTags = new Set([...scene.tags, ...scene.mood]);
  renderTagChips();
}

function renderTagChips() {
  const active = getActiveTags();
  const tags = [...new Set([...state.catalog.tags, ...active])].sort();
  els.tagChips.replaceChildren(
    ...tags.map((tag) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = active.includes(tag) ? "chip active" : "chip";
      chip.textContent = tag.replaceAll("_", " ");
      chip.setAttribute("aria-pressed", active.includes(tag) ? "true" : "false");
      chip.addEventListener("click", () => {
        if (state.selectedTags.has(tag)) {
          state.selectedTags.delete(tag);
        } else {
          state.selectedTags.add(tag);
        }
        renderTagChips();
        recommend();
      });
      return chip;
    })
  );
}

function addCustomTags() {
  for (const tag of splitTags(els.customTags.value)) {
    state.selectedTags.add(tag);
  }
  els.customTags.value = "";
  renderTagChips();
}

// ─── Catalog view ───

function renderCatalogView() {
  renderCatalogTagChips();
  renderCatalogGrid();
}

function renderCatalogTagChips() {
  const active = [...state.catalogFilterTags];
  const tags = [...new Set([...state.catalog.tags, ...active])].sort();
  els.catalogTagChips.replaceChildren(
    ...tags.map((tag) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = state.catalogFilterTags.has(tag) ? "chip active" : "chip";
      chip.textContent = tag.replaceAll("_", " ");
      chip.setAttribute("aria-pressed", state.catalogFilterTags.has(tag) ? "true" : "false");
      chip.addEventListener("click", () => {
        if (state.catalogFilterTags.has(tag)) {
          state.catalogFilterTags.delete(tag);
        } else {
          state.catalogFilterTags.add(tag);
        }
        renderCatalogTagChips();
        renderCatalogGrid();
      });
      return chip;
    })
  );
}

function renderCatalogGrid() {
  const filterTags = [...state.catalogFilterTags];
  const poses = state.catalog.poses.filter((pose) => {
    if (filterTags.length === 0) return true;
    const poseTags = new Set(pose.tags || []);
    return filterTags.some((tag) => poseTags.has(tag));
  });
  els.catalogCount.textContent = `${poses.length} of ${state.catalog.poses.length} poses`;
  els.catalogGrid.replaceChildren(
    ...poses.map((pose) => {
      const card = document.createElement("div");
      card.className = "catalog-card";
      card.addEventListener("click", () => {
        switchView("recommend");
        state.selectedTags = new Set(pose.tags || []);
        renderTagChips();
        recommend();
      });
      const svg = createPoseSvg(pose);
      svg.setAttribute("width", "100");
      svg.setAttribute("height", "128");
      svg.classList.add("catalog-svg");
      card.append(svg);
      const name = document.createElement("span");
      name.className = "catalog-name";
      name.textContent = pose.name || pose.id;
      card.append(name);
      const tags = document.createElement("span");
      tags.className = "catalog-tags";
      tags.textContent = (pose.tags || []).slice(0, 3).join(", ");
      card.append(tags);
      return card;
    })
  );
}

// ─── Background ───

async function handleBackground() {
  const file = els.backgroundFile.files[0];
  state.backgroundTags.clear();
  state.backgroundName = "";
  state.backgroundImage = null;

  if (!file) {
    renderTagChips();
    return recommend();
  }

  state.backgroundName = file.name;
  for (const tag of inferTagsFromName(file.name)) {
    state.backgroundTags.add(tag);
    state.selectedTags.add(tag);
  }

  const image = new Image();
  image.onload = () => {
    state.backgroundImage = image;
    drawPose(state.lastResults[0]);
  };
  image.src = URL.createObjectURL(file);
  renderTagChips();
  return recommend();
}

// ─── Recommend ───

async function recommend() {
  const tags = getActiveTags();
  const topK = Number.parseInt(els.topK.value, 10) || 3;
  setStatus("Ranking poses");

  try {
    if (els.useApi.checked) {
      const apiResults = await recommendViaApi(tags, topK);
      state.lastResults = hydrateResults(apiResults);
      els.source.textContent = "Local API";
    } else {
      state.lastResults = rankOffline(tags, topK);
      els.source.textContent = "Offline catalog";
    }
  } catch (error) {
    state.lastResults = rankOffline(tags, topK);
    els.source.textContent = "Offline catalog";
  }

  renderResults(state.lastResults);
  drawPose(state.lastResults[0]);
  setStatus(`${state.lastResults.length} poses ready`);
}

async function recommendViaApi(tags, topK) {
  const base = els.apiUrl.value.trim().replace(/\/$/, "");
  if (!base) {
    throw new Error("Local API URL is empty");
  }
  const response = await fetch(`${base}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tags,
      top_k: topK,
      background_name: state.backgroundName || null,
    }),
  });
  if (!response.ok) {
    throw new Error(`Local API returned ${response.status}`);
  }
  const payload = await response.json();
  const recommendations = Array.isArray(payload)
    ? payload
    : payload.recommendations || payload.results || [];
  if (!Array.isArray(recommendations)) {
    throw new Error("Local API response did not include recommendations");
  }
  return recommendations.slice(0, topK);
}

function rankOffline(tags, topK) {
  const sceneTags = new Set(tags);
  const ranked = state.catalog.poses.map((pose) => {
    const poseTags = new Set(pose.tags || []);
    const overlap = [...sceneTags].filter((tag) => poseTags.has(tag)).sort();
    const union = new Set([...sceneTags, ...poseTags]);
    const tagScore = union.size ? overlap.length / union.size : 0;
    let score = 0.65 * tagScore + 0.35 * 0.5;
    if (pose.standing !== false && sceneTags.has("outdoor")) {
      score = Math.min(1, score + 0.05);
    }
    return {
      ...pose,
      pose_id: pose.id,
      score: Math.round(score * 10000) / 10000,
      tag_overlap: overlap,
    };
  });
  return ranked.sort((a, b) => b.score - a.score).slice(0, Math.max(1, topK));
}

function hydrateResults(results) {
  return results.map((item) => {
    const id = item.pose_id || item.id;
    const pose = state.catalog.poses.find((candidate) => candidate.id === id) || {};
    return {
      ...pose,
      ...item,
      pose_id: id,
      name: item.name || pose.name || id,
      tag_overlap: item.tag_overlap || item.tagOverlap || [],
      tips: item.tips || pose.tips || [],
      camera_cues: item.camera_cues || item.cameraCues || pose.camera_cues || [],
      score: Number(item.score || 0),
    };
  });
}

function renderResults(results) {
  els.results.replaceChildren(
    ...results.map((pose) => {
      const item = document.createElement("li");
      item.className = "result";
      item.append(createPoseSvg(pose));

      const body = document.createElement("div");
      const title = document.createElement("h3");
      title.textContent = pose.name || pose.pose_id;
      const meta = document.createElement("p");
      meta.className = "meta";
      const overlap = (pose.tag_overlap || []).join(", ") || "catalog prior";
      const score = document.createElement("span");
      score.className = "score";
      score.textContent = pose.score.toFixed(2);
      meta.append(score, document.createTextNode(` ${overlap}`));
      const tips = document.createElement("p");
      tips.className = "tips";
      tips.textContent = [...(pose.tips || []), ...(pose.camera_cues || [])].slice(0, 3).join(" / ");
      body.append(title, meta, tips);
      item.append(body);
      item.addEventListener("click", () => drawPose(pose));
      return item;
    })
  );
}

function createPoseSvg(pose) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 100 128");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", pose.name || pose.pose_id || "Pose");

  for (const [from, to] of SKELETON_EDGES) {
    const a = pose.joints?.[from];
    const b = pose.joints?.[to];
    if (!a || !b) continue;
    const line = document.createElementNS(svg.namespaceURI, "line");
    line.setAttribute("x1", String(a[0] * 100));
    line.setAttribute("y1", String(a[1] * 128));
    line.setAttribute("x2", String(b[0] * 100));
    line.setAttribute("y2", String(b[1] * 128));
    line.setAttribute("stroke", "#0e8a63");
    line.setAttribute("stroke-width", "4");
    line.setAttribute("stroke-linecap", "round");
    svg.append(line);
  }

  for (const point of Object.values(pose.joints || {})) {
    const circle = document.createElementNS(svg.namespaceURI, "circle");
    circle.setAttribute("cx", String(point[0] * 100));
    circle.setAttribute("cy", String(point[1] * 128));
    circle.setAttribute("r", "3.2");
    circle.setAttribute("fill", "#d87924");
    svg.append(circle);
  }
  return svg;
}

function drawPose(pose) {
  const canvas = els.canvas;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBackdrop(ctx, canvas);
  if (!pose) return;

  ctx.lineWidth = 12;
  ctx.lineCap = "round";
  ctx.strokeStyle = "#0e8a63";
  ctx.fillStyle = "#d87924";
  ctx.shadowColor = "rgba(0, 0, 0, 0.18)";
  ctx.shadowBlur = 8;

  for (const [from, to] of SKELETON_EDGES) {
    const a = pose.joints?.[from];
    const b = pose.joints?.[to];
    if (!a || !b) continue;
    ctx.beginPath();
    ctx.moveTo(a[0] * canvas.width, a[1] * canvas.height);
    ctx.lineTo(b[0] * canvas.width, b[1] * canvas.height);
    ctx.stroke();
  }

  ctx.shadowBlur = 0;
  for (const point of Object.values(pose.joints || {})) {
    ctx.beginPath();
    ctx.arc(point[0] * canvas.width, point[1] * canvas.height, 11, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawBackdrop(ctx, canvas) {
  if (state.backgroundImage) {
    const image = state.backgroundImage;
    const scale = Math.max(canvas.width / image.width, canvas.height / image.height);
    const width = image.width * scale;
    const height = image.height * scale;
    ctx.drawImage(image, (canvas.width - width) / 2, (canvas.height - height) / 2, width, height);
    ctx.fillStyle = "rgba(255, 255, 255, 0.18)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    return;
  }

  const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  gradient.addColorStop(0, "#dfe9df");
  gradient.addColorStop(0.55, "#eef3e9");
  gradient.addColorStop(1, "#cfdde1");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(47, 111, 163, 0.18)";
  ctx.fillRect(0, canvas.height * 0.62, canvas.width, canvas.height * 0.38);
}

function getActiveTags() {
  return [...new Set([...state.selectedTags, ...state.backgroundTags])].sort();
}

function splitTags(value) {
  return value
    .replaceAll(";", ",")
    .split(",")
    .map((tag) => tag.trim().toLowerCase().replace(/\s+/g, "_"))
    .filter(Boolean);
}

function inferTagsFromName(name) {
  const lower = name.toLowerCase();
  const tags = new Set();
  for (const [key, values] of Object.entries(TAG_HINTS)) {
    if (lower.includes(key)) {
      values.forEach((tag) => tags.add(tag));
    }
  }
  return [...tags];
}

function setStatus(message) {
  els.status.textContent = message;
}
