import { PlanCanvasViewer } from '@/components/canvas/PlanCanvasViewer';
import { RiserExportView } from '@/components/risers/RiserExportView';

export default function HomePage() {
  return (
    <main className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MEP coordination suite</p>
          <h1>Plumbing Riser & Plan Coordination Tool</h1>
        </div>
        <div className="status-pill">Live project: Tower 42</div>
      </header>

      <section className="workspace-grid">
        <div className="sheet-panel">
          <div className="panel-header">
            <span>Sheet A-103.00</span>
            <span>Floors 3–11</span>
          </div>
          <PlanCanvasViewer />
        </div>

        <aside className="detail-panel">
          <RiserExportView projectId="demo-project" riserId="r-01" riserTag="R-01" />
        </aside>
      </section>
    </main>
  );
}
