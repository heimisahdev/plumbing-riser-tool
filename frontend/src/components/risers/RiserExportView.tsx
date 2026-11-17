'use client';

import { useState } from 'react';

export function RiserExportView({ projectId, riserId, riserTag }: { projectId: string; riserId: string; riserTag: string }) {
  const [activeTab, setActiveTab] = useState<'DIAGRAM' | 'TAKEOFF'>('DIAGRAM');

  const svgMarkup = `
    <svg class="diagram-svg" viewBox="0 0 500 360" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="500" height="360" fill="#ffffff" />
      <text x="18" y="28" font-size="14" font-weight="700" fill="#0f172a">RISER DIAGRAM: ${riserId}</text>
      <line x1="80" y1="60" x2="420" y2="60" stroke="#e2e8f0" stroke-dasharray="5,5" />
      <line x1="80" y1="130" x2="420" y2="130" stroke="#e2e8f0" stroke-dasharray="5,5" />
      <line x1="80" y1="200" x2="420" y2="200" stroke="#e2e8f0" stroke-dasharray="5,5" />
      <line x1="80" y1="270" x2="420" y2="270" stroke="#e2e8f0" stroke-dasharray="5,5" />
      <line x1="230" y1="60" x2="230" y2="270" stroke="#2563eb" stroke-width="4" />
      <line x1="120" y1="90" x2="230" y2="90" stroke="#3b82f6" stroke-width="2.5" />
      <circle cx="230" cy="90" r="5" fill="#1d4ed8" />
      <line x1="120" y1="160" x2="230" y2="160" stroke="#3b82f6" stroke-width="2.5" />
      <circle cx="230" cy="160" r="5" fill="#1d4ed8" />
      <line x1="120" y1="230" x2="230" y2="230" stroke="#3b82f6" stroke-width="2.5" />
      <circle cx="230" cy="230" r="5" fill="#1d4ed8" />
      <text x="20" y="48" font-size="12" fill="#475569">FL 11</text>
      <text x="20" y="118" font-size="12" fill="#475569">FL 9</text>
      <text x="20" y="188" font-size="12" fill="#475569">FL 7</text>
      <text x="20" y="258" font-size="12" fill="#475569">FL 5</text>
      <text x="250" y="98" font-size="10" fill="#1e40af">Cum: 26 DFU</text>
      <text x="250" y="168" font-size="10" fill="#1e40af">Cum: 18 DFU</text>
      <text x="250" y="238" font-size="10" fill="#1e40af">Cum: 12 DFU</text>
    </svg>
  `;

  return (
    <div className="export-card">
      <div className="export-header">
        <div className="riser-tag">{riserTag}</div>
        <div>
          <strong>Vertical Riser Deliverable</strong>
          <div style={{ color: '#475569', fontSize: 12 }}>Project {projectId}</div>
        </div>
      </div>

      <div className="export-controls">
        <button className={`tab-btn ${activeTab === 'DIAGRAM' ? 'active' : ''}`} onClick={() => setActiveTab('DIAGRAM')}>
          Diagram
        </button>
        <button className={`tab-btn ${activeTab === 'TAKEOFF' ? 'active' : ''}`} onClick={() => setActiveTab('TAKEOFF')}>
          Takeoff
        </button>
        <button className="action-btn" onClick={() => window.print()}>
          Print PDF
        </button>
      </div>

      {activeTab === 'DIAGRAM' ? (
        <div className="diagram-surface" dangerouslySetInnerHTML={{ __html: svgMarkup }} />
      ) : (
        <div className="diagram-surface" style={{ fontSize: 12, color: '#0f172a' }}>
          <p><strong>Fixture schedule for {riserTag}</strong></p>
          <ul style={{ paddingLeft: 18, lineHeight: 1.8 }}>
            <li>WC — 12 units — 48 DFU</li>
            <li>LAV — 8 units — 8 DFU</li>
            <li>KS — 4 units — 8 DFU</li>
          </ul>
          <a href={`/api/v1/deliverables/projects/${projectId}/takeoff/export.csv`} style={{ color: '#2563eb', fontWeight: 700 }}>Export CSV</a>
        </div>
      )}
    </div>
  );
}
