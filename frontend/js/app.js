/**
 * NeuroLearn Research Suite - Main Application Controller
 * Manages research state, navigation router across 21 workspaces, and UI telemetry.
 */

const AppState = {
  activeWorkspace: 'dashboard',
  dataset: {
    name: 'PhysioNet_S001 (Focused Task)',
    channels: ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz', 'Pz'],
    samplingRate: 256,
    durationSec: 30.0,
    sqiScore: 95.4,
    sourceType: 'PhysioNet_eegmmidb'
  },
  attention: {
    averageScore: 78.4,
    category: 'High Attention',
    formula: 'beta / theta',
    stabilityIndex: 89.2,
    dropEvents: 1
  }
};

function toggleSidebar() {
  document.getElementById('app-container').classList.toggle('sidebar-collapsed');
}

function switchWorkspace(workspaceId) {
  AppState.activeWorkspace = workspaceId;

  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
  });

  const activeNav = Array.from(document.querySelectorAll('.nav-item')).find(item => 
    item.getAttribute('onclick') && item.getAttribute('onclick').includes(workspaceId)
  );
  if (activeNav) activeNav.classList.add('active');

  const contentArea = document.getElementById('workspace-content');
  contentArea.innerHTML = '';

  switch (workspaceId) {
    case 'dashboard':
      renderDashboard(contentArea);
      break;
    case 'dataset_manager':
      renderDatasetManager(contentArea);
      break;
    case 'biopac_manager':
      renderBiopacManager(contentArea);
      break;
    case 'physionet_manager':
      renderPhysioNetManager(contentArea);
      break;
    case 'eeg_viewer':
      renderEEGViewer(contentArea);
      break;
    case 'signal_quality':
      renderSignalQuality(contentArea);
      break;
    case 'preprocessing':
      renderPreprocessingBuilder(contentArea);
      break;
    case 'feature_extraction':
      renderFeatureExtraction(contentArea);
      break;
    case 'frequency_analysis':
      renderFrequencyAnalysis(contentArea);
      break;
    case 'attention_analysis':
      renderAttentionAnalysis(contentArea);
      break;
    case 'statistical_analysis':
      renderStatisticalAnalysis(contentArea);
      break;
    case 'ablation_study':
      renderAblationStudy(contentArea);
      break;
    case 'research_validation':
      renderResearchValidation(contentArea);
      break;
    case 'reports':
      renderReportCenter(contentArea);
      break;
    case 'settings':
      renderSettings(contentArea);
      break;
    default:
      renderGenericWorkspace(contentArea, workspaceId);
  }

  logTelemetry(`Navigated to Workspace: ${workspaceId.toUpperCase()}`);
}

function logTelemetry(msg) {
  const timeStr = new Date().toLocaleTimeString();
  document.getElementById('log-console-text').innerText = `[${timeStr}] ${msg} | Mode: Non-ML BSP`;
}

/* WORKSPACE RENDERERS */

