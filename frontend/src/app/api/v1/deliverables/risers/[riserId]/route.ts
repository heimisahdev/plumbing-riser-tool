import { NextRequest } from 'next/server';

export async function GET(_request: NextRequest, { params }: { params: { riserId: string } }) {
  const riserId = params.riserId || 'R-01';
  const svg = `
    <svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="background:#fff;">
      <rect x="0" y="0" width="600" height="340" fill="#ffffff" />
      <text x="30" y="30" font-size="18" font-weight="700" fill="#0f172a">RISER DIAGRAM: ${riserId}</text>
      <line x1="80" y1="60" x2="520" y2="60" stroke="#e2e8f0" stroke-dasharray="6,6" />
      <line x1="80" y1="130" x2="520" y2="130" stroke="#e2e8f0" stroke-dasharray="6,6" />
      <line x1="80" y1="200" x2="520" y2="200" stroke="#e2e8f0" stroke-dasharray="6,6" />
      <line x1="80" y1="270" x2="520" y2="270" stroke="#e2e8f0" stroke-dasharray="6,6" />
      <line x1="260" y1="60" x2="260" y2="270" stroke="#2563eb" stroke-width="4" />
      <line x1="130" y1="88" x2="260" y2="88" stroke="#3b82f6" stroke-width="3" />
      <line x1="130" y1="158" x2="260" y2="158" stroke="#3b82f6" stroke-width="3" />
      <line x1="130" y1="228" x2="260" y2="228" stroke="#3b82f6" stroke-width="3" />
      <circle cx="260" cy="88" r="6" fill="#1d4ed8" />
      <circle cx="260" cy="158" r="6" fill="#1d4ed8" />
      <circle cx="260" cy="228" r="6" fill="#1d4ed8" />
      <text x="30" y="48" font-size="12" fill="#475569">FL 11</text>
      <text x="30" y="118" font-size="12" fill="#475569">FL 9</text>
      <text x="30" y="188" font-size="12" fill="#475569">FL 7</text>
      <text x="30" y="258" font-size="12" fill="#475569">FL 5</text>
      <text x="280" y="95" font-size="11" font-weight="700" fill="#1e40af">Cum: 26 DFU</text>
      <text x="280" y="165" font-size="11" font-weight="700" fill="#1e40af">Cum: 18 DFU</text>
      <text x="280" y="235" font-size="11" font-weight="700" fill="#1e40af">Cum: 12 DFU</text>
    </svg>
  `;

  return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml' } });
}
