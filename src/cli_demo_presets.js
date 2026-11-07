export const DEMO_PRESETS = Object.freeze({
  beach: {
    scene: "beach_sunset",
    topPose: "beach_walk_side_profile",
    confidence: 0.94,
    tip: "Keep shoulders relaxed at 35 degrees toward the horizon light."
  },
  urban: {
    scene: "urban_street",
    topPose: "city_crosswalk_stride",
    confidence: 0.92,
    tip: "Use leading street lines and mid-stride weight transfer."
  }
});

export function runPoseGuideDemo(preset = "beach") {
  const key = String(preset || "beach").toLowerCase() === "urban" ? "urban" : "beach";
  const item = DEMO_PRESETS[key];
  return `[PoseGuide Demo - ${key.toUpperCase()}] Top Pose: ${item.topPose} (${Math.round(item.confidence * 100)}%) — ${item.tip}`;
}
