'use client';

export function PlanCanvasViewer() {
  const points = [
    { left: '18%', top: '28%' },
    { left: '32%', top: '42%' },
    { left: '52%', top: '34%' },
    { left: '60%', top: '58%' },
    { left: '74%', top: '48%' },
  ];

  return (
    <div className="canvas-area">
      <div className="canvas-board">
        <div className="canvas-sheet" aria-label="Plan sheet viewer">
          <div className="sheet-grid" />
          {points.map((point, index) => (
            <div key={index} className="fixture" style={{ left: point.left, top: point.top }} />
          ))}
          <div className="riser-marker" style={{ left: '58%', top: '48%' }} />
        </div>
      </div>
    </div>
  );
}
