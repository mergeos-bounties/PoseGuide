/**
 * Pose Detail Panel - Shows tips, camera cues, and variations when clicking a pose
 */

class PoseDetailPanel {
  constructor() {
    this.panel = null;
    this.currentPose = null;
    this.init();
  }

  init() {
    // Create detail panel element
    this.panel = document.createElement('section');
    this.panel.id = 'poseDetailPanel';
    this.panel.className = 'pose-detail-panel hidden';
    this.panel.setAttribute('aria-label', 'Pose details');
    
    // Insert after results list
    const resultsSection = document.querySelector('.results');
    if (resultsSection) {
      resultsSection.parentNode.insertBefore(this.panel, resultsSection.nextSibling);
    }
  }

  show(pose) {
    this.currentPose = pose;
    this.render();
    this.panel.classList.remove('hidden');
  }

  hide() {
    this.panel.classList.add('hidden');
    this.currentPose = null;
  }

  render() {
    if (!this.currentPose) return;

    const pose = this.currentPose;
    
    this.panel.innerHTML = `
      <div class="detail-header">
        <h3>${pose.name || pose.id}</h3>
        <button id="closeDetailPanel" class="close-btn" aria-label="Close">&times;</button>
      </div>
      
      <div class="detail-content">
        ${this.renderTags(pose)}
        ${this.renderTips(pose)}
        ${this.renderCameraCues(pose)}
        ${this.renderLighting(pose)}
        ${this.renderVariations(pose)}
        ${this.renderBestFor(pose)}
        ${this.renderAvoid(pose)}
      </div>
    `;

    // Add close handler
    document.getElementById('closeDetailPanel')?.addEventListener('click', () => this.hide());
  }

  renderTags(pose) {
    if (!pose.tags || pose.tags.length === 0) return '';
    
    const tagsHtml = pose.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
    return `
      <div class="detail-section">
        <h4>Tags</h4>
        <div class="tags-container">${tagsHtml}</div>
      </div>
    `;
  }

  renderTips(pose) {
    if (!pose.tips || pose.tips.length === 0) return '';
    
    const tipsHtml = pose.tips.map(tip => `<li>${tip}</li>`).join('');
    return `
      <div class="detail-section">
        <h4>Posing Tips</h4>
        <ul class="tips-list">${tipsHtml}</ul>
      </div>
    `;
  }

  renderCameraCues(pose) {
    if (!pose.camera_cues || pose.camera_cues.length === 0) return '';
    
    const cuesHtml = pose.camera_cues.map(cue => `<li>${cue}</li>`).join('');
    return `
      <div class="detail-section">
        <h4>Camera Cues</h4>
        <ul class="camera-list">${cuesHtml}</ul>
      </div>
    `;
  }

  renderLighting(pose) {
    if (!pose.lighting) return '';
    
    const lighting = pose.lighting;
    const tipsHtml = lighting.tips?.map(tip => `<li>${tip}</li>`).join('') || '';
    
    return `
      <div class="detail-section">
        <h4>Lighting</h4>
        <p><strong>Type:</strong> ${lighting.type || 'Not specified'}</p>
        <p><strong>Mood:</strong> ${lighting.mood || 'Not specified'}</p>
        ${lighting.sources ? `<p><strong>Sources:</strong> ${lighting.sources.join(', ')}</p>` : ''}
        ${tipsHtml ? `<ul class="lighting-tips">${tipsHtml}</ul>` : ''}
      </div>
    `;
  }

  renderVariations(pose) {
    if (!pose.variations || pose.variations.length === 0) return '';
    
    const variationsHtml = pose.variations.map(v => `
      <div class="variation-item">
        <strong>${v.name}</strong>
        <p>${v.description || ''}</p>
      </div>
    `).join('');
    
    return `
      <div class="detail-section">
        <h4>Variations</h4>
        <div class="variations-container">${variationsHtml}</div>
      </div>
    `;
  }

  renderBestFor(pose) {
    if (!pose.best_for || pose.best_for.length === 0) return '';
    
    const itemsHtml = pose.best_for.map(item => `<li>${item}</li>`).join('');
    return `
      <div class="detail-section">
        <h4>Best For</h4>
        <ul class="best-for-list">${itemsHtml}</ul>
      </div>
    `;
  }

  renderAvoid(pose) {
    if (!pose.avoid || pose.avoid.length === 0) return '';
    
    const itemsHtml = pose.avoid.map(item => `<li>${item}</li>`).join('');
    return `
      <div class="detail-section">
        <h4>Avoid</h4>
        <ul class="avoid-list">${itemsHtml}</ul>
      </div>
    `;
  }
}

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PoseDetailPanel;
}