/* DASHBOARD 1: EXECUTIVE SCIENTIFIC OVERVIEW */
function renderDashboard(container) {
  container.innerHTML = `
    <h2 style="font-size: 22px; font-weight: 800; margin-bottom: 4px;">Executive Scientific Overview (Dashboard 1)</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Real-Time Cognitive Attention State, Signal Quality Telemetry, & Band Power Hub</p>
    
    <!-- ROW 1: 4-COLUMN HERO KPI CARDS -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Signal Quality Index</div>
        <div class="kpi-value">${AppState.dataset.sqiScore}%</div>
        <div class="kpi-subtext">13/13 Channels Passed Audit</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Mean Attention Score</div>
        <div class="kpi-value">${AppState.attention.averageScore} / 100</div>
        <div class="kpi-subtext">Category: ${AppState.attention.category}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Attention Stability</div>
        <div class="kpi-value">${AppState.attention.stabilityIndex}%</div>
        <div class="kpi-subtext">Drop Events: ${AppState.attention.dropEvents}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Acquisition System</div>
        <div class="kpi-value">PhysioNet</div>
        <div class="kpi-subtext">Sampling Rate: ${AppState.dataset.samplingRate} Hz</div>
      </div>
    </div>

    <!-- ROW 2: 65 / 35 SPLIT LAYOUT -->
    <div style="display: grid; grid-template-columns: 65% 35%; gap: 20px; margin-bottom: 24px;">
      <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px;">
        <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 12px;">📈 Real-Time Cognitive Attention Timeline</h3>
        <div id="plotly-att-preview" style="height: 340px;"></div>
      </div>

      <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px;">
        <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 12px;">🧠 Band Power Distribution</h3>
        <div style="display: flex; flex-direction: column; gap: 10px; font-family: var(--font-mono); font-size: 12px; margin-top: 10px;">
          <div style="display: flex; justify-content: space-between;"><span>Delta (0.5-4 Hz):</span><strong style="color: var(--band-delta);">8.4%</strong></div>
          <div style="display: flex; justify-content: space-between;"><span>Theta (4-8 Hz):</span><strong style="color: var(--band-theta);">12.1%</strong></div>
          <div style="display: flex; justify-content: space-between;"><span>Alpha (8-13 Hz):</span><strong style="color: var(--band-alpha);">18.2%</strong></div>
          <div style="display: flex; justify-content: space-between;"><span>Beta (13-30 Hz):</span><strong style="color: var(--band-beta);">45.6%</strong></div>
          <div style="display: flex; justify-content: space-between;"><span>Gamma (30-40 Hz):</span><strong style="color: var(--band-gamma);">15.7%</strong></div>
        </div>
        <hr style="margin: 14px 0; border-color: rgba(255,255,255,0.1);"/>
        <div style="font-size: 11px; color: var(--accent-cyan);">Active Formula: <code>beta / theta</code></div>
      </div>
    </div>

    <!-- ROW 3: PREPROCESSING PIPELINE FLOW -->
    <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px;">
      <h3 style="font-size: 14px; color: var(--text-primary); margin-bottom: 14px;">🛠️ Preprocessing Pipeline Sequence</h3>
      <div class="pipeline-container" style="padding: 10px 0;">
        <div class="pipeline-node"><div style="font-weight: 700; color: var(--accent-cyan);">1. Raw EEG</div><div style="font-size: 11px; color: var(--text-secondary);">Unfiltered Signal</div></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-node"><div style="font-weight: 700; color: var(--accent-cyan);">2. Bandpass</div><div style="font-size: 11px; color: var(--text-secondary);">1.0 - 40.0 Hz</div></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-node"><div style="font-weight: 700; color: var(--accent-cyan);">3. Notch Filter</div><div style="font-size: 11px; color: var(--text-secondary);">50.0 Hz Powerline</div></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-node"><div style="font-weight: 700; color: var(--accent-cyan);">4. Normalization</div><div style="font-size: 11px; color: var(--text-secondary);">Z-Score Detrend</div></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-node" style="border-color: var(--success-green);"><div style="font-weight: 700; color: var(--success-green);">5. SQI Audit</div><div style="font-size: 11px; color: var(--text-secondary);">13/13 Valid</div></div>
      </div>
    </div>
  `;

  setTimeout(() => {
    initAttentionTimelinePlot('plotly-att-preview');
  }, 100);
}

