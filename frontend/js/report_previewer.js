/**
 * Report Center Previewer
 */
function renderReportPreviewer(container) {
  container.innerHTML = `
    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">Multi-Format Report Center</h2>
    <p style="color: var(--text-secondary); margin-bottom: 20px;">Generate IEEE/Frontiers-Styled PDF, Word DOCX, & CSV Laboratory Reports</p>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;">
      <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
        <h3 style="font-size: 14px; color: var(--accent-cyan); margin-bottom: 8px;">📄 IEEE PDF Report</h3>
        <p style="font-size: 11px; color: var(--text-secondary); margin-bottom: 14px;">Full academic report with Methods, SQI Audit, Attention Metrics, Discussion, & IEEE References.</p>
        <button class="sci-btn" onclick="alert('PDF Report Generated!')">Export PDF Report</button>
      </div>

      <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
        <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 8px;">📝 Word DOCX Report</h3>
        <p style="font-size: 11px; color: var(--text-secondary); margin-bottom: 14px;">Editable Microsoft Word document formatted for thesis chapter integration.</p>
        <button class="sci-btn outline" onclick="alert('DOCX Report Generated!')">Export Word DOCX</button>
      </div>

      <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
        <h3 style="font-size: 14px; color: var(--warning-amber); margin-bottom: 8px;">📊 Raw Metrics CSV</h3>
        <p style="font-size: 11px; color: var(--text-secondary); margin-bottom: 14px;">Epoch-level feature vectors, band powers, and attention scores dataset.</p>
        <button class="sci-btn outline" onclick="alert('CSV Exported!')">Export CSV Dataset</button>
      </div>
    </div>

    <div style="background: var(--card-bg); border: var(--glass-border); padding: 20px; border-radius: 8px;">
      <h3 style="font-size: 14px; color: var(--text-primary); margin-bottom: 12px;">Live Report Preview</h3>
      <div style="background: #ffffff; color: #172a45; padding: 30px; border-radius: 4px; font-family: sans-serif; font-size: 12px; line-height: 1.6; max-height: 400px; overflow-y: auto;">
        <h1 style="text-align: center; color: #0a192f; font-size: 18px;">NeuroLearn Research Suite</h1>
        <h3 style="text-align: center; color: #0052cc; font-size: 12px;">Biomedical Signal Processing & Cognitive Attention Laboratory Report</h3>
        <hr style="margin: 15px 0;">
        <p><strong>Subject ID:</strong> PhysioNet_S001 (Focused Task) | <strong>Date:</strong> 2026-08-05 | <strong>Methodology:</strong> Non-ML Pure BSP</p>
        <h4>1. Executive Summary</h4>
        <p>This report presents an objective biomedical signal processing analysis of student attention state derived from multi-channel EEG recordings. In strict accordance with transparent scientific principles, zero machine learning or black-box predictive models were employed.</p>
        <h4>2. Attention Metrics</h4>
        <ul>
          <li><strong>Average Attention Score:</strong> 78.4 / 100 (High Attention)</li>
          <li><strong>Peak Attention Score:</strong> 92.1 / 100</li>
          <li><strong>Attention Stability Index:</strong> 89.2%</li>
        </ul>
      </div>
    </div>
  `;
}
