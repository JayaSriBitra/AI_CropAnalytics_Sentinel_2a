import {
  ChevronDown,
  CloudSun,
  LayoutDashboard,
  Map,
  Activity,
  FileText,
  MoreHorizontal,
  Settings,
  Sprout,
  X,
} from 'lucide-react';

const navItems = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Field map', icon: Map },
  { label: 'NDVI analysis', icon: Activity },
  { label: 'Reports', icon: FileText },
];

function Sidebar({ activeNav, onNavigate, isOpen = false, onClose }) {
  const navigate = (label) => {
    onNavigate(label);
    if (onClose) onClose();
  };

  return (
    <>
      {isOpen && (
        <button
          type="button"
          aria-label="Close navigation"
          onClick={onClose}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 20,
            border: 0,
            background: 'rgba(30, 46, 38, 0.35)',
          }}
        />
      )}

      <aside
        className="sidebar"
        aria-label="Primary navigation"
        style={isOpen ? { display: 'flex', position: 'fixed', zIndex: 21, inset: '0 auto 0 0', width: 248 } : undefined}
      >
        <div className="brand">
          <div className="brand-mark"><Sprout size={19} /></div>
          <div><strong>FieldSight</strong><span>Crop intelligence</span></div>
          {isOpen && (
            <button className="icon-button" type="button" aria-label="Close sidebar" onClick={onClose} style={{ marginLeft: 'auto' }}>
              <X size={18} />
            </button>
          )}
        </div>

        <button className="workspace-switch" type="button" aria-label="Switch workspace">
          <span className="workspace-avatar">RA</span>
          <div><small>Workspace</small><strong>Rajasekhar's fields</strong></div>
          <ChevronDown size={15} />
        </button>

        <nav className="main-nav" aria-label="Workspace">
          <p className="nav-label">Workspace</p>
          {navItems.map(({ label, icon: Icon }) => (
            <button
              key={label}
              type="button"
              className={activeNav === label ? 'nav-item active' : 'nav-item'}
              aria-current={activeNav === label ? 'page' : undefined}
              onClick={() => navigate(label)}
            >
              <Icon size={17} />
              {label}
              {label === 'Reports' && <span className="nav-count">3</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="season-card">
            <div className="season-icon"><CloudSun size={18} /></div>
            <div><small>Current season</small><strong>Rabi · 2025</strong></div>
            <MoreHorizontal size={16} />
          </div>

          <button className="nav-item" type="button" onClick={() => navigate('Settings')}>
            <Settings size={17} />Settings
          </button>

          <div className="profile">
            <div className="profile-avatar">RS</div>
            <div><strong>Rajasekhar</strong><span>Field analyst</span></div>
            <MoreHorizontal size={17} />
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