/* DASHBOARD 2: EEG WAVEFORM HUB & SPECTRAL WORKSPACE */
function renderEEGViewer(container) {
  container.innerHTML = `
    <h2 style="font-size: 22px; font-weight: 800; margin-bottom: 4px;">EEG Waveform Hub & Spectral Workspace (Dashboard 2)</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">High-Density Multi-Channel Stacked EEG Waveforms, Welch PSD Curves, & Channel Quality Audit</p>
    
    <!-- ROW 1: TOP CONTROL BAR -->
    <div style="display: flex; justify-content: space-between; align-items: center; background: var(--card-bg); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;">
      <div style="display: flex; gap: 14px; align-items: center;">
        <span style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Display Mode:</span>
        <button class="sci-btn" onclick="logTelemetry('Filter Mode: Preprocessed')">Preprocessed Filtered</button>
        <button class="sci-btn outline" onclick="logTelemetry('Filter Mode: Raw')">Raw Unfiltered</button>
      </div>

      <div style="display: flex; gap: 14px; align-items: center;">
        <span style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Window:</span>
        <button class="sci-btn outline" onclick="logTelemetry('Window: 5s')">5.0s</button>
        <button class="sci-btn outline" onclick="logTelemetry('Window: 10s')">10.0s</button>
        <button class="sci-btn outline" onclick="logTelemetry('Window: 30s')">30.0s</button>
      </div>
    </div>

    <!-- ROW 2: MULTI-CHANNEL STACKED WAVEFORMS CANVAS -->
    <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
      <div id="plotly-full-eeg" style="height: 480px;"></div>
    </div>

    <!-- ROW 3: 50 / 50 SPLIT (WELCH PSD CURVES & CHANNEL SQI AUDIT MATRIX) -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px;">
        <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 12px;">🌊 Welch Power Spectral Density (PSD)</h3>
        <div id="plotly-psd-preview" style="height: 280px;"></div>
      </div>

      <div style="background: var(--card-bg); backdrop-filter: var(--glass-backdrop); border: 1px solid rgba(100, 255, 218, 0.15); border-radius: 12px; padding: 20px;">
        <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 12px;">🛡️ Channel Quality Audit Matrix</h3>
        <table class="sci-table">
          <tr><th>Channel</th><th>SNR (dB)</th><th>SQI Status</th><th>Artifact Contamination</th></tr>
          <tr><td>Fp1</td><td>14.2 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
          <tr><td>Fp2</td><td>13.8 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
          <tr><td>F3</td><td>18.5 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
          <tr><td>F4</td><td>17.9 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
          <tr><td>C3</td><td>19.1 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
          <tr><td>Cz</td><td>21.4 dB</td><td><span class="status-badge">PASSED</span></td><td>Clean Signal</td></tr>
        </table>
      </div>
    </div>
  `;

  setTimeout(() => {
    initEEGPlot('plotly-full-eeg');
    initPSDPlot('plotly-psd-preview');
  }, 100);
}

function renderDatasetManager(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Dataset Manager</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Import, Validate, & Auto-Detect Metadata for EDF, MAT, CSV, & TXT Files</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
        <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 14px;">Import Data File</h3>
        <input type="file" id="file-input" style="margin-bottom: 14px; color: var(--text-primary);">
        <br>
        <button class="sci-btn" onclick="alert('File imported successfully!')">Load Dataset</button>
      </div>

      <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
        <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 14px;">Detected Metadata</h3>
        <table class="sci-table">
          <tr><th>Property</th><th>Detected Value</th></tr>
          <tr><td>Sampling Rate (fs)</td><td>256 Hz</td></tr>
          <tr><td>Channel Count</td><td>13 Channels</td></tr>
          <tr><td>Recording Duration</td><td>30.0 Seconds</td></tr>
          <tr><td>Signal Units</td><td>uV (Microvolts)</td></tr>
        </table>
      </div>
    </div>
  `;
}

function renderBiopacManager(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Biopac Import Manager</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Import Exported Biopac AcqKnowledge Recordings (MAT, CSV, EDF)</p>
    
    <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
      <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 12px;">Biopac AcqKnowledge Channel Normalization</h3>
      <p style="color: var(--text-secondary); margin-bottom: 14px;">Automatically strips prefix headers ('EEG100C - Cz' -> 'Cz') and aligns sampling frequencies to unified BSP pipeline.</p>
      <button class="sci-btn" onclick="alert('Biopac dataset normalized!')">Import Biopac AcqKnowledge Export</button>
    </div>
  `;
}

