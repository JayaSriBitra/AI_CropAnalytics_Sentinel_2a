import { useEffect, useRef, useState } from 'react';
import {
  Activity, ArrowUpRight, Bell, CalendarDays, ChevronDown, CloudSun, Download,
  FileImage, FileText, LayoutDashboard, Leaf, Map, Menu, MoreHorizontal,
  RefreshCw, Search, Settings, Sprout, Upload, X,
} from 'lucide-react';
import { createReport, getDashboardData, uploadPrediction } from './services/api';

const navItems = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Field map', icon: Map },
  { label: 'NDVI analysis', icon: Activity },
  { label: 'Reports', icon: FileText },
];

function MetricCard({ label, value, detail, icon: Icon, tone = 'green' }) {
  return <article className="metric-card">
    <div className={`metric-icon ${tone}`}><Icon size={18} strokeWidth={1.8} /></div>
    <p>{label}</p>
    <strong>{value}</strong>
    <span className="metric-detail">{detail}</span>
  </article>;
}

function NdviChart({ values }) {
  const points = values.map((value, index) => `${index * 9.09},${92 - value * 82}`).join(' ');
  return <div className="chart-wrap">
    <div className="chart-legend"><span><i className="legend-dot" />Average NDVI</span><strong>0.63 <small>+8.2%</small></strong></div>
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="line-chart" role="img" aria-label="NDVI trend over the last twelve weeks">
      <defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#356859" stopOpacity=".23" /><stop offset="1" stopColor="#356859" stopOpacity="0" /></linearGradient></defs>
      {[20, 45, 70, 92].map((y) => <line key={y} x1="0" x2="100" y1={y} y2={y} className="grid-line" />)}
      <polygon points={`0,92 ${points} 100,92`} fill="url(#area)" />
      <polyline points={points} fill="none" stroke="#356859" strokeWidth="1.6" vectorEffect="non-scaling-stroke" />
      {values.map((value, index) => <circle key={index} cx={index * 9.09} cy={92 - value * 82} r="1.4" fill="#f6f7f2" stroke="#356859" strokeWidth="1" vectorEffect="non-scaling-stroke" />)}
    </svg>
    <div className="chart-labels"><span>Jan 08</span><span>Jan 22</span><span>Feb 05</span><span>Feb 19</span><span>Mar 04</span></div>
  </div>;
}

function FieldMap() {
  const fieldCells = Array.from({ length: 60 }, (_, index) => {
    const row = Math.floor(index / 10);
    const col = index % 10;
    const intensity = (row * 17 + col * 11) % 50;
    return <span key={index} className={`field-cell level-${Math.floor(intensity / 13)}`} />;
  });
  return <div className="map-frame">
    <div className="map-toolbar"><button className="map-control active"><Map size={15} /> Health map</button><button className="map-control">Satellite</button><button className="map-control">Boundary</button></div>
    <div className="map-grid" aria-label="Field health map">{fieldCells}<div className="field-label label-one">North plot</div><div className="field-label label-two">Orchard 04</div></div>
    <div className="map-scale"><span>Low</span><i /><span>High</span></div>
    <div className="map-caption"><span><i className="status-dot" />Live field layer</span><span>Sentinel-2 · 10m</span></div>
  </div>;
}

function UploadDialog({ onClose, onUploaded }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [state, setState] = useState('idle');
  const [error, setError] = useState('');

  async function submit() {
    if (!file) return;
    setState('uploading'); setError('');
    try { await uploadPrediction(file); setState('done'); onUploaded(file.name); }
    catch (requestError) { setState('error'); setError('The API is unavailable. The file stayed local and was not uploaded.'); }
  }
  return <div className="modal-backdrop" onClick={onClose}><section className="upload-modal" onClick={(event) => event.stopPropagation()}>
    <button className="icon-button modal-close" aria-label="Close upload dialog" onClick={onClose}><X size={18} /></button>
    <div className="modal-eyebrow"><Upload size={15} /> New analysis</div><h2>Upload a field image</h2><p className="modal-copy">Add a Sentinel-2 image to generate a segmentation and crop health report.</p>
    <button className="drop-zone" onClick={() => inputRef.current?.click()}><FileImage size={26} /><strong>{file ? file.name : 'Choose a GeoTIFF or image'}</strong><span>Up to 100 MB · PNG, JPG, TIFF</span></button>
    <input ref={inputRef} type="file" accept=".tif,.tiff,.png,.jpg,.jpeg" hidden onChange={(event) => setFile(event.target.files?.[0] || null)} />
    {error && <p className="form-error">{error}</p>}
    {state === 'done' && <p className="form-success">Upload accepted. Your analysis will appear in the activity feed.</p>}
    <div className="modal-actions"><button className="button secondary" onClick={onClose}>Cancel</button><button className="button primary" disabled={!file || state === 'uploading'} onClick={submit}>{state === 'uploading' ? 'Uploading...' : 'Start analysis'}<ArrowUpRight size={16} /></button></div>
  </section></div>;
}

