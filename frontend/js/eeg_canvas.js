/**
 * High-Performance Multi-Channel EEG Signal & Spectral Renderer
 * Uses Plotly.js to render dark medical scientific charts.
 */

function initEEGPlot(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const fs = 256;
  const duration = 10;
  const nSamples = fs * duration;
  const t = Array.from({length: nSamples}, (_, i) => i / fs);

  const channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz', 'Pz'];
  const traces = [];
  let offset = 0;

  channels.forEach((ch, idx) => {
    // Generate realistic sinusoidal EEG signal with noise
    const sig = t.map(time => {
      const theta = 12 * Math.sin(2 * Math.PI * 6.0 * time);
      const alpha = 18 * Math.sin(2 * Math.PI * 10.5 * time);
      const beta = 35 * Math.sin(2 * Math.PI * 21.0 * time);
      const noise = (Math.random() - 0.5) * 8;
      return theta + alpha + beta + noise + offset;
    });

    traces.push({
      x: t,
      y: sig,
      mode: 'lines',
      name: ch,
      line: { width: 1.2 }
    });

    offset -= 60;
  });

  const layout = {
    title: { text: '<b>Multi-Channel Stacked EEG Waveforms</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Time (seconds)', gridcolor: '#233554', zerolinecolor: '#233554' },
    yaxis: { title: 'Amplitude (uV) [Stacked]', gridcolor: '#233554', zerolinecolor: '#233554' },
    legend: { font: { color: '#e6f1ff' }, bgcolor: 'rgba(0,0,0,0)' }
  };

  Plotly.newPlot(elementId, traces, layout, { responsive: true });
}

function initAttentionTimelinePlot(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const t = [0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0];
  const scores = [65.2, 71.0, 78.4, 82.5, 88.1, 85.3, 76.2, 79.5, 84.0, 89.2, 91.5, 86.4, 82.1];

  const trace = {
    x: t,
    y: scores,
    mode: 'lines+markers',
    name: 'Attention Score',
    line: { color: '#64ffda', width: 2.5 },
    marker: { size: 6, color: '#00d2ff' }
  };

  const layout = {
    title: { text: '<b>Neurophysiological Attention Score Timeline (0-100 Scale)</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Recording Time (seconds)', gridcolor: '#233554' },
    yaxis: { title: 'Attention Index (0-100)', range: [0, 105], gridcolor: '#233554' },
    shapes: [
      { type: 'rect', y0: 80, y1: 100, x0: 0, x1: 30, fillcolor: 'rgba(0,230,118,0.1)', line: { width: 0 } },
      { type: 'rect', y0: 60, y1: 80, x0: 0, x1: 30, fillcolor: 'rgba(100,255,218,0.1)', line: { width: 0 } },
      { type: 'rect', y0: 40, y1: 60, x0: 0, x1: 30, fillcolor: 'rgba(52,152,219,0.1)', line: { width: 0 } }
    ]
  };

  Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

function initSQIChart(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz', 'Pz'];
  const sqi = [94, 96, 92, 95, 98, 97, 96, 95, 94, 93, 97, 99, 98];

  const trace = {
    x: channels,
    y: sqi,
    type: 'bar',
    marker: { color: '#64ffda' },
    text: sqi.map(s => `${s}%`),
    textposition: 'auto'
  };

  const layout = {
    title: { text: '<b>Signal Quality Index (SQI) Per Channel</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Channel Label', gridcolor: '#233554' },
    yaxis: { title: 'SQI Score (%)', range: [0, 105], gridcolor: '#233554' }
  };

  Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

function initPSDPlot(elementId) {
  const container = document.getElementById(elementId);
  if (!container) return;

  const freqs = Array.from({length: 100}, (_, i) => i * 0.45);
  const psd = freqs.map(f => {
    const theta = 30 * Math.exp(-Math.pow(f - 6.0, 2) / 2);
    const alpha = 45 * Math.exp(-Math.pow(f - 10.5, 2) / 2);
    const beta = 85 * Math.exp(-Math.pow(f - 21.0, 2) / 10);
    const gamma = 25 * Math.exp(-Math.pow(f - 35.0, 2) / 10);
    return theta + alpha + beta + gamma + Math.random() * 2;
  });

  const trace = {
    x: freqs,
    y: psd,
    mode: 'lines',
    name: 'Cz PSD',
    line: { color: '#00d2ff', width: 2 }
  };

  const layout = {
    title: { text: '<b>Power Spectral Density (Welch Method) - Channel Cz</b>', font: { color: '#e6f1ff', size: 14 } },
    paper_bgcolor: '#172a45',
    plot_bgcolor: '#0a192f',
    font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 30, t: 40, b: 40 },
    xaxis: { title: 'Frequency (Hz)', range: [0, 45], gridcolor: '#233554' },
    yaxis: { title: 'Power (uV^2 / Hz)', gridcolor: '#233554' }
  };

  Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}