function renderPhysioNetManager(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">PhysioNet Manager</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Fetch & Analyze Public PhysioNet EEG Motor Movement/Imagery Datasets (eegmmidb)</p>
    
    <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
      <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 12px;">PhysioNet eegmmidb Fetcher</h3>
      <div style="display: flex; gap: 14px; margin-bottom: 14px;">
        <input type="number" value="1" min="1" max="109" style="background: var(--bg-dark); border: 1px solid var(--card-border); color: var(--text-primary); padding: 6px 12px; border-radius: 4px;">
        <button class="sci-btn" onclick="alert('PhysioNet Subject Loaded!')">Fetch Subject Recording</button>
      </div>
    </div>
  `;
}

function renderSignalQuality(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Signal Quality Index (SQI) Audit</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">SNR, Flat-Line Detection, Kurtosis Contamination, & Bad Channel Auto-Exclusion</p>
    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <div id="plotly-sqi-chart" style="height: 400px;"></div>
    </div>
  `;
  setTimeout(() => initSQIChart('plotly-sqi-chart'), 100);
}

function renderFeatureExtraction(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Multi-Domain Feature Extraction</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Time Domain Stats, Welch PSD, Hjorth Parameters, & Wavelet Entropy</p>
    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <table class="sci-table">
        <tr><th>Epoch</th><th>Hjorth Activity</th><th>Hjorth Mobility</th><th>Hjorth Complexity</th><th>SEF95 (Hz)</th><th>Wavelet Entropy</th></tr>
        <tr><td>Epoch 1 (0-5s)</td><td>142.5</td><td>0.142</td><td>1.85</td><td>28.4 Hz</td><td>0.842</td></tr>
        <tr><td>Epoch 2 (5-10s)</td><td>138.2</td><td>0.138</td><td>1.81</td><td>27.9 Hz</td><td>0.835</td></tr>
        <tr><td>Epoch 3 (10-15s)</td><td>145.1</td><td>0.146</td><td>1.89</td><td>29.1 Hz</td><td>0.851</td></tr>
      </table>
    </div>
  `;
}

function renderFrequencyAnalysis(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Frequency Analysis & Power Spectral Density</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Welch PSD Curves, Multitaper Spectral Estimation, & Spectrogram Heatmaps</p>
    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <div id="plotly-freq-chart" style="height: 400px;"></div>
    </div>
  `;
  setTimeout(() => initPSDPlot('plotly-freq-chart'), 100);
}

function renderAttentionAnalysis(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Mathematical Attention Analysis</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Non-ML Ratio Formulations, Custom Formula Evaluator, & State Classification</p>
    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <div id="plotly-att-full" style="height: 400px;"></div>
    </div>
  `;
  setTimeout(() => initAttentionTimelinePlot('plotly-att-full'), 100);
}

function renderStatisticalAnalysis(container) { renderStatsWorkspace(container); }
function renderAblationStudy(container) { renderAblationWorkspace(container); }
function renderResearchValidation(container) { renderStatsWorkspace(container); }
function renderReportCenter(container) { renderReportPreviewer(container); }
function renderSettings(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Global System Settings</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Configuration Overrides for Sampling Rate, Filter Bounds, & Thresholds</p>
    <div style="background: var(--card-bg); border: var(--glass-border); border-radius: 8px; padding: 20px;">
      <label style="display: block; margin-bottom: 6px; font-weight: 600;">Default Bandpass Low Cut (Hz):</label>
      <input type="number" value="1.0" step="0.5" style="background: var(--bg-dark); border: 1px solid var(--card-border); color: var(--text-primary); padding: 8px 12px; border-radius: 4px; margin-bottom: 14px;">
      <label style="display: block; margin-bottom: 6px; font-weight: 600;">Default Bandpass High Cut (Hz):</label>
      <input type="number" value="40.0" step="1.0" style="background: var(--bg-dark); border: 1px solid var(--card-border); color: var(--text-primary); padding: 8px 12px; border-radius: 4px; margin-bottom: 14px;">
      <br>
      <button class="sci-btn" onclick="alert('Settings saved!')">Save Configuration Overrides</button>
    </div>
  `;
}
function renderGenericWorkspace(container, id) {
  container.innerHTML = `<h2 style="font-size: 20px; font-weight: 700;">Workspace: ${id}</h2><p style="color: var(--text-secondary);">Module loaded successfully.</p>`;
}