function App() {
  const [activeNav, setActiveNav] = useState('Overview');
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);
  const [notice, setNotice] = useState('');

  async function refresh() {
    setLoading(true);
    const controller = new AbortController();
    setDashboard(await getDashboardData(controller.signal));
    setLoading(false);
  }
  useEffect(() => { refresh(); }, []);

  async function handleReport() {
    try { await createReport('latest'); setNotice('Report generation started'); }
    catch { setNotice('Reports API is not connected yet'); }
    window.setTimeout(() => setNotice(''), 3500);
  }

  const data = dashboard || { summary: {}, ndvi: [], classes: [], health: {} };
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Sprout size={19} /></div><div><strong>FieldSight</strong><span>Crop intelligence</span></div></div>
      <div className="workspace-switch"><span className="workspace-avatar">RA</span><div><small>Workspace</small><strong>Rajasekhar's fields</strong></div><ChevronDown size={15} /></div>
      <nav className="main-nav"><p className="nav-label">Workspace</p>{navItems.map(({ label, icon: Icon }) => <button key={label} className={activeNav === label ? 'nav-item active' : 'nav-item'} onClick={() => setActiveNav(label)}><Icon size={17} />{label}{label === 'Reports' && <span className="nav-count">3</span>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="season-card"><div className="season-icon"><CloudSun size={18} /></div><div><small>Current season</small><strong>Rabi · 2025</strong></div><MoreHorizontal size={16} /></div><button className="nav-item"><Settings size={17} />Settings</button><div className="profile"><div className="profile-avatar">RS</div><div><strong>Rajasekhar</strong><span>Field analyst</span></div><MoreHorizontal size={17} /></div></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><button className="mobile-menu icon-button" aria-label="Open navigation"><Menu size={20} /></button><div className="breadcrumb"><span>Workspace</span><span>/</span><strong>{activeNav}</strong></div><div className="top-actions"><div className="search-box"><Search size={16} /><input placeholder="Search fields, reports..." /></div><button className="icon-button notification" aria-label="Notifications"><Bell size={18} /><i /></button><button className="button primary compact" onClick={() => setShowUpload(true)}><Upload size={16} />New analysis</button></div></header>
      <div className="page-content">
        <section className="page-heading"><div><p className="eyebrow">Monday, March 04, 2025 <span className="live-pill"><i />{data.source === 'api' ? 'Connected' : 'Demo data'}</span></p><h1>Good morning, Rajasekhar</h1><p className="subheading">Here is what is happening across your fields today.</p></div><div className="heading-actions"><button className="button secondary"><CalendarDays size={16} />Last 90 days<ChevronDown size={14} /></button><button className="button secondary" onClick={handleReport}><Download size={16} />Export report</button></div></section>
        {notice && <div className="toast"><span className="toast-check">✓</span>{notice}</div>}
        <section className="metrics-grid">{loading ? <div className="loading-card">Refreshing field data...</div> : <><MetricCard label="Monitored area" value={`${data.summary.area || 0} ha`} detail="Across 8 active fields" icon={Map} /><MetricCard label="Crop health score" value={`${data.summary.health || 0}%`} detail={<><span className="up">↑ 6.4%</span> vs last period</>} icon={Leaf} tone="gold" /><MetricCard label="Projected yield" value={`${data.summary.yield || 0} t/ha`} detail={<><span className="up">↑ {data.summary.change || 0}%</span> vs last season</>} icon={Sprout} tone="blue" /><MetricCard label="Latest observation" value="2 days ago" detail="Sentinel-2 · 10m resolution" icon={CalendarDays} tone="slate" /></>}</section>
        <section className="dashboard-grid"><article className="panel chart-panel"><div className="panel-header"><div><p className="panel-kicker">Field performance</p><h2>NDVI trend</h2></div><button className="icon-button"><MoreHorizontal size={18} /></button></div><NdviChart values={data.ndvi.length ? data.ndvi : [0.3, 0.35]} /></article><article className="panel health-panel"><div className="panel-header"><div><p className="panel-kicker">Latest scan</p><h2>Crop health</h2></div><span className="date-tag">Feb 28, 2025</span></div><div className="health-score"><div className="score-ring"><span>{data.summary.health || 0}<small>/100</small></span></div><div><strong>Good condition</strong><p>Most fields are showing healthy vegetation with a small stressed zone in the east plot.</p></div></div><div className="health-breakdown">{data.classes.map((item) => <div key={item.label}><span><i style={{ background: item.color }} />{item.label}</span><strong>{item.value}%</strong></div>)}</div></article></section>
        <section className="lower-grid"><article className="panel map-panel"><div className="panel-header"><div><p className="panel-kicker">Spatial overview</p><h2>Field health map</h2></div><button className="button text-button">Open map <ArrowUpRight size={15} /></button></div><FieldMap /></article><article className="panel activity-panel"><div className="panel-header"><div><p className="panel-kicker">Recent activity</p><h2>Analysis history</h2></div><button className="icon-button" onClick={refresh} aria-label="Refresh activity"><RefreshCw size={17} /></button></div><div className="activity-list"><div className="activity-item"><div className="activity-icon green"><Leaf size={16} /></div><div><strong>NDVI analysis completed</strong><span>North plot · 2 days ago</span></div><span className="activity-status complete">Ready</span></div><div className="activity-item"><div className="activity-icon gold"><Upload size={16} /></div><div><strong>Imagery uploaded</strong><span>Field group A · 5 days ago</span></div><span className="activity-status">Processed</span></div><div className="activity-item"><div className="activity-icon blue"><FileText size={16} /></div><div><strong>Yield report generated</strong><span>Rabi season · 1 week ago</span></div><span className="activity-status">PDF</span></div></div><button className="view-all" onClick={() => setActiveNav('Reports')}>View all activity <ArrowUpRight size={15} /></button></article></section>
        <footer className="page-footer"><span><i className="status-dot" />Data refreshed just now</span><span>FieldSight v0.1 · <button>Help center</button></span></footer>
      </div>
    </main>
    {showUpload && <UploadDialog onClose={() => setShowUpload(false)} onUploaded={(name) => { setNotice(`${name} is queued for analysis`); setShowUpload(false); }} />}
  </div>;
}

export default App;