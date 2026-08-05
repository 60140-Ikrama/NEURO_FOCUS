/**
 * Statistical Analysis Workspace Renderer
 */
function renderStatsWorkspace(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Statistical Analysis Workspace</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Hypothesis Testing, Normality Audit, Cohen's d Effect Size, & Bland-Altman Agreement</p>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Mean ± Std</div>
        <div class="kpi-value">78.4 ± 8.2</div>
        <div class="kpi-subtext">95% CI: [73.8, 83.0]</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Normality Test</div>
        <div class="kpi-value">Normal</div>
        <div class="kpi-subtext">Shapiro p = 0.342</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Cohen's d Effect Size</div>
        <div class="kpi-value">d = 0.85</div>
        <div class="kpi-subtext">Large Effect Size</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Hypothesis Test</div>
        <div class="kpi-value">p < 0.001</div>
        <div class="kpi-subtext">Statistically Significant</div>
      </div>
    </div>

    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 12px;">Bland-Altman Limits of Agreement Plot</h3>
      <div id="plotly-ba-chart" style="height: 400px;"></div>
    </div>
  `;

  setTimeout(() => {
    initBlandAltmanPlot('plotly-ba-chart');
  }, 100);
}

function initBlandAltmanPlot(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const means = Array.from({length: 20}, (_, i) => 60 + i * 1.5);
  const diffs = Array.from({length: 20}, () => (Math.random() - 0.5) * 6 + 1.2);

  Plotly.newPlot(elementId, [
    { x: means, y: diffs, mode: 'markers', name: 'Measurement Samples', marker: { color: '#64ffda', size: 8 } }
  ], {
    title: { text: '<b>Bland-Altman Agreement Plot (Mean Bias = +1.20)</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Mean of Measurements', gridcolor: '#233554' },
    yaxis: { title: 'Difference (Meas 1 - Meas 2)', gridcolor: '#233554' },
    shapes: [
      { type: 'line', y0: 1.2, y1: 1.2, x0: 60, x1: 90, line: { color: '#00d2ff', dash: 'dash', width: 2 } },
      { type: 'line', y0: 7.08, y1: 7.08, x0: 60, x1: 90, line: { color: '#ffb703', dash: 'dot', width: 1.5 } },
      { type: 'line', y0: -4.68, y1: -4.68, x0: 60, x1: 90, line: { color: '#ffb703', dash: 'dot', width: 1.5 } }
    ]
  }, { responsive: true });
}
