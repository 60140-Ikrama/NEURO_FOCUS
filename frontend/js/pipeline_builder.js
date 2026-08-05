/**
 * Pipeline Builder Visualizer
 */
function renderPreprocessingBuilder(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Preprocessing Pipeline Builder</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Visual Filter Sequence Node Builder & Before vs. After Overlay</p>
    
    <div class="pipeline-container">
      <div class="pipeline-node">
        <div style="font-weight: 700; color: var(--accent-cyan);">1. Raw Signal</div>
        <div style="font-size: 11px; color: var(--text-secondary);">Baseline Offset</div>
      </div>
      <div class="pipeline-arrow">➔</div>
      <div class="pipeline-node">
        <div style="font-weight: 700; color: var(--accent-cyan);">2. Bandpass Filter</div>
        <div style="font-size: 11px; color: var(--text-secondary);">1.0 - 40.0 Hz (4th Order)</div>
      </div>
      <div class="pipeline-arrow">➔</div>
      <div class="pipeline-node">
        <div style="font-weight: 700; color: var(--accent-cyan);">3. Notch Filter</div>
        <div style="font-size: 11px; color: var(--text-secondary);">50.0 Hz Powerline</div>
      </div>
      <div class="pipeline-arrow">➔</div>
      <div class="pipeline-node">
        <div style="font-weight: 700; color: var(--accent-cyan);">4. Normalization</div>
        <div style="font-size: 11px; color: var(--text-secondary);">Z-Score Standardization</div>
      </div>
      <div class="pipeline-arrow">➔</div>
      <div class="pipeline-node" style="border-color: var(--success-green);">
        <div style="font-weight: 700; color: var(--success-green);">5. SQI Audit</div>
        <div style="font-size: 11px; color: var(--text-secondary);">13/13 Valid</div>
      </div>
    </div>

    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px; margin-top: 20px;">
      <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 12px;">Preprocessed vs Raw Signal Overlay Comparison</h3>
      <div id="plotly-pipeline-overlay" style="height: 380px;"></div>
    </div>
  `;

  setTimeout(() => {
    initPipelineOverlay('plotly-pipeline-overlay');
  }, 100);
}

function initPipelineOverlay(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const t = Array.from({length: 256}, (_, i) => i / 256);
  const raw = t.map(time => 50 + 20 * Math.sin(2 * Math.PI * 10 * time) + 15 * Math.sin(2 * Math.PI * 50 * time) + (Math.random() - 0.5) * 10);
  const clean = t.map(time => (20 * Math.sin(2 * Math.PI * 10 * time)) / 15);

  Plotly.newPlot(elementId, [
    { x: t, y: raw, mode: 'lines', name: 'Raw Unfiltered Signal', line: { color: '#ff4d4d', width: 1.2 } },
    { x: t, y: clean, mode: 'lines', name: 'Filtered Standardized Signal', line: { color: '#64ffda', width: 2 } }
  ], {
    title: { text: '<b>Raw vs Preprocessed Signal Overlay</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Time (seconds)', gridcolor: '#233554' },
    yaxis: { title: 'Amplitude', gridcolor: '#233554' }
  }, { responsive: true });
}
